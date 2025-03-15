class Brush:
    def __init__(self, tool, shape, size, color):
        self.current_tool = tool
        self.current_shape = shape
        self.tool_size = size
        self.selected_color = color
        self.text = None
        self.font = None
        self.styles = None
        self.current_point = [0, 0]
        self.last_point = [0, 0]

    def set_tool(self, value):
        self.current_tool = value

    def set_shape(self, value):
        self.current_shape = value

    def set_tool_size(self, value):
        self.tool_size = int(value)

    def set_text(self, value):
        self.text = str(value)

    def set_font(self, value):
        self.font = value

    def set_styles(self, value):
        self.styles = value
    
    def set_color(self, value):
        self.selected_color = value

    def set_current_point(self, x, y):
        self.current_point = [x, y]
    
    def set_last_point(self, x, y):
        self.last_point = [x, y]