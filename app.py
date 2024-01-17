from flask import Flask, render_template, request
from sentiment_analysis import sentiment_analysis_bp

app = Flask(__name__)

## Call landing page
@app.route('/')
def index():
    return render_template('index.html')

##Call Sentiment analysis
app.register_blueprint(sentiment_analysis_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
