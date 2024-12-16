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
def load_config():
    """从配置文件加载配置"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                config = json.load(file)
                return config
    except Exception as e:
        print(f"加载配置文件时出错: {e}")
    return {}

def save_config(api_key=None, model_id=None):
    """保存配置到配置文件"""
    try:
        config = load_config()  # 读取现有配置
        if api_key:
            config["api_key"] = api_key
        if model_id:
            config["model_id"] = model_id
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(config, file)
    except Exception as e:
        print(f"保存配置文件时出错: {e}")


@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    """设置 API 密钥和模型 ID"""
    data = request.json
    api_key = data.get('api_key', '')
    model_id = data.get('model_id', '')
    save_option = data.get('save', False)  # 是否保存到本地

    if save_option:
        save_config(api_key=api_key, model_id=model_id)  # 保存到配置文件

    # 更新全局变量
    global DOUBAO_API_KEY, DEFAULT_MODEL_ID
    DOUBAO_API_KEY = api_key
    DEFAULT_MODEL_ID = model_id

    return jsonify({"message": "API 密钥和模型 ID 已设置成功"})

@app.route('/set_model_id', methods=['POST'])
def set_model_id():
    """设置模型 ID"""
    data = request.json
    model_id = data.get('model_id', '')
    save_option = data.get('save', False)  # 是否保存模型 ID

    if save_option:
        save_config(model_id=model_id)
    global DEFAULT_MODEL_ID
    DEFAULT_MODEL_ID = model_id
    return jsonify({"message": "模型 ID 已设置成功"})

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
    max_words = data.get('maxWords', '')
    model = data.get('model', '')  # 接受前端传递的模型 ID

    if not model:
        return jsonify({"error": "模型 ID 未设置，请输入模型 ID"}), 400

    # 构建请求载荷
    payload = {
        "model": model,  # 使用用户输入的模型 ID
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

@app.route('/continue', methods=['POST'])
def continue_conversation():
    if not DOUBAO_API_KEY:
        return jsonify({"error": "API 密钥未设置，请先输入您的 API 密钥"}), 400

    data = request.json
    conversation_history = data.get('conversationHistory', [])

    if not conversation_history:
        return jsonify({"error": "对话历史为空，请输入内容后重试"}), 400

    # 构建请求载荷
    payload = {
        "model": DEFAULT_MODEL_ID,  # 从配置加载的模型 ID
        "messages": conversation_history
    }
    headers = {"Authorization": f"Bearer {DOUBAO_API_KEY}"}

    # 调用豆包 API
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
