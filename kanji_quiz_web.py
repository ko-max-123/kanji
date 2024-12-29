from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# 漢字データの読み込み
def load_kanji_data(filename):
    try:
        # ファイルの存在確認と読み込み
        if not os.path.exists(filename):
            print(f"Error: {filename} not found.")
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            data = [line.strip().split() for line in file.readlines()]
        if not data:
            print("Error: ファイルが空です。")
        return data
    except Exception as e:
        print(f"Error loading file: {e}")
        return []

# データ初期化
data = load_kanji_data("kannji.txt")
if not data:
    print("データが読み込めませんでした。")
used_data = []
remaining_data = data[:]

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Template rendering error: {e}")
        return "Internal Server Error", 500

@app.route('/get_question', methods=['GET'])
def get_question():
    global remaining_data, used_data
    try:
        if not remaining_data:
            return jsonify({"status": "complete", "message": "クリア！"})

        question = random.choice(remaining_data)
        remaining_data.remove(question)
        used_data.append(question)

        return jsonify({
            "status": "question",
            "kanji": question[0],
            "yomi": question[1]
        })
    except Exception as e:
        print(f"Error getting question: {e}")
        return jsonify({"status": "error", "message": "エラーが発生しました。"}), 500

@app.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        data = request.get_json()
        user_input = data.get('answer')
        correct_answer = data.get('correct_answer')

        if user_input == correct_answer:
            return jsonify({"result": "正解◯"})
        else:
            return jsonify({"result": "間違い☓"})
    except Exception as e:
        print(f"Error checking answer: {e}")
        return jsonify({"result": "エラーが発生しました。"}), 500

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global remaining_data, used_data
    try:
        used_data = []
        remaining_data = data[:]
        return jsonify({"status": "reset"})
    except Exception as e:
        print(f"Error resetting game: {e}")
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))  # Render用の環境変数PORTを取得
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Server startup error: {e}")
