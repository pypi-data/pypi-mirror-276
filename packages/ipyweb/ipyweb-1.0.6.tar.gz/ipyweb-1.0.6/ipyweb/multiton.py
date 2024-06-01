class multiton(type):
    _name = ''
    _bases = {}
    _attrs = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._name = name
        cls._bases = bases
        cls._attrs = attrs
