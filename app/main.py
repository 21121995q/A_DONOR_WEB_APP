from app import app
from flask import render_template, request, jsonify, url_for
from .model import predict
from .utils import allowed_file
import tempfile
import os
import uuid

app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def make_prediction():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Файл отсутствует в запросе'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Файл не выбран'}), 400
        
        if file and allowed_file(file.filename):
            # Генерируем уникальное имя файла
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Сохраняем файл
            file.save(filepath)
            
            # Выполняем предсказание
            prediction, confidence, inference_time = predict(filepath)
            
            # Получаем URL для отображения изображения
            image_url = url_for('static', filename=f'uploads/{filename}')
            
            return jsonify({
                'prediction': prediction,
                'confidence': confidence,
                'inference_time': inference_time,
                'image_url': image_url
            })
        
        return jsonify({'error': 'Недопустимый тип файла'}), 400
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)