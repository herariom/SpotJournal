class SongData():

    def __init__(self, legend, values, color_r, color_g, color_b):
        self.legend = legend
        self.values = values
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b

    legend: str
    values: list
    color_r: int
    color_g: int
    color_b: int
