import math
import pandas as pd
import numpy as np
from tkinter import filedialog, Tk, Button, messagebox

class KohonenAlgorithm:
    def __init__(self, entries, neurons, iterations):
        self.entries = np.array(entries, dtype=float)
        if neurons % 2 != 0:
            raise ValueError("El número de neuronas debe ser par.")
        self.neurons = neurons if neurons >= 2 * self.entries.shape[1] else 2 * self.entries.shape[1]
        self.iterations = iterations
        self.neighborhood_coeff = self.calculate_neighborhood_coeff()
        self.weights = np.random.uniform(-1, 1, (self.entries.shape[1], self.neurons))  # Inicializa los pesos aleatorios
        self.distance_means = []
        self.learning_rate = 1

    def calculate_neighborhood_coeff(self):
        num_connections = (self.neurons * (self.neurons - 1)) // 2
        connections = np.random.uniform(0.1, 1.0, num_connections)
        neighborhood_coeff = np.sum(connections) / num_connections
        return neighborhood_coeff

    def euclidean_distance(self, entriePattern, weightPattern):
        if len(entriePattern) != len(weightPattern):
            return ValueError("Can not calculate that")

        euclidean_value = 0
        for i in range(len(entriePattern)):
            euclidean_value += ((entriePattern[i]) - (weightPattern[i]))**2

        euclidean_value = math.sqrt(euclidean_value)
        return euclidean_value

    def dt_distance(self, dv):
        return dv + self.neighborhood_coeff

    def update_weights(self, columnsToUpdate, winnerDistance):
        print("COLUMNAS A ACTUALIZAR: ", columnsToUpdate)
        print("DISTANCIA EUCLIDIANA DE LA VENCEDORA: ", winnerDistance)
        for i in columnsToUpdate:
            if i < self.weights.shape[1]:  # Asegurarse de que 'i' esté dentro del rango de columnas
                for j in range(len(self.entries)):
                    if j < self.weights.shape[0]:  # Validación para no superar las filas de pesos
                        self.weights[j][i] = self.weights[j][i] + self.learning_rate * winnerDistance
                    else:
                        print(f"Índice {j} fuera de los límites de las filas de pesos.")

    def update_learning_rate(self, iterationNumber):
        self.learning_rate = self.learning_rate / iterationNumber

    def train(self):
        dm = 9999999999
        print("ENTRIES: ", self.entries)
        print(f"ENTRIES QUANTITY: {len(self.entries)}")
        print("NEURONS: ", self.neurons)
        print(f"COEFICIENTE DE V. : {self.neighborhood_coeff}")
        print("PESOS GENERADOS: ", self.weights)
        print("NUMERO DE ITERACIONES: ", self.iterations)
        newIteration = 1
        for x in range(self.iterations):
            winner_neurons = []
            print(f"\nIteracion #{x}")
            for i in range(len(self.entries)):
                euc_distances = []
                for j in range(self.neurons):
                    print("Entrada: ", self.entries[i])
                    print(f"Columna de peso: {self.weights[:, j]}")
                    euc_distances.append(self.euclidean_distance(self.entries[i], self.weights[:, j]))
                    print(f"Distancia euclidiana de patron {self.entries[i]} para neurona {(j+1)} = {euc_distances[-1]}")
                
                neuron_winner = min(euc_distances)
                d_distance = self.dt_distance(neuron_winner)

                indices = [index for index, value in enumerate(euc_distances) if value < d_distance and value != neuron_winner]
                # Asegurarse de que los índices estén dentro del rango permitido
                indices = [i for i in indices if i < self.neurons]
                
                neuron_winnerprint = euc_distances.index(neuron_winner)
                if neuron_winnerprint < self.neurons:
                    indices.append(neuron_winnerprint)

                print(f"La neurona vencedora para el {i+1} patron es: {neuron_winnerprint+1}")
                print(f"La distancia total es: ", d_distance)
                print(f"Las neuronas vecinas son: ", *indices)

                self.update_weights(columnsToUpdate=indices, winnerDistance=euc_distances[neuron_winnerprint])
                winner_neurons.append(euc_distances[neuron_winnerprint])
                self.update_learning_rate(iterationNumber=self.iterations)
                newIteration += 1

            dm = sum(winner_neurons) / len(self.entries)
            print("VALOR DEL DM: ", dm)
            print("Distancias de neuronas vencedoras: ", *winner_neurons)
            if dm == 0 or dm == 0.1 or dm == 0.01:
                return

def load_file():
    # Permitimos la selección de archivos Excel o CSV
    file_path = filedialog.askopenfilename(filetypes=[("Excel and CSV files", "*.xlsx;*.xls;*.csv")])
    if file_path:
        try:
            # Detectar si el archivo es CSV o Excel
            if file_path.endswith('.csv'):
                # Cargar archivo CSV con separador ";"
                df = pd.read_csv(file_path, delimiter=';')
            else:
                # Cargar archivo Excel
                df = pd.read_excel(file_path)

            print(df.head())  # Verificar qué se está cargando del archivo
            
            if df.empty:
                messagebox.showerror("Error", "El archivo está vacío o no contiene datos válidos.")
                return

            # Seleccionamos todas las columnas numéricas comenzando desde la fila 2 y columna B (columna 1 en el índice)
            numeric_df = df.iloc[1:, 1:].apply(pd.to_numeric, errors='coerce')  # Convierte todo a numérico, convierte errores a NaN
            numeric_df.dropna(how='all', axis=1, inplace=True)  # Elimina columnas con solo NaN
            numeric_df.dropna(how='all', axis=0, inplace=True)  # Elimina filas con solo NaN

            print(numeric_df.head())  # Verificar los datos procesados

            if numeric_df.empty:
                messagebox.showerror("Error", "No se encontraron columnas numéricas en el archivo.")
                return

            # Convertimos las filas en listas de floats
            entries = [[float(value) for value in row] for row in numeric_df.values]

            # Verificamos si hay valores faltantes (NaN)
            if any(any(np.isnan(value) for value in row) for row in entries):
                messagebox.showerror("Error", "El archivo contiene datos no numéricos o valores faltantes.")
                return

            messagebox.showinfo("Éxito", "Datos cargados correctamente.")
            return entries
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")

def run_kohonen():
    entries = load_file()
    if entries is not None and len(entries) > 0:
        kohonen2 = KohonenAlgorithm(entries, neurons=8, iterations=1000)
        kohonen2.train()
    else:
        messagebox.showerror("Error", "No se encontraron entradas válidas en el archivo.")

def create_gui():
    root = Tk()
    root.title("Algoritmo Kohonen - IA")

    load_button = Button(root, text="Cargar archivo Excel o CSV y ejecutar Kohonen", command=run_kohonen)
    load_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
