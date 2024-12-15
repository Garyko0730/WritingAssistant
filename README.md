<div align="center">
  <h1>WritingAssistant</h1>
  <p>基于 Flask 和前端技术开发的写作辅助工具，集成 豆包 API，实现故事大纲与文本自动生成。</p>
  <img src="https://img.shields.io/badge/Language-Python%203.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Framework-Flask-orange" alt="Flask">
  <img src="https://img.shields.io/badge/Status-Stable-green" alt="Status">
</div>

---

## 📖 项目简介

**WritingAssistant** 是一个基于 Flask 和前端技术开发的写作辅助工具，集成了 **豆包 API**，支持用户输入主题、角色设定和故事背景等内容，自动生成故事大纲或完整文本。  
项目旨在帮助内容创作者更高效地进行故事创作，提升生产力和灵感输出。

---

## 🚀 功能特性

1. **🔑 API 密钥设置**  
   - 支持用户手动输入和保存 **豆包 API 密钥**，实现故事生成服务的接入。

2. **📚 模板选择**  
   - 提供预设的故事模板（如奇幻冒险、科幻探索、校园生活等），快速生成故事框架。

3. **✍ 故事生成**  
   - 根据输入的主题、角色设定和故事背景，通过 **豆包 API** 生成故事大纲或完整文本。

4. **💬 气泡式对话展示**  
   - 互动式气泡展示生成的故事和用户输入，方便阅读与管理。

5. **📤 文档导出**  
   - 支持将生成的故事内容导出为文本文件（`.txt` 格式）。

---

## 📁 项目结构

```plaintext
WritingAssistant/
│
├── static/                 # 静态资源
│   ├── images/             # 图片资源
│   │   ├── step1.png
│   │   └── step2.png
│   └── styles.css          # CSS 样式文件
│
├── templates/              # HTML 模板文件
│   └── index.html          # 前端用户界面
│
├── config.json             # 配置文件，存储 API 密钥
├── app.py                  # Flask 后端应用
├── requirements.txt        # 项目依赖包列表
└── WritingAssistant.exe    # 打包后的可执行文件
```
---
## 🛠️ 安装与运行

### **1. 环境要求**
   - Python 3.8 及以上  
   - pip 已安装  

### **2. 安装依赖**
在项目根目录下运行以下命令：

```bash
pip install -r requirements.txt
```
### **3. 运行项目**

```bash
python app.py
```
---
## 🔑 配置 API 密钥

1. **获取 API 密钥**  
   - 访问 豆包 API 管理平台 注册并获取 API 密钥。

2. **配置密钥**  
   - 在工具页面的 “设置 API 密钥” 部分输入密钥，点击 “设置密钥” 按钮完成配置。
---

## 📝 注意事项
  - 用户需自行获取 豆包 API 密钥 并正确配置。
  - 若在使用过程中遇到问题，请检查网络连接和 API 服务状态。

