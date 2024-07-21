from ..client.JarvisClient import JarvisClient
from ..model.PageResponse import PageResponse

class ReasoningResult:
    def __init__(self, output_predicate, knowledge_graph_id, page=-1, size=50, sort_property="fact", asc=True):
        self.output_predicate = output_predicate
        self.knowledge_graph_id = knowledge_graph_id
        self.page = page
        self.size = size
        self.sort_property=sort_property
        self.asc = asc

    def to_dict(self):
        return {
            'output_predicate': self.output_predicate,
            'knowledge_graph_id': self.knowledge_graph_id,
            'page': self.page,
            'size': self.size,
            'sort_property' : self.sort_property,
            'asc' : self.asc
        }
    
    def get(self):
        if self.page < 0:
            self.page = 0
        chase_facts_response = JarvisClient.get_chase_facts(self.output_predicate, self.knowledge_graph_id, self.page,self.size,self.sort_property,self.asc)
        if chase_facts_response.status_code != 200:
            raise Exception(f"HTTP error! status: {chase_facts_response.status_code}, detail: {chase_facts_response.text}")
        if chase_facts_response.status_code == 200:
            page = PageResponse.from_dict(chase_facts_response.json()["data"])
        return page

    def next(self):
        self.page += 1
    
    def prev(self):
        self.page -= 1
    
    def set_page_size(self, new_page_size):
        self.size = new_page_size

    def set_size(self, new_page):
        self.page = new_page
