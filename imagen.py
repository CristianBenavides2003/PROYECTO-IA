import os
import cv2
import numpy as np

# Directorio de trabajo actual donde está la carpeta 'Letras'
main_folder = os.path.join(os.getcwd(), 'Media/Imagenes')

# Crear la carpeta de salida dentro del directorio de trabajo
output_folder = os.path.join(os.getcwd(), 'Media/letras_binarias')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)  # Crear carpeta si no existe

# Obtener la lista de carpetas de letras
letter_folders = [f for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f)) and not f.startswith('.')]

# Recorrer cada carpeta de letra
for letter_folder_name in letter_folders:
    current_letter_folder = os.path.join(main_folder, letter_folder_name)

    # Crear la carpeta de salida para esta letra en 'letra_binary'
    output_letter_folder = os.path.join(output_folder, letter_folder_name)
    if not os.path.exists(output_letter_folder):
        os.makedirs(output_letter_folder)
        print(f'Creada la carpeta: {output_letter_folder}')  # Depuración

    # Obtener las imágenes BMP dentro de la carpeta de la letra actual
    image_files = [f for f in os.listdir(current_letter_folder) if f.endswith('.bmp')]

    # Procesar cada imagen en la carpeta
    for image_file in image_files:
        # Leer la imagen
        img_path = os.path.join(current_letter_folder, image_file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Leer la imagen en escala de grises
        print(f'Procesando imagen: {img_path}')  # Depuración

        # Convertir la imagen a binaria usando un umbral
        _, binary_img = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)  # Usar 1 como valor máximo

        # Invertir los valores de la imagen binaria (invertir blancos y negros)
        binary_img = 1 - binary_img

        # Encontrar los contornos de la imagen binaria
        contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Si hay contornos, determinar el área de la región de interés (ROI)
        if contours:
            # Encuentra el rectángulo más pequeño que contiene todos los contornos
            x, y, w, h = cv2.boundingRect(contours[0])  # Usar el primer contorno, que debería ser suficiente
            
            # Recortar la imagen para quedarse solo con la región que contiene información
            cropped_img = binary_img[y:y+h, x:x+w]
        else:
            # Si no hay contornos, usar la imagen original
            cropped_img = binary_img

        # Redimensionar la imagen recortada a 100x100 píxeles
        resized_img = cv2.resize(cropped_img, (100, 100), interpolation=cv2.INTER_NEAREST)

        # Asegurar que la matriz tiene solo valores 0 y 1
        final_binary_img = np.array(resized_img, dtype=np.int32)

        # Guardar la matriz binaria en un archivo .npy
        name, _ = os.path.splitext(image_file)  # Obtener el nombre sin extensión
        npy_save_path = os.path.join(output_letter_folder, f'{name}_binary.npy')
        csv_save_path = os.path.join(output_letter_folder, f'{name}_binary.csv')

        # Guardar la matriz binaria correctamente en formato .npy
        try:
            np.save(npy_save_path, final_binary_img)  # Guardar la matriz en formato .npy
            print(f'Guardada la matriz binaria en: {npy_save_path}')  # Confirmación de guardado
        except Exception as e:
            print(f'No se pudo guardar la matriz binaria en: {npy_save_path}. Error: {e}')

        # Guardar la matriz binaria en formato CSV
        try:
            np.savetxt(csv_save_path, final_binary_img, delimiter=',', fmt='%d')  # Guardar la matriz en formato .csv
            print(f'Guardada la matriz binaria en: {csv_save_path}')  # Confirmación de guardado
        except Exception as e:
            print(f'No se pudo guardar la matriz binaria en: {csv_save_path}. Error: {e}')
