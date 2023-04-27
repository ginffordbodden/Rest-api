from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API = 'http://restapi:5001/api' 

@app.route('/',methods=['GET','POST'])
def index():
  data = {}
  if request.method == 'POST':
    requests.post(
      API,
      json={
        'nombre': request.form['nombre'],
        'significado': request.form['significado']
      })
    data['mensaje'] = "Palabra ingresada"
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/eliminar/<nombre>',methods=['GET'])
def eliminar(nombre):
  requests.delete(f'{API}/{nombre}')
  data = {'mensaje': 'Palabra eliminada'}
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/editar/<nombre>', methods=['GET'])
def editar(nombre):
  res = requests.get(f'{API}/{nombre}').json()
  data = {'palabra':{'significado':res['significado'],'nombre':nombre}}
  
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

@app.route('/editar/<nombre>', methods=['POST'])
def editar2(nombre):
  requests.patch(
    f'{API}/{nombre}',
    json={
      'significado':request.form['significado']
    })
  data = {'mensaje':'Palabra editada'}
  data['palabras'] = obtenerPalabras()
  return render_template('index.html',data=data)

def obtenerPalabras():
  res = requests.get(API).json()
  return res['palabras']

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000,debug=True)
