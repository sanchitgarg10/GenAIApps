from flask import Flask, render_template, request
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os

app = Flask(__name__)

# Retrieve endpoint and key from environment variables
endpoint = os.environ.get('AZURE_ENDPOINT')
key = os.environ.get('AZURE_KEY')

# Create a Text Analytics client
credential = AzureKeyCredential(key)
ai_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

@app.route('/sentiment-analysis', methods=['GET', 'POST'])
def sentiment_analysis():
    if request.method == 'POST':
        text_to_analyze = [request.form['text_to_analyze']]
        sentiment_response = ai_client.analyze_sentiment(documents=text_to_analyze)
        key_phrases_response = ai_client.extract_key_phrases(documents=text_to_analyze)
        return render_template('sentiment_analysis.html', 
                               sentiment=sentiment_response[0].sentiment, 
                               key_phrases=key_phrases_response[0].key_phrases)
    return render_template('sentiment_analysis.html', sentiment=None, key_phrases=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
