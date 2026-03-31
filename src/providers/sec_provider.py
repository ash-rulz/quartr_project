import requests
from src.providers.base_provider import BaseProvider
from src.utils.utilities import common_utils

class SECProvider(BaseProvider):
    def __init__(self, user_agent, config):
        self.headers = {"User-Agent": user_agent}
        self.companies = config["companies"]
        self.sec_ticker_cik_url = config["endpoints"]["sec_ticker_url"]
        self.sec_submissions_url = config["endpoints"]["sec_submissions_url"]
        self.sec_filings_url = config["endpoints"]["sec_filing_url"]
        self.cik_mapping_dict = {}
        self.form_10k_url_dict = {} 

    def get_cik(self):
        # Implementation for getting CIK from SEC
        print(f"Getting CIK from SEC...")
        url = self.sec_ticker_cik_url
        self.common_utils = common_utils() # Initialize the common_utils instance for rate limiting
        data = self.edgar_request(url) # Call the helper method to make the request to SEC and get the data
        if data:
            cik_lookup = {}
            for item in data.values():
                 ticker = item.get("ticker")
                 cik = str( item.get("cik_str") ).zfill(10)  # Ensure CIK is 10 digits
                 if ticker and cik:
                     cik_lookup[ticker] = cik
            final_mapping = {company: cik_lookup[company] for company in self.companies}
            print(f"Final CIK mapping: {final_mapping}")
            self.cik_mapping_dict = final_mapping
        
    def fetch_10k_report_url(self):
        # Implementation for fetching 10-K report url for a list of companies
        submissions_url = self.sec_submissions_url
        form_10k_url = {}
        for company in self.companies:
            cik = self.cik_mapping_dict[company]
            if cik:
                print(f"Fetching 10-K report for {company} (CIK: {cik})...")
                data = self.edgar_request(submissions_url.format(cik=cik)) # Call the helper method to make the request to SEC and get the data
                if data:
                    recent_filings = data['filings']['recent']
                    if recent_filings:
                        for i, form in enumerate(recent_filings['form']):
                            if form == '10-K':
                                accession_number = recent_filings['accessionNumber'][i].replace('-', '')
                                primary_doc = recent_filings['primaryDocument'][i]
                                report_url = self.sec_filings_url.format(cik=cik, accession_number=accession_number, filename=primary_doc)
                                print(f"10-K report URL for {company} found.")
                                form_10k_url[company] = report_url
                                break
                    else:
                        print(f"No recent filings found for {company}.")
            else:
                print(f"CIK not found for {company}. Skipping...")
        print(f"Final 10-K report URLs: {form_10k_url}")
        self.form_10k_url_dict = form_10k_url

    def edgar_request(self, url):
        # Helper method to make requests to the SEC EDGAR system
        try:
            # Ensure only 10 requests per second to comply with SEC guidelines
            self.common_utils.rate_limit()
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            if response.status_code == 200:
                return response.json()
            else:                
                print(f"Failed to fetch data from SEC. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None