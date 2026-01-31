from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

API_BASE_URL = 'https://51.75.118.17:20126'

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/<path:api_path>', methods=['GET', 'POST'])
def proxy_api(api_path):
    try:
        url = f"{API_BASE_URL}/{api_path}"
        
        if request.method == 'GET':
            response = requests.get(url, verify=False, timeout=10)
        else:
            response = requests.post(url, json=request.json, verify=False, timeout=10)
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": f"فشل الاتصال بالخادم: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"خطأ في الخادم: {str(e)}"
        }), 500

@app.route('/api', methods=['GET'])
def api_root():
    try:
        response = requests.get(API_BASE_URL, verify=False, timeout=5)
        return jsonify({
            "status": "success",
            "message": "API متصل",
            "timestamp": response.json().get('timestamp', '')
        })
    except:
        return jsonify({
            "status": "error",
            "message": "API غير متصل"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)