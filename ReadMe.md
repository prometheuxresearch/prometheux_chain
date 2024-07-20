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
   source venv/bin/activate
   pip3 install -r requirements.txt
```

To manually install the library in your Jupyter Lab or Jupyter Notebook follows these steps
```bash
   python3 -m venv myenv
   source venv/bin/activate
   pip install -e .
   rm -r myenv/lib/python3.x/site-packages/prometheux_chain/
   cp -r ../prometheux_chain myenv/lib/python3.x/site-packages
   jupyter lab
```

Ensure that the services Constellation and Jarvis are active
