import numpy as np
import matplotlib.pyplot as plt

# Cargar la matriz binaria desde el archivo .npy
file_path = 'letra_binary/C/C_original_binary.npy'
binary_matrix = np.load(file_path)

# Visualizar la matriz binaria
plt.imshow(binary_matrix, cmap='gray')
plt.title('Matriz Binaria')
plt.axis('off')  # Quitar los ejes
plt.show()
