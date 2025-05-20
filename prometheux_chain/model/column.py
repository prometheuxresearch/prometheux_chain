class Column:
    def __init__(self, name: str, type: str=None, position: int=None, nullable: bool = True):
        self.name = name
        self.type = type
        self.position = position
        self.nullable = nullable

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "position": self.position,
            "nullable": self.nullable
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["type"], data["position"], data["nullable"])
