from dotenv import load_dotenv
import os

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    user_agent = os.getenv("SEC_USER_AGENT")
    if not user_agent:
        raise ValueError("SEC_USER_AGENT environment variable is not set.")
    #print(f"Using SEC_USER_AGENT: {user_agent}")

    