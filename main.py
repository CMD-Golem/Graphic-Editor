from controller_view import *
from drawing_view import *
from tree_view import *
from shapes import *
from observer import *



m = Model()
c = Closer()

tree = Tree(m, c)
controller = Controller(m, c)
drawing = Drawing(m, c)


root = m.root

root.add(Circle(10, 30, 40, "black"))
root.add(Rectangle(45, 90, 40, 60, "red"))

g2 = Group(100, 200)

g2.add(Circle(0, 0, 100, "green"))
g2.add(Rectangle(175, 85, 50, 50, "blue"))

root.add(g2)


#print(root.strRecursive(0))

m.root.draw(drawing.canvas)
m.notify_observers(None)


drawing.run()
controller.run()
tree.run()