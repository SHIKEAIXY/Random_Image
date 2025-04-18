import os
import sys
import socket
import random
import logging
import colorlog
import requests
from flask import Flask, jsonify, send_from_directory, make_response

# 设置终端标题
if os.name == 'nt':
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("BY SHIKEAIXY & Random_Image")
    except:
        pass
else:
    print(f"\033]0;BY SHIKEAIXY & Random_Image\007", end='', flush=True)

# 获取当前目录
if getattr(sys, 'frozen', False):
    current_dir = os.path.dirname(sys.executable)
else:
    current_dir = os.getcwd()

config_file = os.path.join(current_dir, 'config.py')

# 定义控制台文本颜色
green_text = "\033[92m"
blue_text = "\033[94m"
yellow_text = "\033[93m"
reset_text = "\033[0m"

# 创建Log文件夹
log_dir = os.path.join(current_dir, 'Log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s总访问次数：%(total_visits)d | %(asctime)s%(reset)s - %(levelname)s - %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
    }
))

log_file = os.path.join(log_dir, 'app.log')
error_log_file = os.path.join(log_dir, 'error.log')
visit_count_file = os.path.join(log_dir, 'visit_count.txt')

file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('总访问次数：%(total_visits)d | %(asctime)s - %(levelname)s - %(message)s'))

error_file_handler = logging.FileHandler(error_log_file, encoding='utf-8')
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(logging.Formatter('总访问次数：%(total_visits)d | %(asctime)s - %(levelname)s - %(message)s'))
logger = colorlog.getLogger()

if not logger.handlers:
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
logger.setLevel(logging.INFO)

def create_config_file():
    try:
        if os.path.exists(visit_count_file):
            with open(visit_count_file, 'r', encoding='utf-8') as f:
                total_visits = int(f.read())
        else:
            total_visits = 0

        with open(config_file, 'w', encoding='utf-8') as f:
            f.write("Port = '5366'          # 端口号\n")
            f.write("Route_name = 'Fafa'    # 路由名称\n")
            f.write("Mode = True            # 调试模式，True为开启 False为关闭\n")
            f.write("Image_path = './Img/'  # 图片路径\n")
            f.write("Rate_Limit = 10000     # 频率限制值（建议100-10000）\n")

        Image_path = os.path.join(current_dir, 'Img')
        if not os.path.exists(Image_path):
            os.makedirs(Image_path)

        tutorial_file = '教程.txt'
        with open(tutorial_file, 'w', encoding='utf-8') as f:
            f.write("1. 编辑config.py进行修改(可默认)\n2. 将图片放置在Img/中 (支持'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')\n可前往https://gitee.com/SHIKEAIXY/zhenxun-wallpaper-picture可前往此处下载可爱真寻2000张+\n3. 重新点击程序启动")

        extra = {'total_visits': total_visits}
        logger.info("配置文件已生成\n请前往当前目录查看`教程.txt`后重新运行本程序", extra=extra)
        input("按回车键退出程序，配置完毕后重新运行 python Random_Image.py ...")
        sys.exit()
    except Exception as e:
        total_visits = 0
        extra = {'total_visits': total_visits}
        logger.error(f"创建配置文件时出错: {e}", extra=extra)
        input("按回车键退出程序...")
        sys.exit()

if not os.path.exists(config_file):
    create_config_file()

import importlib.util
spec = importlib.util.spec_from_file_location("config", config_file)
config = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(config)
    if not config.Port.isdigit() or not (0 < int(config.Port) <= 65535):
        raise ValueError(f"端口号必须为1-65535之间的数字，当前为: {config.Port}")
        
    Image_path = os.path.join(current_dir, config.Image_path.strip('./'))
    if not os.path.exists(Image_path):
        os.makedirs(Image_path)
    if os.path.exists(visit_count_file):
        with open(visit_count_file, 'r', encoding='utf-8') as f:
            total_visits = int(f.read())
    else:
        total_visits = 0
except ValueError as e:
    logger.error(f"配置错误: {e}")
    input("按任意键退出并修改config.py文件...")
    sys.exit(1)
except Exception as e:
    logger.error(f"加载配置文件时出错: {e}")
    input("按任意键退出...")
    sys.exit(1)

app = Flask(__name__)
Mode = config.Mode
Port = config.Port
Route_name = config.Route_name

if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not Mode:
    print("免费开源软件：\nhttps://Gitee.com/SHIKEAIXY/Random_Image\nhttps://Github.com/SHIKEAIXY/Random_Image")

def load_images():
    images = []
    try:
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not Mode:
            for root, _, files in os.walk(Image_path):
                for f in files:
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
                        images.append(os.path.join(root, f))
            extra = {'total_visits': total_visits}
            logger.info(f"加载到 {len(images)} 张图片", extra=extra)
    except Exception as e:
        logger.error(f"加载图片时出错: {e}")
    return images

images = load_images()

@app.route('/' + Route_name)
def random_image():
    global total_visits
    total_visits += 1

    with open(visit_count_file, 'w', encoding='utf-8') as f:
        f.write(str(total_visits))

    if total_visits > int(config.Rate_Limit):
        extra = {'total_visits': total_visits}
        logger.warning(f"访问次数异常: {total_visits}", extra=extra)
        return jsonify({"error": "访问过于频繁"}), 429

    if not images:
        extra = {'total_visits': total_visits}
        logger.error("图片不存在", extra=extra)
        return jsonify({"error": "图片不存在"}), 404
        
    selected_image_path = random.choice(images)
    resp = make_response(send_from_directory(os.path.dirname(selected_image_path), os.path.basename(selected_image_path)))
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
    log_image_path = selected_image_path.replace(Image_path, "")
    extra = {'total_visits': total_visits}
    logger.info(f"访问图片: {log_image_path}", extra=extra)
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

def get_public_ip():
    try:
        response = requests.get('https://icanhazip.com')
        return response.text
    except Exception as e:
        logger.error(f"获取公网IP失败：{e}")
        return None

if __name__ == '__main__':
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    import sys
    cli = sys.modules['flask.cli']
    cli.show_server_banner = lambda *x: None

    try:
        if not Mode or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            mode_str = "当前处于调试模式" if Mode else "当前处于生产模式"
            print(f"{yellow_text}服务已启动（{mode_str}）{reset_text}")
            print(f"{blue_text}本地访问地址：{green_text}http://127.0.0.1:{Port}/{Route_name}{reset_text}")
            print(f"{blue_text}内网访问地址：{green_text}http://{local_ip}:{Port}/{Route_name}{reset_text}")
            if public_ip:
                public_ip = public_ip.rstrip()
                print(f"{blue_text}公网访问地址：{green_text}http://{public_ip}:{Port}/{Route_name}{reset_text}")
            print(f"{yellow_text}如需外部访问，请开放{Port}端口号{reset_text}")
        app.run(debug=Mode, port=int(Port), host='0.0.0.0')
    except Exception as e:
        logger.error(f"服务启动失败: {e}")
        input("按回车键退出程序...")
        sys.exit()