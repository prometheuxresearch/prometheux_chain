from .api import pmtx_for_rag, fetch_explanation

def main():
    nl_query = "Which diseases could Alitretinoin treat?"
    results = pmtx_for_rag(nl_query)
    print(results)

    factToExplain = "potentiallyTreats(Alitretinoin,psoriasis,6)"
    explanation_result = fetch_explanation(factToExplain)
    print(explanation_result)

if __name__ == "__main__":
    main()
