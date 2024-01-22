from flask import Flask, render_template, request
from sentiment_analysis import sentiment_analysis_bp
from speech_translate import speech_translate_bp
from speechtotext import speechtotext_bp
from multiagent import multiagent_bp

app = Flask(__name__)

## Call landing page
@app.route('/')
def index():
    return render_template('index.html')

##Register blueprints
app.register_blueprint(sentiment_analysis_bp)
app.register_blueprint(speechtotext_bp)
app.register_blueprint(speech_translate_bp)
app.register_blueprint(multiagent_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
