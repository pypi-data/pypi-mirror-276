from . import pathplan
from . import manipulate
from . import convex_hull
from . import delaunay

from .file import *
from triangle import triangulate as _triangulate
from .interact.base import Interact
from .interact import border
from matplotlib.tri import Triangulation as _Triangulation
from .circumcircle.calculate import circumcircle

def triangulate(tri, opts = 'p'):
	return _triangulate(tri, opts)
	
def Triangulation(tri, opts = 'p'):
	cc = _triangulate(tri, opts)
	return _Triangulation(cc['vertices'][:,0],cc['vertices'][:,1],cc['triangles'])
	
# __all__=["voronoi",'convex_hull','delaunay']