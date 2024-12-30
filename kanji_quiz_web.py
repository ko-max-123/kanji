from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# 漢字データの読み込み
def load_kanji_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = [line.strip().split() for line in file.readlines()]
        return data
    except FileNotFoundError:
        return []

# データ初期化
data = load_kanji_data("kannji.txt")
used_data = []
remaining_data = data[:]

# 部屋情報管理
rooms = []  # 現在作成されている部屋のリスト

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
    return render_template('room_select.html', rooms=rooms)

# 部屋作成API
@app.route('/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name')
    if room_name and room_name not in rooms:
        rooms.append(room_name)
        return jsonify({"status": "success", "rooms": rooms})
    return jsonify({"status": "error", "message": "部屋名が重複しています。"})

# 部屋一覧API
@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    return jsonify({"rooms": rooms})

# サーバー起動
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render用の環境変数PORTを取得
    app.run(host='0.0.0.0', port=port)
