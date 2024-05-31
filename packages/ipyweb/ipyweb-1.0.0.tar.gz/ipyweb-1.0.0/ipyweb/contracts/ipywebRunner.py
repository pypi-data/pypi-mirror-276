class ipywebRunner():
    def __init__(self):
        if not hasattr(self, 'run'):
            raise TypeError(f"必须实现run方法")
