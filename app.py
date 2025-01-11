import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
from pydub import AudioSegment
import tempfile
import math

load_dotenv()

app = Flask(__name__)

def split_audio(file_path, chunk_duration_ms=300000):  # 5 minutes in milliseconds
    """Split audio file into chunks if it's longer than chunk_duration_ms."""
    try:
        audio = AudioSegment.from_file(file_path)
        duration_ms = len(audio)
        
        if duration_ms <= chunk_duration_ms:
            return [file_path]  # Return original file if it's short enough
        
        # Calculate number of chunks needed
        num_chunks = math.ceil(duration_ms / chunk_duration_ms)
        chunks = []
        
        for i in range(num_chunks):
            start_ms = i * chunk_duration_ms
            end_ms = min((i + 1) * chunk_duration_ms, duration_ms)
            
            # Extract chunk
            chunk = audio[start_ms:end_ms]
            
            # Save chunk to temporary file
            chunk_path = os.path.join(tempfile.gettempdir(), f"chunk_{i}.mp3")
            chunk.export(chunk_path, format="mp3")
            chunks.append(chunk_path)
        
        return chunks
    except Exception as e:
        print(f"Error splitting audio: {str(e)}")
        raise

def transcribe_chunk(chunk_path, language, api_key):
    """Transcribe a single chunk of audio."""
    try:
        with open(chunk_path, 'rb') as audio_file:
            # Create a new OpenAI client with the provided API key
            openai.api_key = api_key
            
            # Call the OpenAI API
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language=language
            )
            return response["text"]
    except Exception as e:
        if "Invalid API key" in str(e):
            raise ValueError("Invalid API key. Please check your OpenAI API key.")
        raise e

def cleanup_chunks(chunk_files):
    """Remove temporary chunk files."""
    for chunk_file in chunk_files:
        if os.path.exists(chunk_file):
            try:
                os.remove(chunk_file)
            except Exception as e:
                print(f"Error removing chunk file {chunk_file}: {str(e)}")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        target_language = request.form.get('language', 'en')
        api_key = request.form.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'Please provide an OpenAI API key'}), 400
        
        # Save uploaded file temporarily
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, file.filename)
        file.save(filepath)
        
        try:
            # Get file size
            file_size = os.path.getsize(filepath)
            large_file_threshold = 25 * 1024 * 1024  # 25MB
            
            if file_size > large_file_threshold:
                # Handle large file
                chunks = split_audio(filepath)
                transcriptions = []
                
                try:
                    for chunk in chunks:
                        chunk_text = transcribe_chunk(chunk, target_language, api_key)
                        transcriptions.append(chunk_text)
                    
                    # Combine all transcriptions
                    final_transcription = ' '.join(transcriptions)
                finally:
                    cleanup_chunks(chunks)
            else:
                # Small file handling
                final_transcription = transcribe_chunk(filepath, target_language, api_key)
            
            # Clean up the original uploaded file
            os.remove(filepath)
            
            return jsonify({
                'transcription': final_transcription
            })
            
        except ValueError as ve:
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
