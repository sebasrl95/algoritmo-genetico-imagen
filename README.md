# Sistema Experto Diagnóstico Médico

Este proyecto fue creado con [Create React App](https://github.com/facebook/create-react-app).

## Lógica de la aplicación

Se encuentra en el archivo Python 

`/backend/diagnostic-system.py`

que expone un API en http://localhost:5000/evaluate que consulta el front.

Las reglas del archivo CLIPS se encuentran en

`/backend/diagnostico.clp`

Para correr el api el archivo Python:

`python diagnostic-system.py`

## Interfaz gráfica

Requisito: Instalar NodeJS

Para instalar las dependencias: 

### `npm install`

Para ejecutar el front:

### `npm start`

Abre [http://localhost:3000](http://localhost:3000) para verlo en tu navegador.