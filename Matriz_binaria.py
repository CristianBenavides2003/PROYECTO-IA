import os
import numpy as np
import csv

# Directorio de trabajo actual donde está la carpeta 'binary_letters'
main_folder = os.path.join(os.getcwd(), 'Media/binary_letters')

# Crear la carpeta de salida para guardar los vectores
output_folder = os.path.join(os.getcwd(), 'Media/Matriz')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f'Creada la carpeta: {output_folder}')

# Inicializar un diccionario para guardar todos los vectores
all_vectors = {}

# Obtener la lista de carpetas de letras (de la A a la Z)
letter_folders = [f for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f))]

# Recorrer cada carpeta de letra
for letter_folder_name in letter_folders:
    current_letter_folder = os.path.join(main_folder, letter_folder_name)

    # Obtener los archivos .npy dentro de la carpeta de la letra actual
    image_files = [f for f in os.listdir(current_letter_folder) if f.endswith('.npy')]

    # Procesar cada archivo .npy en la carpeta
    for j, image_file in enumerate(image_files):
        # Cargar la matriz binaria desde el archivo .npy
        npy_path = os.path.join(current_letter_folder, image_file)
        binary_matrix = np.load(npy_path)

        # Inicializar un vector vacío donde guardaremos los resultados
        result_vector = []

        # Contar los 1 en cada columna
        for k in range(binary_matrix.shape[1]):
            count_ones_col = np.sum(binary_matrix[:, k] == 1)
            result_vector.append(count_ones_col)

        # Crear el nombre del vector (por ejemplo, A1, A2, etc.)
        vector_name = f'{letter_folder_name.upper()}{j + 1}'  # Usar mayúsculas para el nombre

        # Asignar el vector al diccionario con su nombre correspondiente
        all_vectors[vector_name] = result_vector

        # Mostrar el vector resultante (opcional, para depuración)
        print(f'Vector para {vector_name}: {result_vector}')

# Guardar todos los vectores en un archivo .csv
csv_file_path = os.path.join(output_folder, 'todos_los_vectores.csv')
try:
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')  # Cambiar el delimitador a ';'
        
        # Agregar la cabecera al archivo
        header = ['Letra'] + [f'x{i + 1}' for i in range(len(next(iter(all_vectors.values()))) )]  # Dinámicamente calcular la longitud del vector
        writer.writerow(header)  # Escribir la cabecera
        
        # Escribir cada vector en el archivo
        for vector_name, vector_data in all_vectors.items():
            # Escribir el nombre del vector seguido de sus datos
            writer.writerow([vector_name] + vector_data)  # Sin corchetes
    print(f'Todos los vectores se han guardado en un archivo CSV en: {csv_file_path}')
except Exception as e:
    print(f'No se pudo guardar el archivo CSV. Error: {e}')
