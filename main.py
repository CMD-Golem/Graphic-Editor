from controller_with_table import *
from drawing_view import *
from shapes import *
from observer import *



m = Model()
c = Closer()

controller = Controller(m, c)
drawing = Drawing(m, c)

# ################################################################
root = m.root
cm1 = Composite(300, 1, 1)
cm2 = Composite(1, 1, 2)
cm21 = Composite(1, 1, 3)

root.add_component(cm1)
cm1.add_component(Circle(1, 1, 50, "blue", 4))
cm1.add_component(Circle(100, 1, 80, "blue", 5))
cm1.add_component(Circle(50, 150, 20, "blue", 6))

root.add_component(cm2)
cm2.add_component(cm21)

cm21.add_component(Rectangle(1, 1, 20, 20, "red", 7))
cm21.add_component(Rectangle(100, 1, 50, 50, "red", 8))

cm2.add_component(Rectangle(1, 1, 30, 80, "green", 9))
cm2.add_component(Rectangle(200, 50, 100, 50, "green", 10))

root.add_component(Rectangle(100, 200, 30, 80, "yellow", 11))

root.print_descriptor()

drawing.run()
controller.run()