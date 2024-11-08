import tensorflow as tf
from tensorflow import keras
import numpy as np
from vid import extract_frames
import os
import cv2
import numpy as np

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
    print(predicciones)
    #si la predicción es fumador, guardar el frame en una carpeta
    for i in range(len(predicciones)):
        if predicciones[i][0] > 0.5:
            cont += 1
            if len(str(i)) != 4:
                filename = 'frame' + '0'*(4-len(str(i))) + str(i) + '.jpg'
            else:
                filename = 'frame' + str(i) + '.jpg'
            img = os.path.join(input_path, filename)
            cv2.imwrite(os.path.join(result_path, filename, img))
    print("Se han encontrado ", cont, " fotogramas de fumador")
    return predicciones

# Cargar el modelo
modelo = tf.keras.models.load_model('v1.keras')

video_path = 'videofumando.mp4'
output_path = ''
result_path = './result'



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





