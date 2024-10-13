import numpy as np
import os
import pandas as pd

# Cargar los vectores desde el archivo CSV
csv_file_path = 'Media/Matriz/todos_los_vectores.csv'
data = pd.read_csv(csv_file_path, index_col=0)  # Leer el CSV, usando la primera columna como índice

# Obtener los nombres de todos los vectores
fields = data.columns.tolist()
num_vectors = len(fields)
vector_length = data.shape[1]  # Longitud de los vectores originales

# Inicializar un nuevo DataFrame para almacenar los valores en el formato deseado
# Sin columnas adicionales para las salidas binarias
new_vectors = np.zeros((num_vectors, vector_length))

# Especificar las letras que se van a trabajar en el proyecto
letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]  # Letras de 'A' a 'Z'
row_names = []  # Inicializar una lista para almacenar los nombres de las filas

# Determinar cuántos vectores hay por cada letra
num_letters = len(letters)
vectors_per_letter = num_vectors // num_letters  # Número de vectores por letra (aproximado)

# Rellenar el nuevo arreglo y generar nombres del tipo A1, A2, ..., B1, B2, ..., etc.
counter = 0
for letter_index in range(num_letters):
    for j in range(vectors_per_letter):
        if counter < num_vectors:
            # Asignar los valores del vector al arreglo
            new_vectors[counter, :] = data.iloc[counter].values
            # Asignar el nombre para cada fila, por ejemplo A1, A2, A3, etc.
            row_names.append(f'{letters[letter_index]}{j + 1}')
            counter += 1

# Asegurarse de que el número de nombres de filas coincida con el número de vectores
if len(row_names) != new_vectors.shape[0]:
    raise ValueError('El número de nombres de filas no coincide con el número de vectores')

# Crear un DataFrame de pandas para guardar el nuevo arreglo
column_names = [f'x{i + 1}' for i in range(vector_length)]  # Etiquetar columnas de entradas
df = pd.DataFrame(new_vectors, columns=column_names, index=row_names)

# Guardar los valores en un archivo CSV, agregando los nombres de las filas
csv_output_path = 'vectores/bancoDeDatos.csv'
df.to_csv(csv_output_path)

# Mostrar un mensaje de éxito
print(f'Los nuevos vectores han sido guardados en: {csv_output_path}')
