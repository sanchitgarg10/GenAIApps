from flask import Flask, render_template, request
from sentiment_analysis import sentiment_analysis_bp

app = Flask(__name__)

app.register_blueprint(sentiment_analysis_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
