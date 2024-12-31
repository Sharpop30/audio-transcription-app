from gtts import gTTS

# Create a test message in Arabic
text = """مرحباً! هذا اختبار لخدمة تحويل الصوت إلى نص.
نحن نختبر القدرة على تحويل الكلام باللغة العربية إلى نص باستخدام تقنية ويسبر من أوبن اي.
هذا الاختبار يتضمن عدة جمل للتأكد من دقة التحويل."""

# Create the audio file
tts = gTTS(text=text, lang='ar', slow=False)
tts.save("test_audio_arabic.mp3")
