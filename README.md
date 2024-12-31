# Audio Transcription App

This is a web application that allows users to upload audio files and receive transcriptions in their desired language using OpenAI's Whisper API.

## Features

- Upload audio files (supports MP3, WAV, M4A, and OGG formats)
- Support for files larger than 16GB (automatically splits into chunks)
- Multiple language support including Arabic
- Real-time transcription using OpenAI's Whisper API
- Simple and intuitive user interface
- Secure API key management (stored in browser's local storage)

## Prerequisites

1. Python 3.8 or higher
2. FFmpeg (required for audio processing)
   - Windows: Download from https://ffmpeg.org/download.html
   - Add FFmpeg to your system PATH

3. OpenAI API key (users will input their own key in the web interface)

## Setup

1. Install FFmpeg:
   - Download FFmpeg from https://ffmpeg.org/download.html
   - Extract the files
   - Add the bin folder to your system PATH

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and go to `http://localhost:5000`

## Usage

1. Enter your OpenAI API key in the setup section
   - Get your API key from https://platform.openai.com/api-keys
   - The key is stored securely in your browser's local storage
   - Never shared or stored on the server

2. Click "Choose File" to select an audio file
3. Select the desired target language from the dropdown
4. Click "Transcribe"
5. For files larger than 15MB, you'll see a progress indicator
6. The transcription will appear below once complete

## Supported File Types

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)

## Large File Handling

- Files larger than 15MB will be automatically split into chunks
- Each chunk is processed separately and then combined
- Progress is shown for large file processing
- Supports files up to 16GB

## Security Notes

- API keys are never stored on the server
- Keys are stored locally in your browser's localStorage
- Each request requires the API key to be sent
- Use HTTPS in production to ensure secure transmission of API keys
