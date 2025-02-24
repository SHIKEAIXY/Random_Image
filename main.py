from flask import Flask, jsonify, send_from_directory, make_response
import random
import socket
import os

Image_path = './Img/'  # 图片路径
Port = '5366'          # Flask 运行的端口号
Route_name = 'Fafa'    # 路由名称
app = Flask(__name__)

@app.route('/' + Route_name)
def random_image():
    images = []
    for root, _, files in os.walk(Image_path):
        images.extend([os.path.join(root, f) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'))])
    if not images:
        return jsonify({"error": "图片不存在"}), 404
    selected_image_path = random.choice(images)
    resp = make_response(send_from_directory(os.path.dirname(selected_image_path), os.path.basename(selected_image_path)))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    return resp

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"获取内网IP失败：{e}")
        return "127.0.0.1"

if __name__ == '__main__':
    green_text = "\033[92m"
    reset_text = "\033[0m"
    local_ip = get_local_ip()

    print("服务已启动")
    print(f"本地访问地址：{green_text}http://127.0.0.1:{Port}/{Route_name}{reset_text}")
    print(f"内网访问地址：{green_text}http://{local_ip}:{Port}/{Route_name}{reset_text}")
    print(f"如需外部访问，请开放{Port}端口号")
    app.run(debug=False, port=Port, host='0.0.0.0')