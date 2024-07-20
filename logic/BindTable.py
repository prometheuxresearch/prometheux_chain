import pandas as pd
from IPython.display import display
from ..exception.IndexOutOfBoundsError import IndexOutOfBoundsError
from ..logic.Bind import Bind
from typing import List

class BindTable:
    def __init__(self, bindings: List[Bind]):
        self.bindings = bindings

    def to_dict(self):
        return {'bindings': self.bindings}
    
    def get(self, index):
        try:
            return self.bindings[index]
        except IndexError:
            raise IndexOutOfBoundsError(f"Index {index} is out of bounds for bindings table.")
    
    def get_bindings(self):
        return self.bindings

    @classmethod
    def from_dict(cls, data):
        bind = cls(
            bindings=data['bindings']
        )

    def show(self, max_rows=None, max_colwidth=None):
        # Create a DataFrame from the rules
        data = [{
            'Predicate Name': bind.predicate_name,
            'Datasource Name': bind.datasource.name
        } for bind in (self.bindings)]
        
        df = pd.DataFrame(data)

        pd.set_option('display.max_rows', max_rows)
        pd.set_option('display.max_columns', max_colwidth)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('display.max_colwidth', None)
        display(df)


