from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pylab as pili
import csv

print('En este punto tuve varios problemas')
print('Por favor leer las anotaciones y tener piedad')
user_input = input("Si ya viste las anotaciones, oprime 1 o 0 segun quieras: ")

while int(user_input) != 1 and int(user_input) != 0:
	user_input = input("1 es para ver los graficos con las leyendas, pero no los guarda. 0 los guarda pero sin las leyendas: ")

guardar = (int(user_input) == 0)

f = open('top_300_rios.csv', 'r', encoding='latin-1')
lines = f.readlines();

plt.rcParams.update({'font.size': 10})

plt.figure(figsize=(12,8))
m = Basemap(projection='ortho', lat_0=20, lon_0=60)

m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='coral',lake_color='aqua')
m.drawrivers()
parallels = np.arange(0.,81,10.)

i = 1
while i < 151:
	info = lines[i].split(",")
	lon, lat = float(info[2]), float(info[3])
	xpt,ypt = m(lon,lat)
	m.plot(xpt,ypt, 'bo', markersize=5)
	if not guardar:
		plt.text(xpt,ypt-200000,info[1])
	i = i+1

if guardar:
	pili.savefig('rios1.png', bbox_inches='tight')

plt.figure(figsize=(12,8))
m1 = Basemap(projection='ortho', lat_0=10, lon_0=110)

m1.drawmapboundary(fill_color='aqua')
m1.fillcontinents(color='coral',lake_color='aqua')
m1.drawrivers()
parallels = np.arange(0.,81,10.)

i = 1
while i < 151:
	info = lines[i].split(",")
	lon, lat = float(info[2]), float(info[3])
	xpt,ypt = m1(lon,lat)
	m1.plot(xpt,ypt, 'bo', markersize=5)
	if not guardar:
		plt.text(xpt,ypt-200000,info[1])
	i = i+1

if guardar:
	pili.savefig('rios2.png', bbox_inches='tight')

plt.figure(figsize=(12,8))
m2 = Basemap(projection='ortho', lat_0=0, lon_0=-90)

m2.drawmapboundary(fill_color='aqua')
m2.fillcontinents(color='coral',lake_color='aqua')
m2.drawrivers()
parallels = np.arange(0.,81,10.)

i = 1
while i < 151:
	info = lines[i].split(",")
	lon, lat = float(info[2]), float(info[3])
	xpt,ypt = m2(lon,lat)
	m2.plot(xpt,ypt, 'bo', markersize=5)
	if not guardar:
		plt.text(xpt,ypt-200000,info[1])
	i = i+1

if guardar:
	pili.savefig('rios3.png', bbox_inches='tight')
	print('Graficos salvados exitosamente')
else: 
	plt.show()
