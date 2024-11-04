import os
import cv2
import numpy as np

def ejecutar_entrenamiento():
    dataPath = '/home/sistemas/Documentos/Interfaz-main/Interfaz_Eye_System/formularios/base_de_datos/data'
    peopleList = os.listdir(dataPath)
    labels = []
    facesData = []
    label = 0

    for nameDir in peopleList:
        personPath = os.path.join(dataPath, nameDir)
        for fileName in os.listdir(personPath):
            labels.append(label)
            facesData.append(cv2.imread(os.path.join(personPath, fileName), 0))
        label += 1

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(facesData, np.array(labels))
    face_recognizer.write('prueba.xml')
    print("Modelo guardado")