from scipy.fftpack import ifft, fft, fftfreq
import matplotlib.pyplot as plt
import pylab as pili
import numpy as np
import copy
import wave
import sys

def find_nearest(array,value):
    idx = (abs(array-value)).argmin()
    return idx

spf = wave.open('mi_nombre.wav','r')

signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()
time = np.linspace(0, len(signal)/fs, num=len(signal))

fft_x = fft(signal) / len(time)
freq = fftfreq(len(time), time[1]-time[0])
plt.figure(figsize=(10,6))
plt.plot(freq,abs(fft_x))
plt.title('Transformada de Fourier')
#Las unidades de la frecuencia dependen del sampling rate el cual no es necesariamente el mismo para todos los dispositivos
#Es decir, uniadades arbitrarias
plt.xlabel('Frecuencia')
#Para la amplitud se conservan las unidades normalizadas de la grafica anterior
plt.ylabel('Amplitud')
pili.savefig('mivoz_fft.png', bbox_inches='tight')

#EXPLICACION: Como hallar el armonico mas grande
#Teniendo la transformada rapida de fourier, necesitamos el valor absoluto de los valores en el espacio de frecuencias
abs_fft = copy.copy(fft_x)
abs_fft = abs(abs_fft)

#where es una funcion que me retorna el indice en el que se cumple la condicion dada. En este caso me retorna dos indices pues 
#el maximo ocurre en una frecuencia positiva y en su negativa. Trabajare con el positivo.
indexes = pili.where(abs_fft==max(abs_fft))

#Averiguo cuantos multiplos de esta frecuencia hay en todo el espacio de frecuencias que tengo
#Realmente hay 2*rango + 1 multiplos, pero con rango tengo suficiente
rango = int(max(freq)/freq[indexes[0][0]]);

#Averiguo todos los multiplos de la frecuencia fundamental en el espacio de frecuencias. 
#Note que voy de -rango a rango + 1 para obtener los 2*rango + 1 multiplos de los que hablaba. 
harmonics = []
for i in range (-rango, rango + 1):
    a = pili.where(freq - i*freq[indexes[0][0]] == 0)
    #Si el multiplo exacto que me interesa esta en el espacio de frecuenicas, lo marco como armonico
    if len(a[0]) != 0:
        harmonics.append(freq[a[0][0]])
    else:
    #Si no esta el multiplo exacto, hallo la frecuencia mas cercana que si este en el espacio de frecuencias
        harmonics.append(freq[find_nearest(freq, i*freq[indexes[0][0]])])

#Para graficar solo los armonicos, mando a cero todas las amplitudes de las frecuencias que no sean un armonico
for i in range(0, len(abs_fft)):
    if freq[i] not in harmonics:
        abs_fft[i] = 0 

print('El armonico fundamental es ' + str(freq[indexes[0][0]]) + ' con sus multiplos. Estos se grafican en mivoz_fft_armonicos.png')
print('La explicacion de como llegue a estos valores se encuentra como comentario en el codigo :D')

plt.figure(figsize=(10,6))
plt.plot(freq, abs_fft)
plt.title('Armonicos')
plt.xlabel('Frecuencia')
plt.ylabel('Amplitud')
pili.savefig('mivoz_fft_armonicos.png', bbox_inches='tight')
