from flask import Flask, render_template, request, redirect, url_for
from flask import send_file #biblioteca o modulo send_file para forzar la descarga
from funciones import listaArchivos, guardar_foto, allowed_file, borrar_foto, bajar_Archivo  # Importa la función registrarArchivo desde funciones.py



app = Flask(__name__) #Declarando nombre de la  aplicación e inicializando

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', list_Photos = listaArchivos())




@app.route('/guardar-foto', methods=['GET', 'POST'])
def registrarArchivo():
    if request.method == 'POST':
        file = request.files['archivo']
        if file and allowed_file(file.filename): #si el archivo existe y se pasa a la funcion para comprobar que tenga una extensión .jpg, .jpeg o .png
            guardar_foto(file)  # Llama a la función para guardar el archivo
    
            return render_template('index.html', list_Photos = listaArchivos())

        # Verificar si se ha enviado un archivo
        if 'file' not in request.files:
            # Redirigir a una página de error personalizada
            return redirect(url_for('error_page'))
            
        # Verificar si se ha seleccionado un archivo
        if file.filename == '':
            return "Error: No se ha seleccionado ningún archivo", 400

        # Gestionar si el archivo tiene una extensión NO permitida (p. ej., jpg, jpeg, png)
        if file and not allowed_file(file.filename):
            # Redirigir a una página de error personalizada
            return redirect(url_for('error_page'))


@app.route('/<string:nombreFoto>', methods=['GET','POST'])
def EliminarFoto(nombreFoto=''):
        if request.method == 'GET':
            borrar_foto(nombreFoto) # Llama a la función para borrar el archivo
        
        return render_template('index.html', list_Photos = listaArchivos())

@app.route('/descargar/<string:nombreFoto>', methods=['GET','POST'])
def descargar_Archivo(nombreFoto=''):
    url_File = bajar_Archivo(nombreFoto)
    #send_file toma 2 parametros, el primero será la ruta del archivo y el
    # 2 será as_attachment=True porque deseamos que el archivo sea descargable.
    resp =  send_file(url_File, as_attachment=True)
    return resp   


#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
    return 'Ruta no encontrada'

@app.route('/error')
def error_page():
    return render_template('error.html')

#Arrancando la aplicacion
if __name__ == '__main__':
    app.run(debug=True, port=5000)