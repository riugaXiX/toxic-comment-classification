from openai import OpenAI
client = OpenAI(api_key='Your_api_key')


# client.api_key = 'proj_90qazmQpXcnqXACqHVvK63IZ'

audio_file= open("tes2.mp3", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)