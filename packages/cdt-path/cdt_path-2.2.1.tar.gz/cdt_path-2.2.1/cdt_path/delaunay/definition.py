import numpy as np
import matplotlib.pyplot as plt
from .incremental import *
class Delaunay:
	def __init__(self,points,sorted=False):
		if sorted:
			self.points=points
		else:
			self.points=points[np.lexsort((points[:, 1], points[:, 0]))]
		self.sorted=True
		self.create()
	# def create(self):
	# 	self.L_neighbor=Create_DT_incremental(self.points)
		
	# def create_Sorted_Sorted(self):
	# 	self.L_neighbor=Create_DT_incremental_Sorted(self.points)
		
	def create(self):
		self.L_ch_i,self.D_tri=Create_DT_incremental_Sorted(self.points)
		
	# def create_Sorted(self):
	# 	self.L_ch_i,self.D_tri=Create_DT_incremental_Sorted(self.points)
		
	def show(self):
		# for i_a,i_b in self.S_segment:
		# 	a=self.points[i_a]
		# 	b=self.points[i_b]
		# 	plt.plot([a[0],b[0]],[a[1],b[1]])
		# plt.figure(figsize=(8, 6))
		for key1,key2 in self.D_tri:
			if key1>key2:
				plt.plot([self.points[key1][0],self.points[key2][0]],[self.points[key1][1],self.points[key2][1]],
				# color = 'cyan',
				color = '#1f77b4',
				)
		
	# def prepare_for_show(self):
	# 	self.S_segment={}
	# 	i=0
	# 	while i<len(self.points):
	# 		self.S_segment.add(set(i,l) for l in self.S_neighbor)
	# 		i+=1