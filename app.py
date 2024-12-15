from flask import Flask, request, jsonify, render_template, Response
import requests
from flask_cors import CORS
import json
import os
import sys

DOUBAO_API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"  # 替换为实际的豆包 API 地址


# 获取打包后的资源路径
def resource_path(relative_path):
    if getattr(sys, '_MEIPASS', False):  # PyInstaller 使用 _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

app = Flask(__name__,
            static_folder=resource_path("static"),       # 适配 static 目录
            template_folder=resource_path("templates"))  # 适配 templates 目录
CORS(app)

# 配置文件路径
CONFIG_FILE = "config.json"


def load_api_key():
    """从配置文件加载 API 密钥"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                config = json.load(file)
                return config.get("api_key", "")
    except Exception as e:
        print(f"加载配置文件时出错: {e}")
    return ""

def save_api_key(api_key):
    """保存 API 密钥到配置文件"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump({"api_key": api_key}, file)
    except Exception as e:
        print(f"保存配置文件时出错: {e}")


# 动态加载 API 密钥
DOUBAO_API_KEY = load_api_key()

@app.route('/')
def home():
    return render_template('index.html')  # 渲染前端页面

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    """设置 API 密钥"""
    data = request.json
    api_key = data.get('api_key', '')
    save_option = data.get('save', False)  # 是否保存密钥

    if save_option:
        save_api_key(api_key)
    global DOUBAO_API_KEY
    DOUBAO_API_KEY = api_key
    return jsonify({"message": "API 密钥已设置成功"})

@app.route('/get_api_key', methods=['GET'])
def get_api_key():
    """获取当前的 API 密钥（仅用于调试，实际可以隐藏）"""
    return jsonify({"api_key": DOUBAO_API_KEY})

@app.route('/generate', methods=['POST'])
def generate_story():
    if not DOUBAO_API_KEY:
        return jsonify({"error": "API 密钥未设置，请先输入您的 API 密钥"}), 400

    data = request.json
    theme = data.get('theme', '')
    characters = data.get('characters', '')
    setting = data.get('setting', '')
    story_type = data.get('type', '')
    max_words = data.get('maxWords', '')  # 获取字数限制参数

    # 构建请求载荷
    payload = {
        "model": "ep-20241212210011-tlt27",  # 替换为你的模型 ID
        "messages": [
            {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
            {
                "role": "user",
                "content": f"根据主题'{theme}'，角色设定'{characters}'，设定为'{setting}'，生成一个{story_type}，字数限制为{max_words}字。"
            }
        ]
    }
    headers = {"Authorization": f"Bearer {DOUBAO_API_KEY}"}

    # 发送请求到豆包 API
    try:
        response = requests.post(DOUBAO_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            story_content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '生成失败')
            return jsonify({"story": story_content})
        else:
            return jsonify({"error": "调用豆包 API 失败", "details": response.text}), 500
    except Exception as e:
        return jsonify({"error": "请求失败，请检查网络连接或 API 密钥", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
