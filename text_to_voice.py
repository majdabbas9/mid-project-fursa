from elevenlabs import stream
from elevenlabs.client import ElevenLabs
client = ElevenLabs(
  api_key='sk_97626aa783f9fc81d994823343236e3e240f0b4415a178eb',
)
audio_stream = client.text_to_speech.convert_as_stream(
    text="This is a test",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2"
)

# option 1: play the streamed audio locally

stream(audio_stream)

# option 2: process the audio bytes manually

# for chunk in audio_stream:
#     if isinstance(chunk, bytes):
#         print(chunk)