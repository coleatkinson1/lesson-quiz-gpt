import json
import requests
import os

from pydub import AudioSegment

def join_audio(files, filename):
    combined = AudioSegment.empty()

    # Iterate through each filename in the list
    for fname in files:
        # Load the MP3 file and append it to the combined AudioSegment
        audio_segment = AudioSegment.from_mp3(fname)
        combined += audio_segment

    # Export the combined audio as a single MP3 file
    combined.export(f"./audio/{filename}.mp3", format="mp3")

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
            return filename + ".mp3"
        else:
            print("Failed to download the audio.")
            return False
    except:
        print("Invalid audio data")
        return False

def generate(text, gender="MALE", speaker = "en-NZ-MitchellNeural", filename = "tts_download"):

    try:
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNGQ1NWE3MDQtMGVlNy00M2QyLTk3ODQtODM3ODQwYTk2OWMzIiwidHlwZSI6ImFwaV90b2tlbiJ9.rYCS_Cm33S2sVYcPVxpKnJzx7rTd2myC3BuC3PFs0l4"}

        url = "https://api.edenai.run/v2/audio/text_to_speech"
        payload = {
            "providers": "microsoft", "language": "en-US",
            "settings": {"microsoft": speaker},
            "option": gender,
            "text": text,
            "fallback_providers": ""
        }
        response = requests.post(url, json=payload, headers=headers)

        response.raise_for_status()

        result = json.loads(response.text)

        return download_and_save_mp3(result['microsoft']['audio_resource_url'], filename=filename)
    except:
        print("Error generating TTS")
        return False

def generate_dialogue_from_json(json_data, final_filename):
    try:
        data = json.loads(json_data)
        files = []
        for i, line in enumerate(data['dialogue']):
            output = generate(line['line'], gender=line['gender'], speaker=line['voice'], filename=f"multi_dialogue_{str(i)}")
            files.append(output)

        join_audio(files, final_filename)
    except Exception as e:
        print("Failed to generate dialogue: ", e)

    print("Done")

    
test_json = '''
{
    "dialogue": [
        {
            "name": "Lisa",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "Good afternoon, Radiant Wellness Clinic. Lisa speaking."
        },
        {
            "name": "Client 4",
            "gender": "FEMALE",
            "voice": "en-NZ-MollyNeural",
            "line": "Hello, I didn’t receive my appointment reminder. Could you check my booking?"
        },
        {
            "name": "Lisa",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "Certainly, may I have your name, please?"
        },
        {
            "name": "Client 4",
            "gender": "FEMALE",
            "voice": "en-NZ-MollyNeural",
            "line": "Samantha Lee."
        },
        {
            "name": "Lisa",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "One moment, Ms. Lee... Yes, you have an appointment for a Swedish massage this Saturday at 10 AM. Would you like me to resend the reminder?"
        },
        {
            "name": "Client 4",
            "gender": "FEMALE",
            "voice": "en-NZ-MollyNeural",
            "line": "Please, that would be great."
        },
        {
            "name": "Lisa",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "Done. You should receive it shortly."
        },
        {
            "name": "Client 4",
            "gender": "FEMALE",
            "voice": "en-NZ-MollyNeural",
            "line": "Thank you very much."
        },
        {
            "name": "Lisa",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "My pleasure. See you on Saturday!"
        }
    ]
}
'''
generate_dialogue_from_json(test_json, "listening_dialogue_week6_4")

#generate("Hi, I'm Mia. My expertise lies in Deep Tissue Massage and Acupressure. I utilize deep pressure and manipulation of the body's soft tissues to relieve muscle tension and knots. Acupressure, which involves applying pressure to specific points on the body, complements my technique by targeting areas of pain and discomfort. This approach is ideal for clients suffering from chronic pain or recovering from injuries.", "FEMALE")