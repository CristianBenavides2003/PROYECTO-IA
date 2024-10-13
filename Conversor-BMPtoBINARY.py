from PIL import Image
import numpy as np

# Abrir la imagen BMP
imagen = Image.open('Media\Images\A1.bmp')

# Redimensionar la imagen a 100x100 píxeles
imagen_redimensionada = imagen.resize((100, 100))

# Convertir la imagen a escala de grises
imagen_gris = imagen_redimensionada.convert('L')

# Definir un umbral para la conversión binaria
umbral = 128  # Umbral para distinguir entre blanco y negro (0 o 1)

# Convertir la imagen en un array numpy binario (0 y 1)
matriz_binaria = np.array(imagen_gris) < umbral  # Ahora debería tener ceros y unos
matriz_binaria = matriz_binaria.astype(int)  # Convertir booleano a 0 y 1

# Guardar la matriz binaria en un archivo CSV, con espacios en lugar de comas
with open('matriz_binaria.csv', mode='w', newline='') as archivo_csv:
    for fila in matriz_binaria:
        fila_str = ' '.join(map(str, fila))  # Convertir cada fila a una cadena separada por espacios
        archivo_csv.write(fila_str + '\n')   # Escribir la fila en el archivo, seguida de un salto de línea

print("Matriz binaria redimensionada y guardada en 'matriz_binaria.csv'")
