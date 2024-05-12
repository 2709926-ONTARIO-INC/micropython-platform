class MedianFilter:
    def __init__(self, window_size=15):
        self.window_size = window_size
        self.values = []
    
    def add_value(self, value):
        self.values.append(value)
        if len(self.values) > self.window_size:
            self.values.pop(0)
        return sorted(self.values)[len(self.values) // 2]
