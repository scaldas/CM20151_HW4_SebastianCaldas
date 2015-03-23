#include <stdlib.h>
#include <stdio.h>

//Se uso SOX
int main()
{
	printf("¡Tienes 4 segundos para decir tu nombre completo!\n");
	system("rec -c 1 -b 16 mi_nombre.wav trim 0 4");
	return 0;
}