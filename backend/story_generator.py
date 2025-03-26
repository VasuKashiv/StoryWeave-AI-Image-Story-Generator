from backend.story_graph import graph_executor, initial_state

def generate_story(image_caption):
    """Generates a story based on an image caption."""
    state = initial_state(image_caption)
    final_state = graph_executor.invoke(state)

    return {
        "story": final_state["story"],
        "choices": final_state["choices"]
    }
# def continue_story(story, user_choice):
#     """Continue the story based on the user’s choice with optimized performance."""
#     state = {"story": story, "user_choice": user_choice}

#     # New Prompt Format to Improve Continuity
#     state["prompt"] = f"Continue this immersive story: {story}\nAdd a twist based on this choice: {user_choice}.\nMaintain deep emotions, mystery, and sensory details."

#     # Invoke the optimized graph execution
#     final_state = graph_executor.invoke(state)

#     return {
#         "story": final_state["story"],
#         "choices": final_state["choices"]
#     }

def continue_story(story, user_choice):
    """Continue the story based on the user’s choice with optimized performance."""
    state = {"story": story, "user_choice": user_choice}

    # More descriptive prompt with better context for improved continuity
    state["prompt"] = (
        f"Continue this immersive story with the following twist: {user_choice}.\n"
        f"Keep the storyline engaging, add emotional depth, and introduce a surprise or new challenge."
    )

    # Invoke the optimized graph execution
    final_state = graph_executor.invoke(state)

    return {
        "story": final_state["story"],
        "choices": final_state["choices"]  # Allow the user to make another choice
    }