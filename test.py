# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# MODEL_PATH = "microsoft/Phi-3.5-mini-instruct"

# # Load tokenizer
# tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)  

# # Load model
# model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")

# # Generate text
# prompt = "Tell me an interesting story about a time traveler."

# inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

# with torch.no_grad():
#     outputs = model.generate(**inputs, max_length=200, temperature=0.7,do_sample=True,pad_token_id=tokenizer.eos_token_id)

# result = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print(result)
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# import os
# HF_TOKEN = os.environ.get("HF_TOKEN", None)
# model_id = "C:/Users/Lenovo/Documents/HuggingFace_Models/Mistral-7B-Instruct-v0.3"
# tokenizer = AutoTokenizer.from_pretrained(model_id)

# def get_current_weather(location: str, format: str):
#     """
#     Get the current weather

#     Args:
#         location: The city and state, e.g. San Francisco, CA
#         format: The temperature unit to use. Infer this from the users location. (choices: ["celsius", "fahrenheit"])
#     """
#     pass

# conversation = [{"role": "user", "content": "What's the weather like in Paris?"}]
# tools = [get_current_weather]


# # format and tokenize the tool use prompt 
# inputs = tokenizer.apply_chat_template(
#             conversation,
#             tools=tools,
#             add_generation_prompt=True,
#             return_dict=True,
#             return_tensors="pt",
# )

# model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

# inputs.to(model.device)
# outputs = model.generate(**inputs, max_new_tokens=1000)
# print(tokenizer.decode(outputs[0], skip_special_tokens=True))


import requests

url = "http://127.0.0.1:5000/upload-image/"
file_path = "test_image.jpg"  # Make sure this image exists

with open(file_path, "rb") as image_file:
    files = {"file": (file_path, image_file, "image/jpeg")}
    response = requests.post(url, files=files)

print(f"Status Code: {response.status_code}")  # Print status code
print("Raw Response Content:", response.text)  # Print raw response


