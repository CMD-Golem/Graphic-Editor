from controller_view import *
from drawing_view import *
from tree_view import *
from shapes import *
from observer import *



m = Model()
c = Closer()

tree = Tree(m, c)
controller = Controller(m, c, tree)
drawing = Drawing(m, c)

 
# ################################################################
root = m.root
cm1 = Group(300, 1, 1)
cm2 = Group(1, 1, 2)
cm21 = Group(1, 1, 3)

root.add(cm1)
cm1.add(Circle(1, 1, 50, "blue", 4))
cm1.add(Circle(100, 1, 80, "blue", 5))
cm1.add(Circle(50, 150, 20, "blue", 6))

root.add(cm2)
cm2.add(cm21)

cm21.add(Rectangle(1, 1, 20, 20, "red", 7))
cm21.add(Rectangle(100, 1, 50, 50, "red", 8))

cm2.add(Rectangle(1, 1, 30, 80, "green", 9))
cm2.add(Rectangle(200, 50, 100, 50, "green", 10))

root.add(Rectangle(100, 200, 30, 80, "yellow", 11))

root.strRecursive()

m.notify_observers()

drawing.run()
controller.run()
tree.run()