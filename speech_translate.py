from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, ResultReason
from azure.cognitiveservices.speech.translation import TranslationRecognizer, SpeechTranslationConfig
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig, ResultReason, CancellationReason


# Initialize Blueprint
speech_translate_bp = Blueprint('speech_translate', __name__)

# Azure Credentials (Set these as environment variables or replace with actual values)
speech_key = os.environ.get("AZURE_SPEECH_KEY")
service_region = os.environ.get("AZURE_SERVICE_REGION")

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

@speech_translate_bp.route('/speech-translate', methods=['GET', 'POST'])
def speech_translate():
    if request.method == 'POST':
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(url_for('speech_translate.speech_translate'))
        file = request.files['file']
        if file.filename == '':
            #flash('No selected file')
            return redirect(url_for('speech_translate.speech_translate'))

        if file:
            target_language = request.form['target_language']
            filename = secure_filename(file.filename)
            file_path = os.path.join('/tmp', filename)
            file.save(file_path)

            # Check if Azure Speech API keys are provided
            #if not speech_key or not service_region:
                #flash('Azure Key missing')
                #return redirect(request.base_url)


            # Initialize speech config
            speech_config = SpeechConfig(subscription=speech_key, region=service_region)
            audio_config = AudioConfig(filename=file_path)
            print(speech_key)
            print(service_region)


           # Recognize and translate
            translation_config = SpeechTranslationConfig(subscription=speech_key, region=service_region)
            translation_config.speech_recognition_language = "en-US"  # Setting input language as English
            translation_config.add_target_language(target_language)
            recognizer = TranslationRecognizer(translation_config=translation_config, audio_config=audio_config)
            result = recognizer.recognize_once()

            print(result)
            print(result.text)

            if result.reason == ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print("Cancellation reason: ", cancellation_details.reason)
                if cancellation_details.reason == CancellationReason.Error:
                    print("Error details: ", cancellation_details.error_details)

            if result.reason == ResultReason.TranslatedSpeech:
                return render_template('speech_translate.html', 
                                    transcription=result.text, 
                                    translation=result.translations[target_language],
                                    language=languages[target_language],
                                    languages=languages)
            else:
                #flash('Translation failed')
                return redirect(url_for('speech_translate.speech_translate'))

    return render_template('speech_translate.html', languages=languages)

