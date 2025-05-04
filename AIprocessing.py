import google.generativeai as genai
import json
from PIL import Image, UnidentifiedImageError
import io
import os      # For path manipulation
import shutil  # For moving files


my_image_file_path = "imagesNew/nature-animal-fur-47359.jpeg"
# !!! SECURITY WARNING: Avoid hardcoding API keys. Load from environment variable or secure config. !!!
my_api_key = "" # Replace with your actual key or secure loading method


animal_data_list = []

# --- Load JSON data with error handling ---
jsonFilePath = 'sheet_data.json'
try:
    with open(jsonFilePath, 'r', encoding="utf-8") as f:
        # Assume the JSON root is a list of objects
        animal_data_list = json.load(f)
        if not isinstance(animal_data_list, list):
            print(f"Warning: Expected a list of objects in {jsonFilePath}, but got {type(animal_data_list)}. Resetting to empty list.")
            animal_data_list = []
        elif not animal_data_list:
             print(f"Warning: JSON file {jsonFilePath} loaded as an empty list.")

except FileNotFoundError:
    print(f"Error: JSON file not found at {jsonFilePath}")
    animal_data_list = [] # Ensure list is empty on error
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {jsonFilePath}. Check file validity.")
    animal_data_list = [] # Ensure list is empty on error
except Exception as e:
    print(f"An unexpected error occurred loading JSON: {e}")
    animal_data_list = [] # Ensure list is empty on error
# --- End JSON Loading ---


# --- Define the function ---
def generateAnimalInfo(image_bytes, api_key): # Removed default for api_key to ensure it's always passed
    """
    Identifies an animal from image bytes and returns its corresponding JSON object
    from a predefined list.

    Args:
        image_bytes (bytes): The raw byte content of the animal image.
        api_key (str): Your Google AI API key.

    Returns:
        str: A JSON string representing the identified animal's data object,
             or an error message string.
    """
    global animal_data_list

    if not animal_data_list:
        return json.dumps({"error": "Animal data list is empty or failed to load. Cannot proceed."})

    try:
        # --- 1. Load Image from Bytes ---
        img_file_like = io.BytesIO(image_bytes)
        img = Image.open(img_file_like)

        # --- 2. Configure API Key ---
        # Use the api_key passed into the function
        genai.configure(api_key=api_key)

        # --- 3. Initialize the AI Model ---
        # Specify the correct model name here
        model = genai.GenerativeModel("gemini-1.5-flash") # Using 1.5-flash for vision

        # --- 4. Format Context for Prompt ---
        context_json_string = json.dumps(animal_data_list) # Removed indent to save tokens


        # --- 5. Construct the Text Prompt ---
        prompt_text = (
            f"You are an animal identification assistant. Analyze the provided image.\n"
            f"Below is a list of known animals described as JSON objects:\n"
            f"```json\n{context_json_string}\n```\n"
            f"Identify the single animal from the list that is shown in the image. "
            f"Your response MUST be ONLY the single, complete JSON object corresponding to the identified animal from the list provided above. "
            f"Do not include any other text, explanations, or markdown formatting like ```json ``` around the output JSON object."
        )

        # --- 6. Prepare Multimodal Contents ---
        contents_list = [prompt_text, img]

        # --- 7. Call the API (Vision Model) ---
        # Call generate_content directly on the model instance
        response = model.generate_content(contents_list)

        return response.text

    except UnidentifiedImageError:
         return json.dumps({"error": "Could not identify image format from bytes."})
    except Exception as e:
        # Catch-all for other errors (API connection, model errors, etc.)
        return json.dumps({"error": f"An unexpected error occurred within generateAnimalInfo: {e}"})


# --- Helper function to get image bytes ---
def get_image_bytes(path):
    # Add error handling here too
    try:
        with open(path, "rb") as image_file:
            return image_file.read()
    except FileNotFoundError:
        print(f"Error: Image file not found at {path}")
        return None
    except Exception as e:
        print(f"Error reading image file {path}: {e}")
        return None


try:
     # Check if JSON data loaded successfully before proceeding
     if animal_data_list:
         image_byte_data = get_image_bytes(my_image_file_path)

         # Check if image bytes were loaded successfully
         if image_byte_data:
             # Explicitly pass the configured API key
             json_output_string = generateAnimalInfo(image_byte_data, api_key=my_api_key)
             print("Raw AI Response:")
             print(json_output_string)

             # Attempt to parse the response as JSON
             parsed_successfully = False
             try:
                 # Check if the response indicates an error from generateAnimalInfo
                 # Clean the string first to remove potential leading/trailing whitespace or newlines
                 cleaned_string = json_output_string.strip()
                 potential_error = json.loads(cleaned_string)
                 if isinstance(potential_error, dict) and "error" in potential_error:
                     print(f"\nError from AI processing: {potential_error['error']}")
                 else:
                     # If it's not an error dict, assume it's the expected JSON
                     print("\nParsed JSON Object:")
                     # We already parsed it, just print nicely
                     print(json.dumps(potential_error, indent=2))
                     parsed_successfully = True # Mark as successful if not an error dict
             except json.JSONDecodeError:
                 # This means the raw response was likely not JSON at all
                 print("\nError: AI response was not valid JSON.")
             except Exception as e:
                 print(f"\nError parsing AI response: {e}")

             # --- Move the processed image --- 
             try:
                 source_path = my_image_file_path
                 destination_dir = "imagesOld"
                 filename = os.path.basename(source_path)
                 destination_path = os.path.join(destination_dir, filename)

                 # Create the destination directory if it doesn't exist
                 os.makedirs(destination_dir, exist_ok=True)

                 # Move the file
                 shutil.move(source_path, destination_path)
                 print(f"\nSuccessfully moved '{source_path}' to '{destination_path}'")
             except Exception as move_error:
                 print(f"\nError moving file '{source_path}': {move_error}")
             # --- End file move --- 

         else:
             print("Cannot run identification because the image file failed to load.")
     else:
         print("Cannot run identification because the animal data list failed to load.")

except Exception as e:
     print(f"An critical error occurred during script execution: {e}")
