from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import algoritmo_genetico_deteccion_imagen
from PIL import Image, ImageEnhance, ImageFilter
import os

app = Flask(__name__)

# Habilitar CORS en la aplicación
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    # Guardar la imagen que se subió
    file = request.files['image']
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    file.save(file_path)

    # Correr el algoritmo genético en la imagen
    best_params = algoritmo_genetico_deteccion_imagen.run_genetic_algorithm(file_path)

    # Aplicar los mejores parámetros a la imagen original
    img = Image.open(file_path)
    img = apply_best_params_to_image(img, best_params)
    
    # Guardar la imagen procesada
    processed_image_path = os.path.join('uploads', 'processed_' + filename)
    img.save(processed_image_path)

    # Enviar la imagen procesada al frontend
    return send_file(processed_image_path, mimetype='image/png')

def apply_best_params_to_image(img, params):
    brillo, contraste, umbral = params

    # Aplicar los mejores parámetros a la imagen
    enhancer = ImageEnhance.Brightness(img)
    img_bright = enhancer.enhance(brillo)

    enhancer = ImageEnhance.Contrast(img_bright)
    img_contrast = enhancer.enhance(contraste)

    img_gray = img_contrast.convert("L")  # Escala de grises
    img_edge = img_gray.filter(ImageFilter.FIND_EDGES)

    return img_edge

if __name__ == '__main__':
    app.run(debug=True)
