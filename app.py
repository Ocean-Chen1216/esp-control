from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ 加這行

app = Flask(__name__)
CORS(app)  # ✅ 允許跨網域請求

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

@app.route('/get_command/<mac>')
def get_command(mac):
    cmd = device_states.get(mac, "none")
    return jsonify({"cmd": cmd})
