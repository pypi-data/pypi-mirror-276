import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.backend_bases import MouseButton
from cdt_path.pathplan import *
from . import border
class Interact:
	def __init__(self, ax, triang, title=True):
		self.ax = ax
		self.triang = triang
		self.trifinder = triang.get_trifinder()
		
		self._click_state=0
		self._start_point=None
		self._end_point=None
		
		with mpl.rc_context({'lines.linewidth':2, 'lines.linestyle': ':'}):
			plt.triplot(triang)
			
		self.polygon = Polygon([[0, 0], [0, 0]], facecolor='#ADD8E6',alpha = 0.6)  # dummy data for (xs, ys)
		self.update_selected_tri(-1)
		ax.add_patch(self.polygon)
		fig = plt.gcf()
		if title:
			if title == True:
				self.on_mouse_move = self.on_mouse_move_t
			else:
				ax.set_title(title)
		else:
			self.on_mouse_move = self.on_mouse_move_wt
			
		fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
		plt.connect('button_press_event', self.on_click)
		ax.axes.set_aspect('equal')
		ax.axis("off")
		plt.show()
		
		
	def update_selected_tri(self, tri):
		if tri == -1:
			points = [0, 0, 0]
		else:
			points = self.triang.triangles[tri]
		xs = self.triang.x[points]
		ys = self.triang.y[points]
		self.polygon.set_xy(np.column_stack([xs, ys]))

	def on_mouse_move_wt(self, event):
		if event.inaxes is None:
			tri = -1
		else:
			tri = self.trifinder(event.xdata, event.ydata)
		self.update_selected_tri(tri)
		event.canvas.draw()
		
	def on_mouse_move_t(self, event):
		if event.inaxes is None:
			tri = -1
		else:
			tri = self.trifinder(event.xdata, event.ydata)
		self.update_selected_tri(tri)
		self.ax.set_title(f'In triangle {tri}')
		event.canvas.draw()
		
	def updata_path(self, start_point, end_point):
		start = int(self.trifinder(*start_point))
		goal = int(self.trifinder(*end_point))
		came_from, cost_so_far = a_star_search_G(self.triang, start, goal)
		L=[goal]
		val = came_from[goal]
		
		while val != start:
			L.append(val)
			val = came_from[val]
			
		Ll, Lr, Li=tri_to_funnel_plus(self.triang, start, L)
		Ll.reverse()
		Px = self.triang.x[Lr]
		Py = self.triang.y[Lr]
		Pr = np.column_stack((Px, Py))
		Pr = np.concatenate((Pr, [end_point]))
		Px = self.triang.x[Ll]
		Py = self.triang.y[Ll]
		Pl = np.column_stack((Px, Py))
		points = np.concatenate(([start_point], Pr, Pl))
		self.polygon2 = Polygon(points, closed = True, facecolor='#80FF00',alpha = 0.6)
		self.ax.add_patch(self.polygon2)
		
		Pl = np.concatenate((Pl[::-1], [end_point]))
		Ln = funnel(start_point, Pl, Pr, Li)
		Ln = [start_point] + Ln + [end_point]
		Ln_np = np.array(Ln)
		plt.plot(Ln_np[:,0],Ln_np[:,1],lw=3)
		
	def on_click(self, event):
		if event.inaxes is None or self.trifinder(event.xdata, event.ydata) == -1:
			return
		if event.button is MouseButton.LEFT:
			if self._click_state==0:
				self._start_point=(event.xdata, event.ydata)
				self._start_point_in_axes = self.ax.scatter(event.xdata, event.ydata, color='k', marker='*')
				self._click_state+=1
				
			elif self._click_state==1:
				self._end_point=(event.xdata, event.ydata)
				self._start_point_in_axes.remove()
				if self.trifinder(*self._start_point) == self.trifinder(*self._end_point):
					self._click_state==0
					return
				self.updata_path(np.array(self._start_point), np.array(self._end_point))
				self._click_state+=1
			elif self._click_state ==2:
				self.polygon2.set_visible(False)

				self._click_state=0
				