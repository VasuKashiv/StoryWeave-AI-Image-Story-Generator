import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langgraph.graph import StateGraph, END
from typing import Dict, Any

# Phi-3.5-mini-instruct as the story generation model
MODEL_NAME = "microsoft/Phi-3.5-mini-instruct"

# ✅ Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, torch_dtype=torch.float16, device_map="auto"
)


def initial_state(image_caption: str) -> Dict[str, Any]:
    return {
        "image_caption": image_caption,
        "story": "",
        "choices": [],
        "story_continued": False  # ✅ New flag to track story continuation
    }

#  Generate initial story based on image caption
def generate_story(state: Dict[str, Any]) -> Dict[str, Any]:
    prompt = (
        f"Write a captivating story inspired by the scene: {state['image_caption']}.\n\n"
        f"Include vivid emotions, sensory details, and a hint of mystery or surprise."
    )
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

    # Generate the story with creative, diverse sampling
    outputs = model.generate(**inputs, max_new_tokens=150, do_sample=True, temperature=0.8, top_p=0.9)
    state["story"] = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Provide initial story choices
    state["choices"] = ["A shadow appears on the horizon", "The character discovers a secret map", "A storm suddenly approaches"]
    return state

# ✅ Handle user choice and continue story dynamically
def handle_choice(state: Dict[str, Any], user_choice: str) -> Dict[str, Any]:
    # Append user choice to the selections history for tracking
    state["user_selections"].append(user_choice)

    # Update prompt to continue story with user twist
    prompt = f"Continue this story with the following twist: {user_choice}. Make the plot deeper, and introduce unexpected developments."
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

    # Generate the continuation with adjusted parameters for creativity
    outputs = model.generate(**inputs, max_new_tokens=150, do_sample=True, temperature=0.85, top_k=40)
    state["story"] += "\n\n" + tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Generate dynamic choices based on the current story content
    state["choices"] = generate_dynamic_choices(state["story"])
    return state


# ✅ Dynamically generate relevant choices based on current story content
def generate_dynamic_choices(story: str) -> list:
    """Generate choices by analyzing the latest part of the story."""
    if "storm" in story:
        return ["Seek shelter in a nearby cave", "Confront the storm head-on", "Find a guide to navigate through the storm"]
    elif "map" in story:
        return ["Follow the map's hidden clues", "Burn the map and walk away", "Seek help from a mysterious traveler"]
    else:
        return ["Introduce a powerful adversary", "Reveal a hidden treasure", "Change the setting dramatically"]



story_graph = StateGraph(dict)  
story_graph.add_node("generate_story", generate_story)
story_graph.add_node("handle_choice", handle_choice)
story_graph.set_entry_point("generate_story")

# Automatically transition from "generate_story" to "handle_choice" after the first generation
story_graph.add_conditional_edges("generate_story", lambda state: "handle_choice")

# Loop "handle_choice" for continuing the story until the user ends it
story_graph.add_conditional_edges("handle_choice", lambda state: "handle_choice" if state.get("choices") else END)

graph_executor = story_graph.compile()
