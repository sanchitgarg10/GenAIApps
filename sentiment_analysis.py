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
        # Perform sentiment analysis
        sentiment_response = ai_client.analyze_sentiment(documents=[text_to_analyze])
        # Perform key phrase extraction
        key_phrases_response = ai_client.extract_key_phrases(documents=[text_to_analyze])
        # Perform entity recognition
        entities_response = ai_client.recognize_entities(documents=[text_to_analyze])
        # Perform linked entity recognition
        linked_entities_response = ai_client.recognize_linked_entities(documents=[text_to_analyze])
        
        # Pass the results back to the template
        return render_template('sentiment_analysis.html',
                               text_to_analyze=text_to_analyze,
                               sentiment=sentiment_response[0].sentiment,
                               key_phrases=key_phrases_response[0].key_phrases,
                               entities=entities_response[0].entities,
                               linked_entities=linked_entities_response[0].entities)
    else:
        # For GET requests, just render the template
        return render_template('sentiment_analysis.html', text_to_analyze=text_to_analyze)
