from flask import Flask, render_template, request
import os
import sys
import json

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from aes_logic import encrypt_aes, decrypt_aes

# 创建Flask应用，使用相对路径查找模板
app = Flask(__name__, 
           template_folder='templates')

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

# Vercel入口点
def lambda_handler(event, context):
    with app.test_client() as client:
        if event['httpMethod'] == 'GET':
            response = client.get('/')
        elif event['httpMethod'] == 'POST':
            # 解析POST数据
            body = event.get('body', '')
            if event.get('headers', {}).get('content-type', '').startswith('application/json'):
                data = json.loads(body)
            else:
                # 解析表单数据
                from urllib.parse import parse_qs
                data = parse_qs(body)
                # 转换为Flask期望的格式
                data = {k: v[0] if v else '' for k, v in data.items()}
            
            response = client.post('/', data=data)
        else:
            return {
                'statusCode': 405,
                'body': 'Method not allowed'
            }
        
        return {
            'statusCode': response.status_code,
            'headers': {
                'Content-Type': 'text/html',
                'Access-Control-Allow-Origin': '*'
            },
            'body': response.data.decode('utf-8')
        } 