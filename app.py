from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import unquote  # 為了解碼 MAC 地址中的 %3A

app = Flask(__name__)
CORS(app)  # 啟用跨域支援

# 儲存每個裝置的狀態（記憶體中）
device_states = {}

@app.route('/')
def home():
    return "ESP 控制伺服器運作中"

@app.route('/set_command', methods=['POST'])
def set_command():
    data = request.json
    mac = data.get("mac")
    cmd = data.get("cmd")
    if not mac or not cmd:
        return jsonify({"status": "error", "message": "缺少參數"}), 400
    device_states[mac] = cmd
    return jsonify({"status": "ok"})

@app.route('/get_command/<path:mac>')  # 使用 <path:mac> 支援冒號
def get_command(mac):
    mac = unquote(mac)  # 將 %3A 解碼回冒號
    cmd = device_states.get(mac, "none")
    return jsonify({"cmd": cmd})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
