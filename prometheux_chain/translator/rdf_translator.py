import os
from ..client.jarvispy_client import JarvisPyClient


def translate_from_rdf(rdf_file_path):
    with open(rdf_file_path, 'r') as file:
        rdf_data = file.read()
    response = JarvisPyClient.translate_from_rdf(rdf_data)

    if response.status_code == 200:
        vadalog_data = response.json()['data']['vadalog']
        if vadalog_data:
            with open(os.path.join(os.path.dirname(rdf_file_path), 'from_rdf.vada'), 'w') as file:
                file.write(vadalog_data)
        else:
            raise Exception(f"Failed to translate from RDF: {response.json()}")
    else:
        raise Exception(f"Failed to translate from RDF: {response.json()}")