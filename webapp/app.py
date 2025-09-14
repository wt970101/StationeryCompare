from flask import Flask, render_template, request, jsonify
from webapp.modules import sta_compare

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/scraper/compare_list/<keyword>', methods=['GET'])
def compare_list(keyword):
    data = sta_compare.get_compare_data(keyword)
    # 將資料整理成前端使用的格式
    jsonData = []
    for pname, items in data.items():
        jsonData.append({
            'name': pname,
            'items': [{'store': i['store'], 'price_unit': i['price_unit']} for i in items]
        })
    return jsonify({'jsonData': jsonData})
