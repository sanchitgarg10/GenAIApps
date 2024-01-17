from flask import Blueprint, render_template, request
import whisper
import moviepy.editor as mp
import os

# Create a Blueprint
audiototext_bp = Blueprint('audiototext', __name__, template_folder='templates')

# Function to convert MP4 to MP3
def convert_mp4_to_mp3(mp4_path, mp3_path):
    clip = mp.VideoFileClip(mp4_path)
    clip.audio.write_audiofile(mp3_path)

# Route for audio-to-text functionality
@audiototext_bp.route('/whisper', methods=['GET', 'POST'])
def whisper_transcribe():
    transcription = ""
    if request.method == 'POST':
        file = request.files['audiofile']
        filename = file.filename
        file_path = os.path.join('uploads', filename)

        # Ensure 'uploads' directory exists
        os.makedirs('uploads', exist_ok=True)

        if filename.endswith('.mp4'):
            mp3_path = file_path.replace('.mp4', '.mp3')
            file.save(file_path)
            convert_mp4_to_mp3(file_path, mp3_path)
            os.remove(file_path)
            audio_path = mp3_path
        elif filename.endswith('.mp3'):
            file.save(file_path)
            audio_path = file_path
        else:
            return 'File format not supported', 400

        # Load model and transcribe audio
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        transcription = result["text"]

        # Clean up uploaded file
        os.remove(audio_path)

    return render_template('whisper.html', transcription=transcription)

