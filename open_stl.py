import vtkplotlib as vpl
from stl.mesh import Mesh
import sys


# Load path and name of STL
path = str(sys.argv[1])
name = str(sys.argv[2])

# Read the STL using numpy-stl
mesh = Mesh.from_file(path)

# Plot the mesh
vpl.mesh_plot(mesh)

# Show Text with beam- and block-name
vpl.text(name,fontsize=14, color='black')

# Show the figure
vpl.show()