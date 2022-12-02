class BoundsException(Exception):
    def __init__(self):
        self.message = "Stock exceeded transaction bounds"
        super().__init__(self.message)
