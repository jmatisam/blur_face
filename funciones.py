from flask import Flask, app, render_template, request
from flask import send_file #biblioteca o modulo send_file para forzar la descarga
import uuid  #Modulo de python para crear un string para nombrar el orden de las fotos
from werkzeug.utils import secure_filename #  Subir archivos al servidor de forma segura manejar la subida de archivos desde formularios en el framework Flask https://juncotic.com/archivos-en-formulario-de-flask/ , cómo guardarlos y cómo limitar el tipo y tamaño de archivos permitidos a través de las validaciones de campo.
import cv2 # OpenCV para cargar imágenes, realizar operaciones de procesamiento de imágenes, como difuminar rostros, y mucho más.
import os #El módulo os en Python proporciona los detalles y la funcionalidad del sistema operativo.
from os import remove #Modulo  para remover archivo
from os import path #Modulo para obtener la ruta o directorio
from mtcnn import MTCNN


# --------------Funciones para el manejo de archivos ----------------------------



#Funcion que recorre todos las fotos almacenados en la carpeta (archivos)  
def listaArchivos():
    urlFiles = 'static/archivos'
    return (os.listdir(urlFiles))

def guardar_foto(file):
    filename = secure_filename(file.filename) 
    basepath = path.dirname(__file__) 
    img_path = path.join(basepath, 'static/archivos', filename) 
    file.save(img_path)  # Guardar la imagen en la ruta especificada
    process_image(img_path) # Función para procesar la imagen y detectar rostros


# Función para procesar la imagen y detectar rostros
def process_image(img_path):
    # Cargar la imagen
    image = cv2.imread(img_path)
    # Convertir la imagen a RGB (MTCNN espera imágenes en formato RGB)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Inicializar el detector MTCNN
    detector = MTCNN()
    # Detectar rostros en la imagen
    results = detector.detect_faces(image_rgb)
    # Difuminar los rostros detectados
    for result in results:
        x, y, w, h = result['box']
        # Ampliar o reducir el cuadro delimitador
        # Definir un factor de expansión (por ejemplo, 0.2 para aumentar en un 20%)
        expansion_factor = 0.001
        # Calcular el aumento en las coordenadas
        dx = int(w * expansion_factor / 2)
        dy = int(h * expansion_factor / 2)
        # Aplicar el aumento a las coordenadas del cuadro delimitador
        x -= dx
        y -= dy
        w += 2 * dx
        h += 2 * dy
        
        # Asegurarse de que las coordenadas no sean negativas
        x = max(0, x)
        y = max(0, y)
        
        # Difuminar el área expandida del rostro
        face = image[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
        image[y:y+h, x:x+w] = blurred_face

 # Sobrescribir la imagen original con la versión difuminada
    cv2.imwrite(img_path, image)

    # Devuelve la ruta de la imagen guardada
    return img_path


# Verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

# Para el Boton de borrar_foto, y poder eliminar las que deseemos.
def borrar_foto(nombreFoto):    
        basepath = path.dirname (__file__) #C:\xampp\htdocs\elmininar-archivos-con-Python-y-Flask\app
        url_File = path.join (basepath, 'static/archivos', nombreFoto)
        
        #verifcando si existe el archivo, con la funcion (path.exists) antes de de llamar remove 
        # para eliminarlo, con el fin de evitar un error si no existe.
        if path.exists(url_File):
            remove(url_File) #Borrar foto desde la carpeta
        
    
# Para el Boton de descargar_foto, y poder bajar las que deseemos.
def bajar_Archivo(nombreFoto=''):
    basepath = path.dirname (__file__) 
    url_File = path.join (basepath, 'static/archivos', nombreFoto)
    
    return url_File


