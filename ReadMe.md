# Prometheux_chain

## Description
Prometheux_chain is a Python SDK designed to your knowledge graphs by 
- ingesting a constellation of datasources from every kind of databases and files, 
- performing reasoning on it and augment it with the new derived knowledge
- providing the explanations of the results.

## Installation

### Requirements
- Python 3.7 or higher

## Installation

1. Clone the repository.
2. Create a virtual environment and install dependencies:

```bash
   python3 -m venv myvenv
   source myvenv/bin/activate
   pip3 install -r requirements.txt
```

To automatically install the library in your Jupyter Lab or Jupyter Notebook run the following command
```bash
    pip install git+https://github.com/prometheuxresearch/prometheux_chain.git
```

To manually install the library in your Jupyter Lab or Jupyter Notebook follows these steps
```bash
   python3 -m venv myenv
   source myvenv/bin/activate
   pip install -e .
   rm -r myenv/lib/python3.x/site-packages/prometheux_chain/
   cp -r ../prometheux_chain myenv/lib/python3.x/site-packages
   jupyter lab
```

Ensure that the services Constellation and Jarvis are active


### Usage
The following sections describe the steps to use the SDK, from connecting to databases to obtaining explanations of reasoning results.

## Connecting to Databases
Load database configurations from a YAML file. This step initializes the connection settings without migrating any data:

```bash
import prometheux_chain as pmtx

databases = pmtx.connect_from_yaml("databases.yaml")
```

## Compiling Ontology from Vadalog
Compile an ontology from a Vadalog file and display its rules:

```bash
ontology = pmtx.compile_vadalog("file.vada")
ontology.show_rules()
```

## Binding Inputs
Identify and display compatible bindings between data sources and input predicates:

```bash
potential_input_bindings = pmtx.bind_input(ontology, databases)
potential_input_bindings.show()
```

## Selecting Input Bindings
Select specific bindings from the list of compatible ones:

```bash
selected_input_bindings = pmtx.select_bindings(potential_input_bindings, {0})
```

## Binding Outputs
Identify and display compatible bindings between data sources and output predicates:

```bash
potential_output_bindings = pmtx.bind_output(ontology)
potential_output_bindings.show()
```

## Selecting Output Bindings
Choose specific output bindings from the compatible ones:
```bash
selected_output_bindings = pmtx.select_bindings(potential_output_bindings, {2})
```

## Reasoning
Execute a reasoning task using the selected ontology and bindings, with an option to enable explainability:

```bash
reasoning_task = pmtx.reason(ontology, selected_input_bindings, selected_output_bindings, for_explanation = True)
```

## Displaying Paginated Reasoning Results
Retrieve and display paginated results from the reasoning task, specifying page number and size:

```bash
paginated_results = reasoning_task.get(new_page = 0, new_page_size = 100)
paginated_results.show()
```

## Generating Textual Explanations
Generate and display textual explanations for a selected result, using a predefined glossary:

```bash
pmtx.explain(paginated_results.get(0), json_glossary="glossary.json")
```