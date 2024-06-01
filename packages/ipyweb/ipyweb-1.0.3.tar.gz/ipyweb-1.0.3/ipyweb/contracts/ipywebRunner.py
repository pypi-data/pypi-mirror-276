class ipywebRunner():
    def __init__(self):
        if not hasattr(self, 'run'):
            raise TypeError(f"The run method must be implemented")
