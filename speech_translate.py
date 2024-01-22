from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
import whisper
from werkzeug.utils import secure_filename
import moviepy.editor as mp
import requests, uuid, json

# Initialize Blueprint
speech_translate_bp = Blueprint('speech_translate', __name__)

# Azure Credentials
translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
translator_endpoint = "https://api.cognitive.microsofttranslator.com"
translator_location = os.environ.get("AZURE_TRANSLATOR_LOCATION")

# Supported Languages for Translation
languages = {
    "en": "English",
    "hi": "Hindi",
    "pa": "Punjabi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "zh-Hans": "Chinese (Simplified)"
    # Add more languages as needed
}

def convert_mp4_to_mp3(mp4_path, mp3_path):
    clip = mp.VideoFileClip(mp4_path)
    clip.audio.write_audiofile(mp3_path)

def extract_text_from_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

def translate_text(text, target_language):
    path = '/translate'
    constructed_url = translator_endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': translator_location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    return response.json()

@speech_translate_bp.route('/speech-translate', methods=['GET', 'POST'])
def speech_translate():
    transcription = ""
    translation = ""
    target_language = "en"  # Initialize with a default value like 'en' for English
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            #flash('No file selected')
            return redirect(url_for('speech_translate.speech_translate'))

        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)

        target_language = request.form.get('target_language', 'en')  # Get target_language from form data
        if not target_language:
            #flash('No target language selected')
            return redirect(url_for('speech_translate.speech_translate'))

        # Convert MP4 to MP3 if necessary and extract text
        if filename.lower().endswith(".mp4"):
            mp3_file_path = os.path.splitext(file_path)[0] + ".mp3"
            convert_mp4_to_mp3(file_path, mp3_file_path)
            transcription = extract_text_from_audio(mp3_file_path)
        elif filename.lower().endswith(".mp3"):
            transcription = extract_text_from_audio(file_path)
        else:
            #flash('File format not supported')
            return redirect(url_for('speech_translate.speech_translate'))

        target_language = request.form['target_language']
        translation_response = translate_text(transcription, target_language)

        if translation_response and 'translations' in translation_response[0]:
            translation = translation_response[0]['translations'][0]['text']

        # Clean up uploaded file
        os.remove(file_path)

    return render_template('speech_translate.html', transcription=transcription, translation=translation, language=languages.get(target_language, "Unknown"), languages=languages)

# Additional app setup and run configurations
# ...
