import os
import pickle
import speech_recognition as sr
from openai import OpenAI
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

class AudioProcessor:
    def __init__(self, model_path, tokenizer_path):
        # Load LSTM model
        self.model = load_model(model_path)
        
        # Load tokenizer
        with open(tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key='Your_api_key')

    def upload_audio_to_folder(self, audio_file, folder_path):
        # Create folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Save audio file to the folder
        audio_file_path = os.path.join(folder_path, audio_file.name)
        with open(audio_file_path, "wb") as f:
            f.write(audio_file.getbuffer())
        
        return audio_file_path

    def cleanup_files(self, folder_path):
        # Delete all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    def recognize_text_from_audio(self, audio_file_path):
        try:
            # Recognize audio using speech recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
            recognized_text = recognizer.recognize_google(audio_data)
            
            return recognized_text
        except Exception as e:
            print(f"An error occurred during audio recognition: {str(e)}")
            return None

    def preprocess_text(self, text, max_length):
        sequences = self.tokenizer.texts_to_sequences([text])
        padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post')
        return padded_sequences

    def predict_toxicity(self, text):
        data = [text]
        max_length = 100  # Adjust according to your model's input shape
        processed_text = self.preprocess_text(data, max_length)
        predictions = self.model.predict(processed_text)

        # Nama label sesuai urutan
        labels = ['pornografi', 'sara', 'radikalisme', 'pencemaran_nama_baik']

        # Tentukan ambang batas
        threshold = 0.5

        # Konversi probabilitas ke label 0 atau 1
        binary_predictions = (predictions > threshold).astype(int)

        # Kaitkan hasilnya dengan nama label
        predicted_labels = {labels[i]: (predictions[0, i], binary_predictions[0, i]) for i in range(len(labels))}

        # Membuat daftar label dan skor yang punya nilai 1
        detected_labels_with_scores = [(label, score) for label, (score, binary_value) in predicted_labels.items() if binary_value == 1]

        # Membuat pesan hasil prediksi
        if detected_labels_with_scores:
            detected_labels_str = ', '.join([f"{label} (score: {score:.4f})" for label, score in detected_labels_with_scores])
            message = f"Comment anda mengandung kata kata: {detected_labels_str}"
        else:
            message = "Comment anda tidak mengandung kata kata berbahaya."

        # Menampilkan pesan
        return message

    def transcribe_audio(self, audio_file):
        try:
            audio_file_path = self.upload_audio_to_folder(audio_file, 'audio')
            
            # Using OpenAI Whisper model for transcription
            with open(audio_file_path, "rb") as f:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=f
                )
            
            recognized_text = response.text
            return recognized_text
        except Exception as e:
            print(f"An error occurred during audio transcription: {str(e)}")
            return None
        finally:
            self.cleanup_files('audio')
