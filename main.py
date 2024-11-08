import tensorflow as tf
from tensorflow import keras
import numpy as np
from vid import extract_frames
import os
import cv2
import numpy as np
import shutil


def getImages(directorio, size=(256,256)):
    ## pasar las imagenes a np.array
    imagenes = []
    etiquetas = []
    for filename in os.listdir(directorio):
        img = cv2.imread(os.path.join(directorio, filename))
        img = cv2.resize(img, size)
        imagenes.append(img)
        etiquetas.append(0)
    return np.array(imagenes), np.array(etiquetas)

#funcion para cargar las fotos al modelo y que las clasifique en fumador o no fumador
def predictImages(modelo, datos, result_path, input_path):
    predicciones = modelo.predict(datos)
    cont = 0
    # Verifica si el directorio existe, si no, lo crea
    if not os.path.exists(result_path):
        os.makedirs(result_path)

    #borrar todo el contenido de la carpeta de resultados
    for filename in os.listdir(result_path):
        os.remove(os.path.join(result_path, filename))

    #si la predicción es fumador, guardar el frame en una carpeta
    for i in range(len(predicciones)):
        if predicciones[i][0] > 0.8:
            cont += 1
            if len(str(i)) != 4:
                filename = 'frame_' + '0'*(4-len(str(i))) + str(i) + '.jpg'
            else:
                filename = 'frame_' + str(i) + '.jpg'

            # Ruta completa del archivo en la carpeta input
            input_file = os.path.join(input_path, filename)
            shutil.copy(input_file, result_path)
    print("Se han encontrado ", cont, " fotogramas de fumador")
    return predicciones

# Cargar el modelo
modelo = tf.keras.models.load_model('v1.keras')

video_path = 'fumo.mp4'
output_path = ''
result_path = './datavid/result'



# extraer frames del video
frames_path = extract_frames(video_path, output_path)


print("Extracción de fotogramas completada con aceleración GPU del video ", frames_path)

# Cargar los datos
datos, etiquetas = getImages(frames_path)

print("Datos cargados")

# Normalizar los datos
datos = datos / 255.0

print("Prediciendo las imagenes...")
# Predecir las imagenes
predicciones = predictImages(modelo, datos, result_path, frames_path)

print("Predicciones completadas")





