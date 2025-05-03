from google import genai
import json

jsonFilePath = 'sheet_data.json'
animals = []

with open(jsonFilePath, 'r') as f:
    data = json.load(f)
    animals = data.get('Scientific Name', [])

def generateAnimalInfo(input):
    client = genai.Client(api_key="YOUR_API_KEY")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Identify the animal you see in this picture"+input+"from the following list:" 
        + animals
    )

    return response.text