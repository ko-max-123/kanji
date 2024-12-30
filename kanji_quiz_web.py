from flask import Flask, render_template, request, jsonify, redirect, url_for
import random
import os

app = Flask(__name__)

# 部屋情報管理
rooms = {}
room_participants = {}

# メニュー画面
@app.route('/')
def index():
    return render_template('menu.html')

# 一人プレイ画面
@app.route('/single_player')
def single_player():
    return render_template('index.html')

# 二人プレイ - 部屋選択画面
@app.route('/multi_player')
def multi_player():
    return render_template('room_select.html')

# 部屋作成API
@app.route('/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name')
    if room_name and room_name not in rooms:
        rooms[room_name] = []
        room_participants[room_name] = 0
        return jsonify({"status": "success", "room_name": room_name})
    return jsonify({"status": "error", "message": "部屋名が重複しています。"})

# 部屋一覧API
@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    return jsonify({"rooms": list(rooms.keys())})

# ロビー画面
@app.route('/lobby/<room_name>')
def lobby(room_name):
    if room_name not in rooms:
        return redirect(url_for('multi_player'))
    participants = room_participants.get(room_name, 0)
    return render_template('lobby.html', room_name=room_name, participants=participants)

# 参加者数更新API
@app.route('/update_participants/<room_name>', methods=['POST'])
def update_participants(room_name):
    action = request.json.get('action')
    if room_name in room_participants:
        if action == "enter":
            room_participants[room_name] += 1
        elif action == "leave" and room_participants[room_name] > 0:
            room_participants[room_name] -= 1
    return jsonify({"participants": room_participants[room_name]})

# テスト終了API
@app.route('/end_test/<room_name>', methods=['POST'])
def end_test(room_name):
    if room_name in rooms:
        del rooms[room_name]
        del room_participants[room_name]
    return jsonify({"status": "success"})

# サーバー起動
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
