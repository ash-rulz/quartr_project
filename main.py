from dotenv import load_dotenv
import os
import yaml
from src.providers.sec_provider import SECProvider

def load_config():
    # Load configuration from conffig.yaml file
    with open("config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)
    

def run_automation(user_agent):
    config = load_config()

    # Initialize SEC provider with user agent
    sec_provider = SECProvider(user_agent, config)

    # Fetch CIK mapping for the companies
    sec_provider.get_cik()

    # Fetch 10-K report urls for the companies    
    sec_provider.fetch_10k_report_url()

    # Download 10-K reports for the companies in PDF format and save them to the specified directory
    sec_provider.download_10k_reports()

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    user_agent = os.getenv("SEC_USER_AGENT")
    if not user_agent:
        raise ValueError("SEC_USER_AGENT environment variable is not set.")
    #print(f"Using SEC_USER_AGENT: {user_agent}")

    run_automation(user_agent)
