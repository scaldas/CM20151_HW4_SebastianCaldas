all: mivoz_fft.png mivoz_fft_armonicos.png mi_voz.png

mivoz_fft.png mivoz_fft_armonicos.png:	fft_de_mi_voz.py
	python fft_de_mi_voz.py

mi_voz.png: grafica_mi_voz.py
	python grafica_mi_voz.py

fft_de_mi_voz.py: mi_nombre.wav
	python fft_de_mi_voz.py

grafica_mi_voz.py: mi_nombre.wav
	python grafica_mi_voz.py

mi_nombre.wav: grabar_mi_nombre.x
	./grabar_mi_nombre.x

grabar_mi_nombre.x: grabar_mi_nombre.c
	cc grabar_mi_nombre.c -o grabar_mi_nombre.x

clean: 
	rm -f mivoz_fft.png mivoz_fft_armonicos.png mi_voz.png mi_nombre.wav


