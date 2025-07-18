import streamlit as st
from router import LLMRouter
import openai

def main():
    # Get API key from Streamlit secrets
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in Streamlit secrets. Please set it in secrets.toml or Streamlit Cloud.")
    
    # Initialize the router with the API key
    router = LLMRouter(api_key=api_key)

    # Example 1: Content moderation
    try:
        moderation_response = router.run_task(
            "moderator",
            content="This is a test message that needs moderation."
        )
        print("\nModeration Response:")
        print(moderation_response)
    except Exception as e:
        print(f"Error in moderation task: {e}")

    # Example 2: Theme coding
    try:
        coding_response = router.run_task(
            "theme_coder",
            requirements="Create a dark theme with blue accents for a code editor."
        )
        print("\nTheme Coding Response:")
        print(coding_response)
    except Exception as e:
        print(f"Error in theme coding task: {e}")

    # Example 3: Translation (dummy implementation)
    try:
        translation_response = router.run_task(
            "translator",
            source_language="English",
            target_language="Spanish",
            text="Hello, how are you?"
        )
        print("\nTranslation Response:")
        print(translation_response)
    except Exception as e:
        print(f"Error in translation task: {e}")

if __name__ == "__main__":
    main() 