import re
import numpy as np
from collections import defaultdict
import csv
import os

def procesar_info(info):
	antes = ''
	upper = ''
	despues = ''
	n = 0
	while not info[n].isupper():
		if(len(antes) == 0):
			antes = info[n]
		else:
			antes += (' ' + info[n])
		n = n+1
	upper = info[n]
	despues = ' '.join(info[n+1:])
	return [antes] + [upper] + [despues]

print('Para poder trabajar, es necesario descargar el archivo de datos correspondiente. Este se eliminara despuesself.')
os.system('wget http://www.cgd.ucar.edu/cas/catalog/surface/dai-runoff/coastal-stns-byVol-updated-oct2007.txt')
os.system('mv coastal-stns-byVol-updated-oct2007.txt info_rios_temp.txt')

ff = open("info_rios_temp.txt", "r", encoding='latin-1')
text = ff.readlines()
ff.close()

hash_table = defaultdict(list)
original_data = {}
tasa_flujo = []

n=1
while n < len(text):
	data = text[n].split()
	num = data[0]
	caudal = int(data[1])
	hash_table[caudal].append(num)
	original_data[num] = text[n]
	if caudal not in tasa_flujo:
		tasa_flujo.append(caudal)
	n = n+1

tasa_flujo = sorted(tasa_flujo, reverse=True)

n=0
mayor_caudal = []
while len(mayor_caudal) < 300:
	longitud_actual = len(mayor_caudal)
	posibles_inclusiones = hash_table[tasa_flujo[n]]
	if longitud_actual + len(posibles_inclusiones) > 300:
		mayor_caudal += posibles_inclusiones[0:300-len(mayor_caudal)]
	else:
		mayor_caudal += posibles_inclusiones
	n = n+1

ff = open("top_300_rios.csv", "w", encoding='latin-1')
writer = csv.writer(ff, quoting=csv.QUOTE_NONNUMERIC)
writer.writerow(text[0].split())

for identificacion in mayor_caudal:
		info = original_data[identificacion].split()
		writer.writerow([int(x) for x in info[0:2]] + [float(x) for x in info[2:7]] + [int(x) for x in info[7:9]] + [float(info[9])] + info[10:12] + procesar_info(info[12:])) 
ff.close()

os.remove('info_rios_temp.txt')

print("Archivo creado con exito")
