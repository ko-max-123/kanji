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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    global remaining_data, used_data
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

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    user_input = data.get('answer')
    correct_answer = data.get('correct_answer')

    if user_input == correct_answer:
        return jsonify({"result": "正解◯"})
    else:
        return jsonify({"result": "間違い☓"})

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global remaining_data, used_data
    used_data = []
    remaining_data = data[:]
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True)
