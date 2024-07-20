from .Pagination import Pagination
from ..logic.Fact import Fact
import pandas as pd
from IPython.display import display

class PageResponse:
    def __init__(self, content, pagination, total_pages, total_elements, last, size, number, sort, number_of_elements, first, empty):
        self.content = [Fact.from_dict(fact) for fact in content]
        self.pagination = Pagination.from_dict(pagination)
        self.total_pages = total_pages
        self.total_elements = total_elements
        self.last = last
        self.size = size
        self.number = number
        self.sort = sort
        self.number_of_elements = number_of_elements
        self.first = first
        self.empty = empty
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            content=data['content'],
            pagination=data['pageable'],
            total_pages=data['totalPages'],
            total_elements=data['totalElements'],
            last=data['last'],
            size=data['size'],
            number=data['number'],
            sort=data['sort'],
            number_of_elements=data['numberOfElements'],
            first=data['first'],
            empty=data['empty']
        )
    
    def get(self, index):
        return self.content[index]
    
    def show(self, max_rows=None, max_colwidth=None):
        # Create a DataFrame from the rules
        data = [{
            'Fact': fact.fact,
        } for fact in self.content]
        
        df = pd.DataFrame(data)

        pd.set_option('display.max_rows', max_rows)
        pd.set_option('display.max_columns', max_colwidth)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('display.max_colwidth', None)
        display(df)
