import json
import requests
import os

from pydub import AudioSegment

def download_and_save_mp3(url, filename = "tts_download"):
    try:
        response = requests.get(url)

        response.raise_for_status()
        
        if response.status_code == 200:
            with open(filename + '.temp', 'wb') as f:
                f.write(response.content)
            
            # Load the audio from the temporary file
            audio = AudioSegment.from_file(filename + '.temp')
            
            # Save the audio as MP3
            audio.export(filename + '.mp3', format="mp3")
            
            # Remove the temporary file
            os.remove(filename + '.temp')
            print(f"MP3 file saved as {filename}.mp3")
        else:
            print("Failed to download the audio.")
    except:
        print("Invalid audio data")

def generate(text, gender="MALE"):
    try:
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNGQ1NWE3MDQtMGVlNy00M2QyLTk3ODQtODM3ODQwYTk2OWMzIiwidHlwZSI6ImFwaV90b2tlbiJ9.rYCS_Cm33S2sVYcPVxpKnJzx7rTd2myC3BuC3PFs0l4"}

        url = "https://api.edenai.run/v2/audio/text_to_speech"
        payload = {
            "providers": "microsoft", "language": "en-US",
            "settings": {"microsoft": "en-NZ-MitchellNeural"},
            "option": gender,
            "text": text,
            "fallback_providers": ""
        }
        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()

        result = json.loads(response.text)

        download_and_save_mp3(result['microsoft']['audio_resource_url'])
    except:
        print("Error generating TTS")


generate("Hi, I'm Mia. My expertise lies in Deep Tissue Massage and Acupressure. I utilize deep pressure and manipulation of the body's soft tissues to relieve muscle tension and knots. Acupressure, which involves applying pressure to specific points on the body, complements my technique by targeting areas of pain and discomfort. This approach is ideal for clients suffering from chronic pain or recovering from injuries.", "FEMALE")