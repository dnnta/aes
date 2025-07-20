from flask import Flask, render_template, request
from aes_logic import encrypt_aes, decrypt_aes

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    rounds_info = None

    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']
        mode = request.form['mode']
        action = request.form['action']

        try:
            if action == 'Encrypt':
                result, rounds_info = encrypt_aes(text, key, mode)
            else:
                result, rounds_info = decrypt_aes(text, key, mode)
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result, rounds_info=rounds_info)

if __name__ == '__main__':
    # 生产环境配置
    app.run(host='0.0.0.0', port=5000, debug=False)