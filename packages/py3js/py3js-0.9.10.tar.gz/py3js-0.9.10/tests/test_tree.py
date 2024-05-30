from py3js.tree import Tree, Node, TreeKind

save_path = "c:\\tmp\\1.html"


def test_radial():
    root = Node("programming", [
        Node("C++"),
        Node("Python"),
        Node("C#"),
        Node("Scala")
    ])

    t = Tree(root, TreeKind.RADIAL_TIDY)
    t.save(save_path)


def test_normal():
    root = Node("programming", [
        Node("C++", color="blue"),
        Node("Python"),
        Node("C#"),
        Node("Scala")
    ])

    t = Tree(root, TreeKind.TIDY,
             color="red",
             stroke_width=0.5,
             font_size=20)
    t.save(save_path)
