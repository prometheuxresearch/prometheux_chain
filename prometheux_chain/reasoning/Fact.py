class Fact:
    def __init__(self, predicate_name, arguments: list, column_names: list, column_types: list):
        self.predicate_name = predicate_name
        self.arguments = arguments
        self.column_names = column_names
        self.column_types = column_types

    def to_dict(self):
        return {
            'predicate_name': self.predicate_name,
            'arguments': self.arguments,
            'column_names': self.column_names,
            'column_types': self.column_types
        }

    def get_arg_by_column_name(self, column_name):
        if column_name in self.column_names:
            index = self.column_names.index(column_name)
            return self.arguments[index]
        else:
            raise ValueError(f"Column name {column_name} not found in {self.column_names}")

    def get_arg_by_pos(self, pos):
        if 0 <= pos < len(self.arguments):
            return self.arguments[pos]
        else:
            raise IndexError("Position out of range")

    def get_column_names(self):
        return self.column_names

    def get_column_types(self):
        return self.column_types
    
    def __str__(self):
        args_str = '|'.join(map(str, self.arguments))
        return f"{self.predicate_name}({args_str})"

    def __repr__(self):
        return self.__str__()

            
