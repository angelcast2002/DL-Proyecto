import tensorflow as tf
import numpy as np
from vid import extract_frames
import os
import cv2
import numpy as np

def getImages(directorio, size=(256,256)):
    datos = []
    etiquetas = []
    for etiqueta, clase in enumerate(["fumador", "noFumador"]):
        pathClass = os.path.join(directorio, clase)
        for img in os.listdir(pathClass):
            imgPath = os.path.join(pathClass, img)
            imagen = cv2.imread(imgPath)
            if imagen is not None: 
                imagen = cv2.resize(imagen, size)
                datos.append(imagen)
                etiquetas.append(etiqueta)
    return (np.array(datos), np.array(etiquetas))

#funcion para cargar las fotos al modelo y que las clasifique en fumador o no fumador
def predictImages(modelo, datos, result_path):
    predicciones = modelo.predict(datos)
    #si la predicción es fumador, guardar el frame en una carpeta
    for i in range(len(predicciones)):
        if predicciones[i] > 0.5:
            cv2.imwrite(result_path + '/frame'+str(i)+'.jpg', datos[i])
    return predicciones

# Cargar el modelo
modelo = tf.keras.models.load_model('v1.keras')

video_path = 'videofumando.mp4'
output_path = ''
result_path = './result'



# extraer frames del video
frames_path = extract_frames(video_path, output_path)

# Cargar los datos
datos, etiquetas = getImages(frames_path)

# Normalizar los datos
datos = datos / 255.0

# Predecir las imagenes
predicciones = predictImages(modelo, datos)





