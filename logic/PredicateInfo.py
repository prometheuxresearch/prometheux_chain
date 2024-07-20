class PredicateInfo:
    def __init__(self, name, num_args=0, args=None):
        self.name = name
        self.num_args = num_args
        self.args = args if args is not None else []

    def to_dict(self):
        return {
            'name': self.name,
            'numArgs': self.num_args,
            'args': self.args
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            num_args=data['numArgs'],
            args=data.get('args', [])
        )
