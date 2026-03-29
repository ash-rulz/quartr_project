import requests
from .base_provider import BaseProvider

class SECProvider(BaseProvider):
    def __init__(self, user_agent):
        self.headers = {"User-Agent": user_agent}
        
    def fetch_10k_report(self, company):
        # Implementation for fetching 10-K report from SEC
        print(f"Fetching 10-K report for {company} from SEC...")

    def get_cik(self, companies):
        # Implementation for getting CIK from SEC
        print(f"Getting CIK from SEC...")
        url = "https://www.sec.gov/files/company_tickers.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            cik_lookup = {}
            for item in data.values():
                 ticker = item.get("ticker")
                 cik = str( item.get("cik_str") ).zfill(10)  # Ensure CIK is 10 digits
                 if ticker and cik:
                     cik_lookup[ticker] = cik
            final_mapping = {company: cik_lookup.get(company) for company in companies}
            print(final_mapping)
            return final_mapping
        else:
            print(f"Failed to fetch CIK data from SEC. Status code: {response.status_code}")
            return None