from gtts import gTTS

# Create a test message
text = """Hello! This is a test audio file for our transcription service. 
We're testing the ability to transcribe speech into text using OpenAI's Whisper API.
This test includes multiple sentences to ensure accurate transcription."""

# Create the audio file
tts = gTTS(text=text, lang='en', slow=False)
tts.save("test_audio.mp3")
