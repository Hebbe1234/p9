class Demand:
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target
        self.size = 2

    def __str__(self):
        return f"{self.source} => {self.target}"
    
    def __repr__(self):
        return str(self)