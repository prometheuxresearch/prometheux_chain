from ..client.JarvisClient import JarvisClient
from .Ontology2Databases import Ontology2Databases
from .Bind import Bind
from .BindTable import BindTable
from ..logic.Ontology import Ontology
from ..model.Datasource import Datasource
from typing import List
from ..model.DatabaseInfo import DatabaseInfo

def bind_input(ontology : Ontology, databases : List[DatabaseInfo]):
    databases_ids = []
    for database in databases:
        databases_ids.append(database.id)
    ontology2Databases = Ontology2Databases(ontology, databases_ids)
    potential_bindings = JarvisClient.get_potential_bindings(ontology2Databases).json()["data"]

    bindings_obj = []
    for bind in potential_bindings:
        bind = Bind.from_dict(bind)
        bindings_obj.append(bind)
    return BindTable(bindings_obj)

# future implementation consider output database
def bind_output(ontology : Ontology, databases=None):
    #databases_ids = []
    #for database in databases:
    #    databases_ids.append(database.id)
    #ontology2Databases = Ontology2Databases(ontology, databases_ids)
    #potential_bindings = JarvisClient.get_potential_bindings(ontology2Databases).json()["data"]

    #bindings_obj = []
    #for bind in potential_bindings:
    #    bind = Bind.from_dict(bind)
    #    bindings_obj.append(bind)
    intensional_predicates = ontology.intensionalPredicates
    intensional_bindings = []
    for intensional_predicate in intensional_predicates:
        intensional_bindings.append(Bind(None, intensional_predicate.name, "", Datasource(name="None")))
    return BindTable(intensional_bindings)


def select_bindings(bind_table : BindTable, bind_indexes):
    selected_bindings = []
    bind_indexes = set(bind_indexes)
    for i in bind_indexes:
        selected_bindings.append(bind_table.get(i))
    return BindTable(selected_bindings)
