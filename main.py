from flask import Flask, jsonify, send_from_directory
import random
import os

app = Flask(__name__)
image_Fafa = './Img/'
@app.route('/Fafa')
def random_image():
    images = [f for f in os.listdir(image_Fafa) if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'))]
    if not images:
        return jsonify({"error": "图片不存在"}), 404
    selected_image = random.choice(images)
    return send_from_directory(image_Fafa, selected_image)
if __name__ == '__main__':
    app.run(debug=True, port=5366)