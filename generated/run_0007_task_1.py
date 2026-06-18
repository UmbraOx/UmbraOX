import subprocess
import sys

def install_speech_recognition():
    """
    Install the SpeechRecognition library using pip.
    
    This function attempts to install the SpeechRecognition library via pip.
    It handles potential errors during the installation process and provides feedback to the user.
    """
    try:
        # Ensure pip is installed
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        
        # Install SpeechRecognition
        subprocess.check_call([sys.executable, "-m", "pip", "install", "SpeechRecognition"])
        print("SpeechRecognition library has been successfully installed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to install the SpeechRecognition library: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    install_speech_recognition()
