class singleton(type):
    _instances = {}
    _name = ''
    _bases = {}
    _attrs = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._name = name
        cls._bases = bases
        cls._attrs = attrs

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
