from dotenv import load_dotenv
import os
import yaml
from src.providers.sec_provider import SECProvider

def load_config():
    # Load configuration from conffig.yaml file
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)
    

def run_automation(user_agent):
    config = load_config()

    # Initialize SEC provider with user agent
    sec_provider = SECProvider(user_agent)
    
    companies = config["companies"] # List of company tickers to fetch 10-K reports for
    if not companies:
        raise ValueError("companies list is empty in config.yaml")

    # Fetch CIK for the list of companies
    cik_mapping = sec_provider.get_cik(companies)

    # Convert report to pdf and save to local directory

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    user_agent = os.getenv("SEC_USER_AGENT")
    if not user_agent:
        raise ValueError("SEC_USER_AGENT environment variable is not set.")
    #print(f"Using SEC_USER_AGENT: {user_agent}")

    run_automation(user_agent)
