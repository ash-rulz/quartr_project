from dotenv import load_dotenv
import os
from src.providers.sec_provider import SECProvider

def run_automation(user_agent):
    # Initialize SEC provider with user agent
    sec_provider = SECProvider(user_agent)
    
    # Fetch 10-K report
    sec_provider.fetch_10k_report()

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    user_agent = os.getenv("SEC_USER_AGENT")
    if not user_agent:
        raise ValueError("SEC_USER_AGENT environment variable is not set.")
    #print(f"Using SEC_USER_AGENT: {user_agent}")

    run_automation(user_agent)
