from gtts import gTTS

def text_to_speech(text, filename="tts.mp3"):
    tts = gTTS(text, lang='en')
    tts.save(filename)
    return "saved"