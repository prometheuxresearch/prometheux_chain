class Pagination:
    def __init__(self, sort, page_number, page_size, offset, paged, unpaged):
        self.sort = sort
        self.page_number = page_number
        self.page_size = page_size
        self.offset = offset
        self.paged = paged
        self.unpaged = unpaged
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            sort=data['sort'],
            page_number=data['pageNumber'],
            page_size=data['pageSize'],
            offset=data['offset'],
            paged=data['paged'],
            unpaged=data['unpaged']
        )
