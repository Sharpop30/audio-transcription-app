# Audio Transcription App

A web application that allows users to upload audio files and receive transcriptions in their desired language using OpenAI's Whisper API. The application supports multiple languages, including Arabic, and can handle large audio files by automatically splitting them into manageable chunks.

## Requirements

### 1. System Requirements
- Windows, macOS, or Linux operating system
- Python 3.8 or higher
- FFmpeg (included in the repository)
- 2GB RAM minimum (4GB recommended)
- Sufficient disk space for audio processing

### 2. API Requirements
- OpenAI API key (get one from https://platform.openai.com/api-keys)
  - Free tier available
  - Pay-as-you-go pricing for larger usage

### 3. Python Dependencies
```bash
flask==3.0.0
openai>=1.6.1
python-dotenv==1.0.0
pydub==0.25.1
Werkzeug==3.0.1
```

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sharpop30/audio-transcription-app.git
   cd audio-transcription-app
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **FFmpeg Setup**
   - FFmpeg is already included in the repository
   - No additional setup required

## Usage

1. **Start the Application**
   ```bash
   python app.py
   ```

2. **Access the Web Interface**
   - Open your web browser
   - Go to `http://127.0.0.1:5000`

3. **Using the Application**
   - Enter your OpenAI API key in the setup section
   - Select an audio file (supported formats: MP3, WAV, M4A, OGG)
   - Choose the target language
   - Click "Transcribe"
   - Wait for the transcription to complete

## Features

- **Multiple Language Support**
  - Arabic (العربية)
  - English
  - Spanish
  - French
  - German
  - Italian
  - Portuguese
  - Dutch
  - Russian
  - Japanese
  - Korean
  - Chinese
  - And more...

- **Large File Support**
  - Handles files larger than 15MB
  - Automatic file splitting and processing
  - Progress tracking for large files

- **Security Features**
  - API keys stored locally in browser
  - No server-side API key storage
  - Secure file handling

## File Format Support

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)

## Limitations

- Maximum file size: 16GB
- Audio quality affects transcription accuracy
- Internet connection required
- API usage subject to OpenAI's pricing and rate limits

## Troubleshooting

1. **FFmpeg Issues**
   - If you see FFmpeg-related errors, ensure the application has access to the ffmpeg folder
   - The ffmpeg folder should be in the same directory as app.py

2. **API Key Issues**
   - Ensure your OpenAI API key is valid
   - Check if you have sufficient credits in your OpenAI account
   - Make sure you're connected to the internet

3. **File Upload Issues**
   - Check if the file format is supported
   - Ensure the file isn't corrupted
   - For large files, be patient during upload and processing

## Support

For issues, questions, or contributions, please:
1. Open an issue on GitHub
2. Submit a pull request
3. Contact the maintainer

## License

This project is licensed under the MIT License - see the LICENSE file for details.
