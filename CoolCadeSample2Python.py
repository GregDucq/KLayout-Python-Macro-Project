
# Enter your Python code here

import pya

# Creates a list of points from a list of tuples of DBU adjusted points
def create_new_points(points, inital, spacing, iteration, dbu):
  new_points = []
  
  for (x,y) in points:
    
    n_x = (x + (-1 if x < 0 else 1) * ((2 + initial) * (iteration + 1) + spacing * (iteration * (iteration + 1) / 2))) / dbu
    n_y = (y + (-1 if y < 0 else 1) * ((2 + initial) * (iteration + 1) + spacing * (iteration * (iteration + 1) / 2))) / dbu
    
    new_points.append(pya.Point(n_x, n_y))
  
  return new_points
  
# fetches current layout view and cell view
cv = pya.CellView.active()
ly = cv.layout()
dbu = ly.dbu # dbu so we can convert the coordinates we get from klayout to points on the layout that can then be edited

inputd= pya.InputDialog

# Get the desired requirements from the user
iterations = inputd.ask_int("Iterations", "Enter the number of new boxes to generate", 0)
initial = inputd.ask_int("Initial Spacing", "Enter the initial spacing between the innermost two boxes", 0)
spacing = inputd.ask_int("Spacing", "Enter the amount by which spacing between subsequent boxes will increase", 0)

# Fail if any of the inputed values are invalid (None or negative values are invalid)
if ((iterations == None or iterations < 0) or (initial == None or initial < 0) or (spacing == None or spacing < 0)):
  pya.MessageBox.warning("Invalid Input", "One or more values were not inputted or were negative. Exiting macro immediately.", pya.MessageBox.Ok)

# Otherwise, continue:
else:
  cell =  ly.cell("test")
  rect_points = []
  
  # Find the simple polygon box in the cell
  for shape in cell.shapes(ly.layer(1, 0)).each():
    if(shape.is_simple_polygon()):
      print("Getting polygon")
      for point in shape.simple_polygon.each_point():
        rect_points.append(((point.x * dbu),(point.y * dbu)))
  
  # Generate each box using the coordinates of the points for the original box
  for i in range(iterations):
    points = create_new_points(rect_points, initial, spacing, i, dbu)
    cell.shapes(ly.layer(1, 0)).insert(pya.SimplePolygon(points))
    