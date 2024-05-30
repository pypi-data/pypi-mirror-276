import base64
from importlib import resources


class Visualisation:
    def __init__(self, width, height, template="d3v6.html", background="white"):
        self._width = width
        self._height = height
        if template:
            self.html = resources.read_text("py3js", template)
            self.html = (self.html
                             .replace("$width", str(width))
                             .replace("$height", str(height)))

        self.style = f"svg {{background-color: \"{background}\"; }}"
        self.script = ""

    def add_script(self, line: str):
        self.script += "\n"
        self.script += line

    def add_style(self, line: str):
        self.style += "\n"
        self.style += line

    def _render_data(self):
        data = (self.html
                .replace("$style", self.style)
                .replace("$script", self.script))
        return data

    def _repr_html_(self):
        data = self._render_data()
        b64data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        url = f"data:text/html;charset=utf-8;base64,{b64data}"
        return f"<iframe src=\"{url}\" width=\"{self._width}\" height=\"{self._height}\" scrolling=\"no\" style=\"border:none !important;\"></iframe>"

    def save(self, path: str):
        with open(path, "w") as writer:
            writer.write(self._render_data())
