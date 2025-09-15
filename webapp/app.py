from flask import Flask, request, jsonify, render_template
from webapp.modules import sta_compare

app = Flask(__name__)
app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html', page_title="比價平台")

@app.route('/search')
def search():
    query = request.args.get('query', '') # 搜尋的關鍵字
    print("搜尋關鍵字:", query)
    results = sta_compare.get_data(query)
    print("回傳結果:", results)
    return jsonify(results) 