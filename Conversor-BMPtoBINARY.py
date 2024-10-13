from PIL import Image
import numpy as np

# Abrir la imagen BMP
imagen = Image.open('Media\Images\A1.bmp')

# Convertir la imagen a escala de grises
imagen_gris = imagen.convert('L')  # 'L' convierte a escala de grises

# Definir un umbral para la conversión binaria
umbral = 128

# Convertir la imagen en un array numpy binario (0 y 1)
matriz_binaria = np.array(imagen_gris) > umbral
matriz_binaria = matriz_binaria.astype(int)  # Convertir booleano a 0 y 1

print(matriz_binaria)
