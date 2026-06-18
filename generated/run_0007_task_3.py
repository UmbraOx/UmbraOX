"""
This script captures audio input from the microphone and transcribes it into text using Google's Speech Recognition API.
"""

import speech_recognition as sr

def transcribe_audio():
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Please speak something...")
        
        # Adjust for ambient noise levels
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Capture audio from the microphone
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Transcribe the captured audio
            print("Transcribing...")
            text = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {text}")
        
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == '__main__':
    transcribe_audio()
