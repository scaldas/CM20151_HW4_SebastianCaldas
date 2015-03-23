# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import pylab as pili
import datetime
import numpy as np
from scipy.interpolate import interp1d, splrep, splev 
from scipy.stats import chisquare as csquare
import csv
import copy
from random import randint

def concatenar_mensaje(city, util):
	mensaje = 'Para los datos de ' + city + ' se encontro que los mejores metodos de interpolacion fueron: ' + ', '.join(util)
	return mensaje

def print_interpolations(city):
    ff = open('temperaturas.csv', 'rt')
    reader = csv.reader(ff)

    dates = []
    hash_temperaturas = {}
    
    for row in reader:
        if row[4] == city and float(row[3]) != 999.9:
            date = datetime.datetime.strptime(row[5],"%Y-%m-%d")
            dates.append(date)
            hash_temperaturas[date] = float(row[3])  

    dates = np.sort(dates)

    temperaturas = []
    for each in dates:
        temperaturas.append(hash_temperaturas[each])

    dates = matplotlib.dates.date2num(dates)
    x_l = np.linspace(dates[0],dates[-1],10000)

    f_l = interp1d(dates, temperaturas, kind=1)
    y_l=f_l(x_l)

    f_pol = interp1d(dates, temperaturas, kind=2)
    y_pol=f_pol(x_l)

    tck = splrep(dates, temperaturas, k=3)
    y_spl = splev(x_l, tck)

    plt.figure(figsize=(12,8))
    plt.subplot(3, 1, 1)
    plt.plot_date(x_l, y_l, '-b', c='r')
    plt.plot_date(dates, temperaturas, 'o')
    plt.title('Temperaturas ' + city)
    plt.ylabel(u"Temeperatura (ºC)")
    plt.legend(['linear interpolation','data'])

    plt.subplot(3, 1, 2)
    plt.plot_date(x_l, y_pol, '-b', c='g')
    plt.plot_date(dates, temperaturas, 'o')
    plt.ylabel(u'Temperatura(ºC)')
    plt.legend(['quadratic interpolation', 'data'])

    plt.subplot(3, 1, 3)
    plt.plot_date(x_l, y_spl, '-b', c='k')
    plt.plot_date(dates, temperaturas, 'o')
    plt.xlabel('Fecha')
    plt.ylabel(u'Temperatura(ºC)')
    plt.legend(['quadratic splines', 'data'])

    pili.savefig('Interpolaciones-' + city + '.png', bbox_inches='tight')
    
    util = ['lineal', 'pol. cuadrado', 'splines grado 3']
    for i in range(0,10):
        dates_new = copy.copy(dates)
        temperaturas_new = copy.copy(temperaturas)
        number = int(len(dates_new)/3)
        for i in range(0,number):
            rand = randint(1,len(dates_new)-2)
            dates_new = np.delete(dates_new,rand)
            temperaturas_new.pop(rand)
        f_l = interp1d(dates_new, temperaturas_new, kind=1)
        f_pol2 = interp1d(dates_new, temperaturas_new, kind=2)
        tck = splrep(dates_new, temperaturas_new, k=3)
        temperaturas_2 = np.asarray(temperaturas)
        if csquare(f_l(dates),temperaturas_2)[1] < 0.5 and 'lineal' in util:
            util.remove('lineal')
        if csquare(f_pol2(dates),temperaturas_2)[1] < 0.5 and 'pol. cuadrado' in util:
            util.remove('pol. cuadrado')
        if csquare(splev(dates, tck), temperaturas_2)[1] < 0.5 and 'splines grado 3' in util:
            util.remove('splines grado 3')
    print(concatenar_mensaje(city, util))

print('Despues de varias pruebas exploratorias, se decide usar tres metodos de interpolacion: lineal, cuadratico y por splines de grado 3.')
print('La interpolacion cuadratica se escoge pues tiende a ser bastante diferente a las series de datos, permitiendo comprobar que el analisis estadistico posterior es efectivo.')
print('La interpolacion por splines de grado 3, por su parte, tiende a ser bastante parecida a una interpolacion cubica. Tener ambas parece redundante.')
print('Las interpolaciones se guardan como png.')
print('*****************************************************')
print_interpolations('Bogota')
print_interpolations('Cali')
print_interpolations('Barranquilla')
print_interpolations('Bucaramanga')
print_interpolations('Ipiales')
print('*****************************************************')
print('La escogencia de los metodos anteriores se basa en la prueba chi cuadrado con un nivel de significancia del 0.05 (es decir, con confianza del 95%).')
print('Se parte del supuesto que una buena interpolacion deberia predecir una cantidad de puntos considerable que se eliminen del conjunto incial.')
print('Es decir, si se elimina aleatoriamente una cantidad de los puntos iniciales, y con los restantes se interpola, deberia ser posible aproximar nuevamente aquellos puntos eliminados.')
print('Lo anterior se repite 10 veces eliminando un tercio de los puntos. Esto pues una buena interpolacion no deberia depender de aquellos puntos que se eliminen.')
print('Si una interpolacion falla la prueba en alguna ocasion, es descartada.')