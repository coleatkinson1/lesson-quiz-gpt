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
            "name": "Anchor",
            "gender": "MALE",
            "voice": "en-NZ-MitchellNeural",
            "line": "Good evening, and welcome to the Health and Wellness segment of our news. Tonight, we spotlight the evolution of massage techniques and how they're revolutionizing the way we approach physical well-being. Our correspondent, Taylor Green, has the story."
        },
        {
            "name": "Taylor Green",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "Thank you. Massage therapy, a practice as ancient as it is therapeutic, has seen remarkable evolution over the centuries. Today, I'm here at the National Wellness Conference, where experts have gathered to discuss the latest advancements in massage techniques."
        },
        {
            "name": "Dr. Maya Chen",
            "gender": "FEMALE",
            "voice": "en-NZ-MollyNeural",
            "line": "Massage therapy has come a long way. From the traditional Swedish massage, known for its gentle and relaxing strokes, to the more intense deep tissue massage, aimed at relieving musculoskeletal issues."
        },
        {
            "name": "Taylor Green",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "Dr. Maya Chen, a renowned physiotherapist, highlights how different techniques cater to diverse needs. For instance, Shiatsu, a Japanese technique, applies pressure to specific points on the body, promoting energy flow and relaxation."
        },
        {
            "name": "Alex Rivera",
            "gender": "MALE",
            "voice": "en-NZ-MitchellNeural",
            "line": "And it's not just about relaxation. Sports massage, for instance, focuses on the needs of athletes, helping them recover from injuries or enhance their performance."
        },
        {
            "name": "Taylor Green",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "That's Alex Rivera, a sports massage therapist. Techniques like trigger point therapy and lymphatic drainage are also gaining popularity for their targeted benefits."
        },
        {
            "name": "Dr. Chen",
            "gender": "FEMALE",
            "voice": "en-NZ-MollyNeural",
            "line": "The beauty of massage therapy lies in its versatility. Techniques like hot stone massage use heated stones to relax muscles deeply, while aromatherapy massage incorporates essential oils for a holistic experience."
        },
        {
            "name": "Taylor Green",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "With such variety, the key is understanding the client's needs. Reflexology, for instance, might be perfect for someone looking for a less conventional approach, applying pressure to the feet or hands to improve health."
        },
        {
            "name": "Anchor",
            "gender": "MALE",
            "voice": "en-NZ-MitchellNeural",
            "line": "Fascinating insights, Taylor. It's clear that the field of massage therapy is as dynamic as it is diverse, with each technique offering unique benefits."
        },
        {
            "name": "Taylor Green",
            "gender": "FEMALE",
            "voice": "en-AU-AnnetteNeural",
            "line": "Absolutely. And as professionals continue to explore and innovate, the future of massage therapy holds even greater promise for holistic health and wellness."
        },
        {
            "name": "Anchor",
            "gender": "MALE",
            "voice": "en-NZ-MitchellNeural",
            "line": "Taylor Green reporting. Thank you for that enlightening feature. Stay with us for more news on how traditional practices are shaping modern health care. Goodnight."
        }
    ]
}
'''
generate_dialogue_from_json(test_json, "mytestdialogue")

#generate("Hi, I'm Mia. My expertise lies in Deep Tissue Massage and Acupressure. I utilize deep pressure and manipulation of the body's soft tissues to relieve muscle tension and knots. Acupressure, which involves applying pressure to specific points on the body, complements my technique by targeting areas of pain and discomfort. This approach is ideal for clients suffering from chronic pain or recovering from injuries.", "FEMALE")