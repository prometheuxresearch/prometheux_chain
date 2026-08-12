#!/usr/bin/env python3
"""CI-A: on a PR merged into main (a release), draft user-facing changelog
entries and open ONE PR in the changelog repo for human review.

Two modes, chosen by the release PR's head branch:

  * RELEASE (head == develop): the develop -> main merge. Enumerate the feature
    PRs that went into develop (via the release's commit range), draft one entry
    per feature PR, and add them all in a single changelog PR. Entries are dated
    with the release (main-merge) date — that's when they shipped to prod.

  * SINGLE (head != develop): a feature branch merged straight to main. Draft one
    entry from that PR, as before.

Description only — never the diff. Internal-only PRs (model publish=false) are
skipped by default (SKIP_INTERNAL=true) and listed in the PR body so nothing is
dropped silently.

Reads on the source repo use `gh` (GITHUB_TOKEN). Writes to the changelog repo
use CHANGELOG_TOKEN. Deps: anthropic, requests, gh CLI.

Env:
  ANTHROPIC_API_KEY   Claude API key
  CHANGELOG_TOKEN     token with contents+PR write on the changelog repo
  CHANGELOG_REPO      owner/name of the changelog repo
  GH_TOKEN            token with read on the source repo (the Actions GITHUB_TOKEN)
  SOURCE_REPO         owner/name of this product repo
  RELEASE_PR          the merged PR number
  HEAD_REF            head branch of the merged PR
  RELEASE_DATE        merged_at of the release PR (ISO)
  DEVELOP_BRANCH      staging branch name (default: develop)
  SKIP_INTERNAL       skip publish=false entries (default: true)
  CHANGELOG_MODEL     default: claude-opus-4-8
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys

import anthropic
import requests

GH_API = "https://api.github.com"
MODEL = os.environ.get("CHANGELOG_MODEL", "claude-opus-4-8")
DEVELOP_BRANCH = os.environ.get("DEVELOP_BRANCH", "develop")
SKIP_INTERNAL = os.environ.get("SKIP_INTERNAL", "true").lower() == "true"

ENTRY_SCHEMA = {
    "type": "object",
    "properties": {
        "publish": {"type": "boolean",
                    "description": "True if worth a user-facing entry; False for pure chores "
                                   "(CI, refactors, tests, dependency bumps, internal instrumentation)."},
        "title": {"type": "string",
                  "description": "Headline, ~4-8 words, sentence case, no trailing period, per "
                                 "the style guide. E.g. 'Unified context layer'."},
        "feature": {"type": "string", "description": "kebab-case feature slug; may span repos/PRs."},
        "area": {"type": "string", "description": "product area, e.g. editor, apps, ontology, compute, cli, engine"},
        "category": {"type": "string",
                     "enum": ["Added", "Changed", "Fixed", "Deprecated", "Removed", "Security"]},
        "entry": {"type": "string",
                  "description": "The changelog body, length scaled to the change per the style "
                                 "guide. Small change: one sentence. Substantial feature: a lead "
                                 "sentence, then a blank line, then 2-5 markdown '- ' bullets of "
                                 "concrete user-facing sub-capabilities. Markdown allowed."},
    },
    "required": ["publish", "title", "feature", "area", "category", "entry"],
    "additionalProperties": False,
}

DEFAULT_STYLE = """Write one user-facing sentence, benefit-first, present tense, active voice.
Summarize the impact; do not enumerate every affected element.
No repo names, file paths, PR numbers, or engineer names in the body.
Categories: Added / Changed / Fixed / Deprecated / Removed / Security."""


# ---- source-repo reads (gh CLI, GITHUB_TOKEN) --------------------------------

def sh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def sh_json(*args: str):
    return json.loads(sh(*args))


def pr_data(repo: str, number: int) -> dict:
    d = sh_json("pr", "view", str(number), "--repo", repo,
                "--json", "title,body,labels,files,mergedAt,baseRefName,headRefName")
    return {
        "number": number,
        "title": d.get("title", ""),
        "body": d.get("body", "") or "",
        "labels": ",".join(l["name"] for l in d.get("labels", [])),
        "files": "\n".join(f["path"] for f in d.get("files", [])),
        "merged_at": d.get("mergedAt", "") or "",
    }


def constituent_feature_prs(repo: str, release_pr: int) -> list[int]:
    """Feature PRs (base == develop) whose commits are in this release."""
    shas = sh("api", "--paginate",
              f"repos/{repo}/pulls/{release_pr}/commits", "--jq", ".[].sha").split()
    print(f"release #{release_pr}: {len(shas)} commits to scan")
    ordered: dict[int, None] = {}
    for sha in shas:
        try:
            rows = sh("api", f"repos/{repo}/commits/{sha}/pulls",
                      "--jq", '.[] | "\\(.number) \\(.base.ref)"')
        except subprocess.CalledProcessError:
            continue
        for row in rows.splitlines():
            if not row.strip():
                continue
            num_s, _, base_ref = row.partition(" ")
            try:
                num = int(num_s)
            except ValueError:
                continue
            if num != release_pr and base_ref == DEVELOP_BRANCH:
                ordered.setdefault(num, None)
    return list(ordered)


# ---- changelog-repo writes (requests, CHANGELOG_TOKEN) -----------------------

def capi(method: str, url: str, token: str, **kwargs) -> requests.Response:
    headers = kwargs.pop("headers", {})
    headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    return requests.request(method, url, headers=headers, timeout=30, **kwargs)


def fetch_style(repo: str, token: str) -> str:
    resp = capi("GET", f"{GH_API}/repos/{repo}/contents/STYLE.md", token)
    if resp.status_code == 200:
        try:
            return base64.b64decode(resp.json().get("content", "")).decode("utf-8")
        except Exception:
            pass
    print("warning: could not fetch STYLE.md, using default voice", file=sys.stderr)
    return DEFAULT_STYLE


def open_changelog_pr(changelog_repo: str, token: str, branch: str,
                      files: list[tuple[str, str]], title: str, body: str) -> None:
    repo_resp = capi("GET", f"{GH_API}/repos/{changelog_repo}", token)
    if repo_resp.status_code != 200:
        print(f"error: CHANGELOG_TOKEN cannot read {changelog_repo} "
              f"(HTTP {repo_resp.status_code}: "
              f"{repo_resp.json().get('message', repo_resp.text)}). Needs Contents + "
              f"Pull requests read/write on that repo.", file=sys.stderr)
        sys.exit(1)
    base = repo_resp.json()["default_branch"]
    base_sha = capi("GET", f"{GH_API}/repos/{changelog_repo}/git/ref/heads/{base}",
                    token).json()["object"]["sha"]

    if capi("GET", f"{GH_API}/repos/{changelog_repo}/git/ref/heads/{branch}",
            token).status_code == 404:
        capi("POST", f"{GH_API}/repos/{changelog_repo}/git/refs", token,
             json={"ref": f"refs/heads/{branch}", "sha": base_sha})

    for path, content in files:
        existing = capi("GET",
                        f"{GH_API}/repos/{changelog_repo}/contents/{path}?ref={branch}",
                        token)
        put_body = {
            "message": f"changelog: {path}",
            "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
            "branch": branch,
        }
        if existing.status_code == 200:
            put_body["sha"] = existing.json()["sha"]
        put = capi("PUT", f"{GH_API}/repos/{changelog_repo}/contents/{path}", token, json=put_body)
        if put.status_code not in (200, 201):
            print(f"error writing {path}: {put.status_code} {put.text}", file=sys.stderr)
            sys.exit(1)

    owner = changelog_repo.split("/")[0]
    open_prs = capi("GET", f"{GH_API}/repos/{changelog_repo}/pulls", token,
                    params={"head": f"{owner}:{branch}", "state": "open"}).json()
    if open_prs:
        print(f"PR already open: {open_prs[0]['html_url']}")
        return
    pr_resp = capi("POST", f"{GH_API}/repos/{changelog_repo}/pulls", token,
                   json={"title": title, "head": branch, "base": base, "body": body})
    if pr_resp.status_code == 201:
        print(f"opened PR: {pr_resp.json()['html_url']}")
    else:
        print(f"error opening PR: {pr_resp.status_code} {pr_resp.text}", file=sys.stderr)
        sys.exit(1)


# ---- drafting ----------------------------------------------------------------

def classify(style: str, source_repo: str, pr: dict) -> dict:
    client = anthropic.Anthropic()
    system = ("You write entries for the Prometheux user-facing platform changelog. "
              "Follow this style guide exactly:\n\n" + style)
    user = f"""A pull request merged in `{source_repo}`. Draft its changelog entry.

Title: {pr['title']}

Description:
{pr['body'] or '(no description)'}

Labels: {pr['labels'] or '(none)'}

Changed files:
{pr['files'] or '(not provided)'}

Return the structured entry. If this is a pure internal chore with no user-visible
effect, set publish=false (still fill the other fields with your best guess)."""
    resp = client.messages.create(
        model=MODEL, max_tokens=1024, system=system,
        messages=[{"role": "user", "content": user}],
        output_config={"format": {"type": "json_schema", "schema": ENTRY_SCHEMA}},
    )
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text)


def render_entry(meta: dict, repo_short: str, pr: int, date: str) -> str:
    title = meta.get("title", "").replace('"', "'")
    return ("---\n"
            f'title: "{title}"\n'
            f"feature: {meta['feature']}\n"
            f"area: {meta['area']}\n"
            f"category: {meta['category']}\n"
            f"repo: {repo_short}\n"
            f"pr: {pr}\n"
            f"date: {date}\n"
            "---\n"
            f"{meta['entry'].strip()}\n")


def entry_path(meta: dict, repo_short: str, pr: int) -> str:
    return f"entries/{meta['feature']}/{repo_short}-{pr}.mdx"


def main() -> int:
    source_repo = os.environ["SOURCE_REPO"]
    changelog_repo = os.environ["CHANGELOG_REPO"]
    ctoken = os.environ["CHANGELOG_TOKEN"]
    release_pr = int(os.environ["RELEASE_PR"])
    head_ref = os.environ.get("HEAD_REF", "")
    release_date = (os.environ.get("RELEASE_DATE", "") or "")[:10]
    repo_short = source_repo.split("/")[-1]

    style = fetch_style(changelog_repo, ctoken)

    # RELEASE mode: develop -> main. Fan out over constituent feature PRs.
    if head_ref == DEVELOP_BRANCH:
        feature_prs = constituent_feature_prs(source_repo, release_pr)
        print(f"constituent feature PRs (base={DEVELOP_BRANCH}): {feature_prs or 'none'}")
        if not feature_prs:
            print("no constituent feature PRs found; falling back to single-entry mode")
            head_ref = ""  # fall through to single mode below
        else:
            files, skipped = [], []
            for n in feature_prs:
                pr = pr_data(source_repo, n)
                meta = classify(style, source_repo, pr)
                print(f"  #{n}: {json.dumps(meta)}")
                if SKIP_INTERNAL and not meta.get("publish", True):
                    skipped.append((n, meta.get("entry", "")))
                    continue
                files.append((entry_path(meta, repo_short, n),
                              render_entry(meta, repo_short, n, release_date)))
            if not files:
                print("nothing publishable in this release; no PR opened")
                return 0
            body_lines = [f"Auto-drafted from the {source_repo} release (#{release_pr}, "
                          f"`{DEVELOP_BRANCH}` → `main`).", "",
                          f"**{len(files)} entr{'y' if len(files) == 1 else 'ies'}** for review. "
                          "Edit the wording / `feature` slugs, delete any that shouldn't ship, "
                          "then merge to publish."]
            if skipped:
                body_lines += ["", "<details><summary>Skipped as internal "
                               f"({len(skipped)})</summary>", ""]
                body_lines += [f"- #{n}" for n, _ in skipped]
                body_lines += ["", "</details>"]
            open_changelog_pr(changelog_repo, ctoken,
                              f"changelog/{repo_short}-release-{release_pr}",
                              files,
                              f"Changelog: {source_repo} release (#{release_pr})",
                              "\n".join(body_lines))
            return 0

    # SINGLE mode: a feature branch merged straight to main.
    pr = pr_data(source_repo, release_pr)
    meta = classify(style, source_repo, pr)
    print(f"classified: {json.dumps(meta)}")
    if SKIP_INTERNAL and not meta.get("publish", True):
        print(f"#{release_pr} judged internal-only; no PR opened (SKIP_INTERNAL)")
        return 0
    date = release_date or (pr["merged_at"] or "")[:10]
    body = (f"Auto-drafted from {source_repo}#{release_pr}.\n\n"
            f"**Feature:** `{meta['feature']}` · **Area:** {meta['area']} · "
            f"**Category:** {meta['category']}\n\n> {meta['entry']}\n\n"
            "Review the wording and the `feature` slug, then merge to publish. "
            "Close this PR if the change should not appear in the changelog.")
    open_changelog_pr(changelog_repo, ctoken,
                      f"changelog/{repo_short}-{release_pr}",
                      [(entry_path(meta, repo_short, release_pr),
                        render_entry(meta, repo_short, release_pr, date))],
                      f"Changelog: {source_repo}#{release_pr}", body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
