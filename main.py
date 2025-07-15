from controller_view import *
from drawing_view import *
from tree_view import *
from shapes import *
from observer import *



m = Model()
c = Closer()

controller = Controller(m, c)
drawing = Drawing(m, c)
tree = Tree(m, c)

root = m.root

root.add(Circle(10, 30, 40, "black"))
root.add(Rectangle(45, 90, 40, 60, "red"))

g2 = Group(100, 200)

g2.add(Circle(0, 0, 100, "green"))
g2.add(Rectangle(175, 85, 50, 50, "blue"))

root.add(g2)




m.draw(drawing.canvas)
controller.loadFigures()
tree.loadFigures()

print(root.strRecursive(0))

drawing.run()
controller.run()
tree.run()