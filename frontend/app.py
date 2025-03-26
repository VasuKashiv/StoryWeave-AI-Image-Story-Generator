# import streamlit as st
# import requests
# from PIL import Image
# import io

# # Backend API URL
# BACKEND_URL = "http://127.0.0.1:8000"  # Ensure this matches your backend port

# # Streamlit UI
# st.set_page_config(page_title="AI Story Generator", layout="wide")

# st.title("📖 AI-Powered Story Generator")

# # Upload Image
# uploaded_file = st.file_uploader("Upload an image to generate a story", type=["png", "jpg", "jpeg"])

# if uploaded_file:
#     # Display the uploaded image
#     image = Image.open(uploaded_file)
#     st.image(image, caption="Uploaded Image", use_column_width=True)

#     # Convert image to bytes
#     image_bytes = io.BytesIO()
#     image.save(image_bytes, format="PNG")
#     image_bytes = image_bytes.getvalue()

#     # Button to generate story
#     if st.button("Generate Story"):
#         with st.spinner("Analyzing image..."):
#             files = {"file": ("image.png", image_bytes, "image/png")}
#             response = requests.post(f"{BACKEND_URL}/upload-image/", files=files)

#             if response.status_code == 200:
#                 data = response.json()
#                 image_caption = data.get("caption", "")

#                 if not image_caption:
#                     st.error("Image analysis failed!")
#                 else:
#                     st.success(f"Image caption: {image_caption}")

#                     with st.spinner("Generating story..."):
#                         story_response = requests.post(
#                             f"{BACKEND_URL}/generate_story", json={"image_caption": image_caption}
#                         )

#                         if story_response.status_code == 200:
#                             story_data = story_response.json()
#                             st.session_state["story"] = story_data["story"]
#                             st.session_state["choices"] = story_data["choices"]
#                         else:
#                             st.error("Error generating story.")
#             else:
#                 st.error("Error uploading image!")

# # Display and handle the story continuation
# if "story" in st.session_state:
#     st.subheader("📜 Generated Story")
#     st.write(st.session_state["story"])

#     # Display user choices
#     if "choices" in st.session_state and st.session_state["choices"]:
#         st.subheader("🔮 What Happens Next?")
#         user_choice = st.radio("Choose what happens next:", st.session_state["choices"])

#         if st.button("Continue Story"):
#             with st.spinner(f"Continuing story with: {user_choice}..."):
#                 response = requests.post(
#                     f"{BACKEND_URL}/continue_story",
#                     json={"story": st.session_state["story"], "user_choice": user_choice}
#                 )
#                 if response.status_code == 200:
#                     data = response.json()
#                     st.session_state["story"] = data["story"]
#                     st.session_state["choices"] = data["choices"]
#                 else:
#                     st.error("Error continuing story.")


import streamlit as st
import requests
from PIL import Image
import io

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"  # Ensure this matches your backend port

# Streamlit UI
st.set_page_config(page_title="AI Story Generator", layout="wide")

st.title("📖 AI-Powered Story Generator")

# Ensure proper state initialization for story and image caption
if "story_state" not in st.session_state:
    st.session_state["story_state"] = {}
if "image_caption" not in st.session_state:
    st.session_state["image_caption"] = ""

# Upload Image
uploaded_file = st.file_uploader("Upload an image to generate a story", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes = image_bytes.getvalue()

    # Button to generate story, with unique key for handling state
    if st.button("Generate Story", key="generate_story_btn"):
        with st.spinner("Analyzing image..."):
            try:
                # Upload the image to `/upload-image/` endpoint
                files = {"file": ("image.png", image_bytes, "image/png")}
                response = requests.post(f"{BACKEND_URL}/upload-image/", files=files, timeout=15)

                if response.status_code == 200:
                    data = response.json()
                    st.session_state["image_caption"] = data.get("caption", "")
                    st.session_state["story_state"] = {"story": "", "choices": []}

                    if not st.session_state["image_caption"]:
                        st.error("Image analysis failed.")
                    else:
                        st.success(f"Image caption: {st.session_state['image_caption']}")

                        with st.spinner("Generating story..."):
                            story_response = requests.post(
                                f"{BACKEND_URL}/generate_story",
                                json={"image_caption": st.session_state["image_caption"]}, 
                            )
                            if story_response.status_code == 200:
                                story_data = story_response.json()
                                st.session_state["story_state"]["story"] = story_data["story"]
                                st.session_state["story_state"]["choices"] = story_data["choices"]
                            else:
                                st.error("Error generating story.")
                else:
                    st.error("Error uploading image.")
            except requests.exceptions.Timeout:
                st.error("Server is taking too long to respond. Please try again later.")

# Display and handle the story continuation
if st.session_state["story_state"].get("story"):
    st.subheader("📜 Generated Story")
    st.write(st.session_state["story_state"]["story"])

    # Display user choices if available
    if st.session_state["story_state"].get("choices"):
        st.subheader("🔮 What Happens Next?")
        user_choice = st.radio(
            "Choose what happens next:", st.session_state["story_state"]["choices"], key="story_choices_radio"
        )

        # Button to continue story, with unique key
        if st.button("Continue Story", key="continue_story_btn"):
            with st.spinner(f"Continuing story with: {user_choice}..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/continue_story",
                        json={"story": st.session_state["story_state"]["story"], "user_choice": user_choice}, # Timeout to avoid long waits
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state["story_state"]["story"] = data["story"]
                        st.session_state["story_state"]["choices"] = data["choices"]
                    else:
                        st.error("Error continuing story.")
                except requests.exceptions.Timeout:
                    st.error("Server is taking too long to respond. Please try again later.")
