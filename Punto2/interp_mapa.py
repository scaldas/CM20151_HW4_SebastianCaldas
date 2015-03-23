from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import NearestNDInterpolator
import os

print('Para poder trabajar, es necesario descargar el archivo de datos. Este sera eliminado despues.')
os.system('wget ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis.derived/surface/air.mon.ltm.nc')

my_nc_file = 'air.mon.ltm.nc'
fh = Dataset(my_nc_file, mode='r')

lats = fh.variables['lat'][:]
lons = fh.variables['lon'][:]
airs = fh.variables['air'][:]

units = fh.variables['air'].units
fh.close()

print('***********************************************')
print('La dinamica de este punto es la siguiente: ')
print('El algoritmo ira mostrando las graficas y los comentarios en el orden en que los pide el enunciado')
print('Para poder continuar, deberas cerrar las graficas que haya abiertas.')
mean_temps = []
for i in range(0, airs.shape[1]): #lat
	mean_temps.append([])
	for j in range(0, airs.shape[2]): #lon
		mean_temps[i].append(0.0)
		for k in range(0, airs.shape[0]):
			mean_temps[i][j] += airs[k][i][j]
		mean_temps[i][j] = mean_temps[i][j]/12

mean_temps = np.asarray(mean_temps)


plt.figure(figsize=(12,8))

m = Basemap(projection='ortho', lat_0=10, lon_0=90)

lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

cs = m.pcolor(xi,yi,mean_temps)
m.drawcoastlines()
parallels = np.arange(0.,81,10.)

cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('Temperature (' + units + ')')

plt.title('Mean Temperature')

plt.figure(figsize=(12,8))
m1 = Basemap(projection='ortho', lat_0=10, lon_0=-90)

xi, yi = m1(lon, lat)

cs = m1.pcolor(xi,yi,mean_temps)
m1.drawcoastlines()
parallels = np.arange(0.,81,10.)

cbar = m1.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(units)

plt.title('Mean Temperature')

print('***********************************************')
print('Las primeras graficas son entonces de las temperaturas medias del aire usando Basemap.')
print('Se presentan dos para obtener una vision mas amplia del mundo ;)')
print('Para continuar, debes cerrar las dos.')

plt.show( )

print('***********************************************')
print('Ahora haremos la interpolacion')

my_nc_file = 'air.mon.ltm.nc'
fh = Dataset(my_nc_file, mode='r')

lats = fh.variables['lat'][:]
lons = fh.variables['lon'][:]
airs = fh.variables['air'][:]

units = fh.variables['air'].units

mean_temps = []
for i in range(0, airs.shape[1]): #lat
	mean_temps.append([])
	for j in range(0, airs.shape[2]): #lon
		mean_temps[i].append(0.0)
		for k in range(0, airs.shape[0]):
			mean_temps[i][j] += airs[k][i][j]
		mean_temps[i][j] = mean_temps[i][j]/12

mean_temps = np.asarray(mean_temps)
lon, lat = np.meshgrid(lons, lats)

points = np.array([lat,lon]).T
points_unpacked = []

for i in range(0, len(points)):
	for j in range(0, len(points[i])):
		points_unpacked.append(points[i][j])

points_unpacked = np.asarray(points_unpacked)

squeeshy = []
for i in range(0,len(mean_temps[0])):
	for j in range(0, len(mean_temps)):
		squeeshy.append(mean_temps[j][i])

squeeshy = np.asarray(squeeshy)
nearest = NearestNDInterpolator(points_unpacked,squeeshy)

x_int = np.sort(np.linspace(lats[0],lats[-1],100))
y_int = np.sort(np.linspace(lons[0],lons[-1],100))
x_int,y_int = np.meshgrid(x_int, y_int)
z_int = nearest(x_int, y_int)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x_int, y_int, z_int, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
fcb = fig.colorbar(surf, shrink=0.5, aspect=5)
fcb.set_label("Foo", labelpad=-1)

ax.plot_wireframe(lat, lon, mean_temps, rstride=10, cstride=10, color='k')

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))


print('!Juega con la grafica! A veces no se ve la grilla (que corresponde a la funcion original). La superficie es la interpolacion "nearest-neighbours"')
print('Cierra la grafica para ver los comentarios finales.')
plt.show()
print('***********************************************')
print('La interpolacion "nearest-neighbours" resulto ser bastante cercana a la funcion original, o aunque sea asi pareciera a simple vista.')
print('Tal y como su nombre lo indica, este tipo de interpolacion solo usa los valores de los puntos mas cercanos al que se quiere averiguar, o incluso aproxima al valor de solo el mas cercano!')
print('Al reducir el numero de puntos a evaluar en cada iteracion (incluso llegando a uno solo), el algoritmo es bastante eficiente computacionalmente')
print('Tal vez por esto es que la funcion usada, NearestNDInterpolator, no aconseja una dimension maxima, tal y como lo hacen sus homologas en su documentacion')
print('En particular, "interp2d", dedicada solo a dos dimensiones, reconoce ser ineficiente para grillas irregulares')
print('El algoritmo de vecinos cercanos es entonces un "workaround" a la maldicion de la dimensionalidad, pues su complejidad seria relegada a entontrar tal vecino cercano.')
print('Una heuristica ayudaria. Y si se relaja la condicion de aproximar al MAS cercana, la maldicion de la dimensionalidad se veria bastante reducida.')
os.system('rm air.mon.ltm.nc')
