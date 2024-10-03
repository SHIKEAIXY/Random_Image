from flask import Flask, jsonify, send_from_directory, make_response
import random
import os

app = Flask(__name__)
image_Fafa = './Img/'

@app.route('/Fafa')
def random_image():
    images = []
    for root, _, files in os.walk(image_Fafa):
        images.extend([os.path.join(root, f) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'))])
    if not images:
        return jsonify({"error": "图片不存在"}), 404
    selected_image_path = random.choice(images)
    resp = make_response(send_from_directory(os.path.dirname(selected_image_path), os.path.basename(selected_image_path)))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5366)