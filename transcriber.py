import os
import whisper
from dotenv import load_dotenv
import tempfile
from pydub import AudioSegment

load_dotenv()

class Transcriber:
    def __init__(self):
        self.model = whisper.load_model(os.getenv("WHISPER_MODEL", "base"))
    def convert_to_wav(self, audio_file):
        """Convert audio file to WAV format if needed."""
        if audio_file.name.endswith('.wav'):
            return audio_file.name
        
        #Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_file_path = temp_file.name
        temp_file.close()#close immediately to avoid Windows file lock
        
        #Convert to WAV
        audio = AudioSegment.from_file(audio_file)
        audio.export(temp_file_path, format="wav")  
        
        return temp_file_path
    
    def transcribe(self, audio_file):
        """
        Transcribe audio file to text using Whisper
        
        Args:
            audio_file:File object(mp3 or wav)
            
        Returns:
            str: Transcribed text
        """
        try:
            # Convert to WAV if needed
            wav_file_path = self.convert_to_wav(audio_file)
            #Transcribe
            result = self.model.transcribe(wav_file_path)
            
            #Clean up temporary file
            if wav_file_path != audio_file.name:
                os.unlink(wav_file_path)
            return result["text"]
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    def validate_audio(self, audio_file):
        """

        Validate the audio file format and size.
        Args:
            audio_file: File object
        Returns:
            bool: True if valid 
        """
        if not audio_file:
            raise ValueError("No audio file provided.")
        if not audio_file.name.endswith(('.mp3', '.wav')):
            raise ValueError("Only .mp3 and .wav formats are supported.")
        
        #Check file size (max 25MB)
        if audio_file.size > 25 * 1024 * 1024:
            raise ValueError("File size must be less than 25MB.")
        return True
