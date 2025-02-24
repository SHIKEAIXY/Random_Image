import os
import socket
import random
import logging
import colorlog
from flask import Flask, jsonify, send_from_directory, make_response

Image_path = './Img/'  # 图片路径
Port = '5366'          # Flask 运行的端口号
Route_name = 'Fafa'    # 路由名称
Mode = True            # 调试模式，修改为布尔类型
app = Flask(__name__)

# 配置日志
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s%(reset)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'bold_green',
        'WARNING': 'underline_yellow',
        'ERROR': 'bold_red',
        'CRITICAL': 'bold_red,bg_white',
    },
    secondary_log_colors={
        'asctime': {
            'DEBUG': 'cyan',
            'INFO': 'cyan',
            'WARNING': 'cyan',
            'ERROR': 'cyan',
            'CRITICAL': 'cyan'
        }
    }
))
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

green_text = "\033[92m"
blue_text = "\033[94m"
yellow_text = "\033[93m"
reset_text = "\033[0m"

# 加载图片列表
def load_images():
    images = []
    try:
        for root, _, files in os.walk(Image_path):
            images.extend([os.path.join(root, f) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'))])
    except Exception as e:
        logger.error(f"加载图片时出错: {e}")
    return images

images = load_images()  # 缓存图片列表

@app.route('/' + Route_name)
def random_image():
    if not images:
        logger.error("图片不存在")
        return jsonify({"error": "图片不存在"}), 404
    selected_image_path = random.choice(images)
    resp = make_response(send_from_directory(os.path.dirname(selected_image_path), os.path.basename(selected_image_path)))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    log_image_path = selected_image_path.replace(Image_path, "")
    logger.info(f"访问图片: {log_image_path}")
    return resp

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        logger.error(f"获取内网IP失败：{e}")
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    import sys
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None  # 禁用 Flask 启动时的横幅信息

    try:
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            mode_str = "当前处于调试模式" if Mode else "当前处于生产模式"
            print(f"{yellow_text}服务已启动（{mode_str}）{reset_text}")
            print(f"{blue_text}本地访问地址：{green_text}http://127.0.0.1:{Port}/{Route_name}{reset_text}")
            print(f"{blue_text}内网访问地址：{green_text}http://{local_ip}:{Port}/{Route_name}{reset_text}")
            print(f"{yellow_text}如需外部访问，请开放{Port}端口号{reset_text}")
        app.run(debug=Mode, port=Port, host='0.0.0.0')
    except Exception as e:
        logger.error(f"服务启动失败: {e}")