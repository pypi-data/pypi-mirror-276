
import matplotlib.pyplot as plt
import numpy as np

def ToLeft(a,b,c):
	return a[0]*(b[1]-c[1])+a[1]*(c[0]-b[0])+b[0]*c[1]-c[0]*b[1]>0
	
def Qdet(a,b,c):
	return a[0]*(b[1]-c[1])+a[1]*(c[0]-b[0])+b[0]*c[1]-c[0]*b[1]
	
def LogLeft(a,b,c):
	O=Qdet(a,b,c)
	if O==0:
		return 0
	elif O>0:
		return 1
	return -1
def Convex_Hull_EE(P):
	l=len(P)
	i=0
	L=[]
	while i<l-1:
		j=i+1
		while j<l:
			k=0
			flag=2
			while k<l:
				if k==i or k==j:
					k+=1
					continue
				O=LogLeft(P[i],P[j],P[k])
				if O==0:
					k+=1
					continue
				if flag==2:
					flag=O
				elif flag!=O:
					break
				k+=1
			if k==l:
				if flag==1:
					L.append([P[i],P[j]])
				else:
					L.append([P[j],P[i]])
			j+=1
		i+=1
	return L
	
	
N=20
# 生成N个随机横坐标，范围在0到10之间  
X = 10 * np.random.rand(N)  
  
# 生成N个随机纵坐标，范围在0到5之间  
Y = 5 * np.random.rand(N)  
  
# 将X和Y组合成一个二维数组P，其中P[i][0]是X的第i个元素，P[i][1]是Y的第i个元素  
P = np.column_stack((X, Y))
plt.scatter(X,Y)
L=Convex_Hull_EE(P)
# print(L)
for edge in L:
	plt.plot([edge[0][0],edge[1][0]],[edge[0][1],edge[1][1]])
# line_x=[sublist[0] for sublist in L]
# line_y=[sublist[1] for sublist in L]
# plt.plot(line_x,line_y)
plt.show()