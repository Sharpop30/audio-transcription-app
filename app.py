import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import tempfile
import math

load_dotenv()

# Set FFmpeg path with absolute paths
app_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_path = os.path.join(app_dir, 'ffmpeg', 'ffmpeg-7.1-essentials_build', 'bin')
ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
ffprobe_exe = os.path.join(ffmpeg_path, 'ffprobe.exe')

os.environ["PATH"] += os.pathsep + ffmpeg_path
os.environ["FFMPEG_BINARY"] = ffmpeg_exe
os.environ["FFPROBE_BINARY"] = ffprobe_exe

# Configure pydub to use the FFmpeg path
AudioSegment.converter = ffmpeg_exe
AudioSegment.ffmpeg = ffmpeg_exe
AudioSegment.ffprobe = ffprobe_exe

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 17 * 1024 * 1024 * 1024  # 17GB max file size
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg'}
CHUNK_SIZE = 15 * 1024 * 1024  # 15MB chunks for API limit

# Ensure the uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_audio(audio_path):
    """Split audio file into chunks of approximately CHUNK_SIZE."""
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio)
    
    # Calculate chunk size in milliseconds
    file_size = os.path.getsize(audio_path)
    chunk_duration = math.floor((CHUNK_SIZE / file_size) * duration)
    
    chunks = []
    for i in range(0, duration, chunk_duration):
        chunk = audio[i:i + chunk_duration]
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            chunk.export(temp_file.name, format='mp3')
            chunks.append(temp_file.name)
    
    return chunks

def transcribe_chunk(chunk_path, language, api_key):
    """Transcribe a single chunk of audio."""
    try:
        with open(chunk_path, 'rb') as audio_file:
            # Create a new OpenAI client with the provided API key
            client = OpenAI(api_key=api_key)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language
            )
            return transcript.text
    except Exception as e:
        if 'api_key' in str(e).lower():
            raise ValueError("Invalid API key. Please check your OpenAI API key.")
        raise e

def cleanup_chunks(chunk_files):
    """Remove temporary chunk files."""
    for chunk_file in chunk_files:
        try:
            os.remove(chunk_file)
        except Exception:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    target_language = request.form.get('language', 'en')
    api_key = request.form.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'Please provide an OpenAI API key'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        
        if file_size > CHUNK_SIZE:
            # Large file handling
            chunks = split_audio(filepath)
            transcriptions = []
            
            try:
                for chunk in chunks:
                    chunk_text = transcribe_chunk(chunk, target_language, api_key)
                    transcriptions.append(chunk_text)
                
                # Combine all transcriptions
                final_transcription = ' '.join(transcriptions)
            finally:
                # Clean up chunk files
                cleanup_chunks(chunks)
        else:
            # Small file handling
            final_transcription = transcribe_chunk(filepath, target_language, api_key)
        
        # Clean up the original uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'transcription': final_transcription
        })
        
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use environment variables for host and port
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
