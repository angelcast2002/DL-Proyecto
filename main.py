import threading
import tensorflow as tf
from tensorflow import keras
import numpy as np
from vid import extract_frames
import os
import cv2
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from zipfile import ZipFile
from PIL import Image, ImageTk
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def getImages(directorio, size=(256, 256)):
    imagenes = []
    etiquetas = []
    for filename in os.listdir(directorio):
        img = cv2.imread(os.path.join(directorio, filename))
        img = cv2.resize(img, size)
        imagenes.append(img)
        etiquetas.append(0)
    return np.array(imagenes), np.array(etiquetas)

def predictImages(modelo, datos, result_path, input_path, progress, message_label):
    message_label.config(text="Realizando predicciones sobre las imágenes...")
    predicciones = modelo.predict(datos)
    cont = 0
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    for filename in os.listdir(result_path):
        os.remove(os.path.join(result_path, filename))

    for i in range(len(predicciones)):
        if predicciones[i][0] > 0.8:
            cont += 1
            filename = f'frame_{str(i).zfill(4)}.jpg'
            input_file = os.path.join(input_path, filename)
            shutil.copy(input_file, result_path)
        progress["value"] += 20 / len(predicciones)  # Avanza 20% del total durante las predicciones
        ventana.update_idletasks()
    
    message_label.config(text=f"Se encontraron {cont} fotogramas de fumador")
    return predicciones

def seleccionar_video():
    video_path = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")]
    )
    if video_path:
        return video_path
    return None

def guardar_zip(frames_path, zip_path):
    with ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(frames_path):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    print("Archivo .zip guardado en:", zip_path)

def procesar_video():
    reset_ui()
    video_path = seleccionar_video()
    if video_path:
        progress["value"] = 10
        message_label.config(text="Extrayendo fotogramas del video...")
        ventana.update_idletasks()
        
        output_path = './input_frames'
        frames_path = extract_frames(video_path, output_path)
        time.sleep(1)
        progress["value"] = 30
        message_label.config(text="Fotogramas extraídos con éxito. Cargando modelo...")
        ventana.update_idletasks()

        modelo = tf.keras.models.load_model('v1.keras')
        time.sleep(3)
        progress["value"] = 50
        message_label.config(text="Modelo cargado. Preparando datos...")
        ventana.update_idletasks()

        datos, etiquetas = getImages(frames_path)
        datos = datos / 255.0
        progress["value"] = 70
        message_label.config(text="Datos preparados. Iniciando predicción...")
        ventana.update_idletasks()

        predictImages(modelo, datos, './datavid/result', frames_path, progress, message_label)
        
        messagebox.showinfo("Proceso completo", "El proceso ha finalizado. Ahora selecciona dónde guardar las imágenes.")
        
        zip_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("Archivo ZIP", "*.zip")],
            title="Guardar archivo ZIP"
        )
        if zip_path:
            guardar_zip('./datavid/result', zip_path)
            messagebox.showinfo("Guardado completo", "Las imágenes se han guardado en el archivo ZIP.")
            reset_ui()

def iniciar_procesamiento():
    # Muestra la barra de progreso al iniciar el procesamiento
    progress.pack(pady=10)
    # Ejecuta `procesar_video` en un hilo separado
    thread = threading.Thread(target=procesar_video)
    thread.start()

def reset_ui():
    progress["value"] = 0
    message_label.config(text="")
    btn_procesar.config(state="normal")

# Crear ventana con ttkbootstrap
ventana = ttk.Window(themename="darkly")
ventana.title("Detector de Fumadores en Video")
ventana.geometry("400x400")

# Cargar el logo
#logo_image = Image.open("logo.png")
#logo_image = logo_image.resize((100, 100))
#logo_photo = ImageTk.PhotoImage(logo_image)
#logo_label = ttk.Label(ventana, image=logo_photo)
#logo_label.pack(pady=10)

# Título
titulo_label = ttk.Label(ventana, text="Sube un video para detectar fumadores", font=("Arial", 16))
titulo_label.pack(pady=10)

# Botón para seleccionar el video
btn_procesar = ttk.Button(ventana, text="Seleccionar y procesar video", bootstyle=SUCCESS, command=iniciar_procesamiento)
btn_procesar.pack(pady=10)

# Label para mostrar mensajes de estado
message_label = ttk.Label(ventana, text="", font=("Arial", 10))
message_label.pack(pady=5)

# Barra de progreso (oculta al inicio)
progress = ttk.Progressbar(ventana, orient="horizontal", length=300, mode="determinate", bootstyle="info-striped")
progress.pack_forget()  # Ocultar la barra de progreso al inicio

ventana.mainloop()