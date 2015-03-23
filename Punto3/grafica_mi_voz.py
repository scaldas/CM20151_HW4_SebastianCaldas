import wave
import sys
import matplotlib.pyplot as plt
import pylab as pili
import numpy as np

spf = wave.open('mi_nombre.wav','r')

signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()
time = np.linspace(0, len(signal)/fs, num=len(signal))

plt.figure(figsize=(10,6))
plt.plot(time, signal)
plt.title('Onda Modulada')
plt.xlabel('Tiempo (s)')
#Para entender la etiquieta del eje y, ver http://www.mathworks.com/matlabcentral/answers/86258-what-is-the-amplitude-unit-when-we-plot-wav-files
plt.ylabel('Voltaje (normalizado al minimo/maximo soportado)')
pili.savefig('mi_voz.png', bbox_inches='tight')
