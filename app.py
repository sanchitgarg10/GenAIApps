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

@app.route('/prodadvid')
def prodadvid():
    return render_template('prodadvid.html')

@app.route('/custgpttut')
def custgpttut():
    return render_template('custgpttut.html')

@app.route('/exp')
def exp():
    return render_template('exp.html')

@app.route('/phi2')
def phi2():
    return render_template('phi2.html')

@app.route('/ccgmailplugin')
def ccgmailplugin():
    return render_template('ccgmailplugin.html')


##Register blueprints
app.register_blueprint(sentiment_analysis_bp)
app.register_blueprint(speechtotext_bp)
app.register_blueprint(speech_translate_bp)
app.register_blueprint(multiagent_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
