import pandas as pd
import numpy as np
from minisom import MiniSom
from tkinter import filedialog, Tk, Button, messagebox, Label, PhotoImage, Canvas
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Variables globales para la GUI
num_patterns_label = None
num_inputs_label = None
dm_values = []
som = None
training_mode = False  # False: Competencia Suave, True: Competencia Dura
mode_label = None

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel and CSV files", "*.xlsx;*.xls;*.csv")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, delimiter=';')
            else:
                df = pd.read_excel(file_path)

            if df.empty:
                messagebox.showerror("Error", "El archivo está vacío o no contiene datos válidos.")
                return None, None

            numeric_df = df.iloc[1:, 1:].apply(pd.to_numeric, errors='coerce')
            numeric_df.dropna(how='all', axis=1, inplace=True)
            numeric_df.dropna(how='all', axis=0, inplace=True)

            if numeric_df.empty:
                messagebox.showerror("Error", "No se encontraron columnas numéricas en el archivo.")
                return None, None

            entries = numeric_df.values

            if np.isnan(entries).any():
                messagebox.showerror("Error", "El archivo contiene datos no numéricos o valores faltantes.")
                return None, None

            num_patterns = entries.shape[0]
            num_inputs = entries.shape[1]
            num_patterns_label.config(text=f"Número de patrones: {num_patterns}")
            num_inputs_label.config(text=f"Número de entradas: {num_inputs}")

            messagebox.showinfo("Éxito", "Datos cargados correctamente.")
            return entries, df
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
            return None, None

def run_kohonen():
    global dm_values, som, training_mode
    entries, df = load_file()
    if entries is not None and len(entries) > 0:
        map_size = (10, 10)
        som = MiniSom(x=map_size[0], y=map_size[1], input_len=entries.shape[1], sigma=1.0, learning_rate=0.5)

        som.random_weights_init(entries)
        print("Pesos inicializados")

        iterations = 1000
        dm_values = []
        for i in range(iterations):
            som.train_random(entries, 1)
            winner_neurons = [som.winner(x) for x in entries]
            
            # Determinar si se usa competencia dura o suave
            if training_mode:
                dm = np.mean([np.linalg.norm(x - som.get_weights()[n]) for x, n in zip(entries, winner_neurons)])
            else:
                dm = np.mean([np.mean([np.linalg.norm(x - som.get_weights()[n]), 0.5]) for x, n in zip(entries, winner_neurons)])  # Competencia suave simulada
            dm_values.append(dm)

        print("Entrenamiento finalizado")

        for i, x in enumerate(entries):
            winner = som.winner(x)
            print(f"Patrón {i+1} asignado a la neurona vencedora: {winner}")

    else:
        messagebox.showerror("Error", "No se encontraron entradas válidas en el archivo.")

def plot_dm():
    if not dm_values:
        messagebox.showerror("Error", "La red no ha sido entrenada.")
        return
    plt.figure(figsize=(8, 6))
    plt.plot(dm_values, label="Distancia Media (DM)", color='green')
    plt.title("Evolución de la Distancia Media (DM)", color='green')
    plt.xlabel("Iteración", color='green')
    plt.ylabel("DM", color='green')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_weights():
    if som is None:
        messagebox.showerror("Error", "La red no ha sido entrenada.")
        return
    weights = som.get_weights()
    plt.figure(figsize=(8, 6))
    for i, weight_matrix in enumerate(weights):
        plt.subplot(1, len(weights), i + 1)
        plt.imshow(weight_matrix, aspect='auto')
        plt.title(f"Pesos capa {i+1}")
    plt.tight_layout()
    plt.show()

def toggle_mode():
    global training_mode, mode_label
    training_mode = not training_mode  # Cambiar entre suave y dura
    if training_mode:
        mode_label.config(text="Dura")
    else:
        mode_label.config(text="Suave")

def create_gui():
    global num_patterns_label, num_inputs_label, mode_label

    root = Tk()
    root.title("Algoritmo Kohonen - IA con MiniSom")
    root.geometry("700x500")
    root.configure(bg='black')

    # Centro de la pantalla
    root.eval('tk::PlaceWindow . center')

    # Agregar ícono circular ajustado
    canvas = Canvas(root, width=100, height=100, bg='black', highlightthickness=0)
    canvas.pack(pady=10)

    # Cargar y redimensionar imagen
    icon_image = Image.open("Media/icon.png")  # Reemplaza con la ruta de tu ícono
    icon_image_resized = icon_image.resize((100, 100), Image.Resampling.LANCZOS)  # Redimensionar a 100x100
    icon = ImageTk.PhotoImage(icon_image_resized)

    # Dibujar círculo y colocar imagen
    canvas.create_oval(0, 0, 100, 100, outline="green", width=2)
    canvas.create_image(50, 50, image=icon)

    # Botón para cargar archivo y ejecutar Kohonen
    load_button = Button(root, text="Cargar archivo y ejecutar Kohonen", command=run_kohonen, bg='green', fg='black')
    load_button.pack(pady=10)

    # Etiqueta para mostrar tipo de entrenamiento
    mode_text_label = Label(root, text="Tipo de entrenamiento:", fg='green', bg='black', font=('Helvetica', 12))
    mode_text_label.pack(pady=5)

    # Etiqueta que indica el modo de entrenamiento actual
    mode_label = Label(root, text="Suave", fg='green', bg='black', font=('Helvetica', 12))
    mode_label.pack(pady=5)

    # Botón para alternar entre competencia suave y dura
    mode_button = Button(root, text="Cambiar", command=toggle_mode, bg='green', fg='black')
    mode_button.pack(pady=10)

    # Etiquetas para mostrar número de patrones y entradas
    num_patterns_label = Label(root, text="Número de patrones: N/A", fg='green', bg='black', font=('Helvetica', 12))
    num_patterns_label.pack(pady=10)

    num_inputs_label = Label(root, text="Número de entradas: N/A", fg='green', bg='black', font=('Helvetica', 12))
    num_inputs_label.pack(pady=10)

    # Botón para mostrar gráfica de DM
    dm_button = Button(root, text="Mostrar gráfica de DM", command=plot_dm, bg='green', fg='black')
    dm_button.pack(pady=10)

    # Botón para mostrar gráfica de Pesos
    weights_button = Button(root, text="Mostrar gráfica de Pesos", command=plot_weights, bg='green', fg='black')
    weights_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
