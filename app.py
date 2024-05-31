from flask import Flask, render_template, jsonify
from selenium_script import get_trending_topics, save_to_mongo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    trending_topics = get_trending_topics()
    record = save_to_mongo(trending_topics)
    return jsonify(record)

if __name__ == "__main__":
    app.run(debug=True)
