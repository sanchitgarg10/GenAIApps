from flask import Blueprint, render_template, request
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import os

# Retrieve endpoint and key from environment variables
endpoint = os.environ.get('AZURE_ENDPOINT')
key = os.environ.get('AZURE_KEY')

# Create a Text Analytics client
credential = AzureKeyCredential(key)
ai_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

sentiment_analysis_bp = Blueprint('sentiment_analysis', __name__)

@sentiment_analysis_bp.route('/sentiment-analysis', methods=['GET', 'POST'])
def sentiment_analysis():
    text_to_analyze = ""
    if request.method == 'POST':
        text_to_analyze = request.form['text_to_analyze']
        # ... Azure API calls ...
        return render_template('sentiment_analysis.html',
                               text_to_analyze=text_to_analyze,
                               sentiment=sentiment_response[0].sentiment,
                               key_phrases=key_phrases_response[0].key_phrases,
                               entities=entities_response[0].entities)
    return render_template('sentiment_analysis.html', text_to_analyze=text_to_analyze)