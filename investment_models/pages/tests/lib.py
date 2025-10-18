def unzip_names(zip):
    return [x[0] for x in zip]

class FormData(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
    
    def items(self):
        for name, value in self.__dict__.items():
            yield name, value
