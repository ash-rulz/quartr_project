import requests
from datetime import datetime
import time
from src.utils.utilities import common_utils
from os import path, makedirs
import pdfkit

class SECProvider:
    def __init__(self, user_agent, config):
        self.headers = {"User-Agent": user_agent}
        self.config = config
        self.session = requests.Session()
        self.common_utils = common_utils() # Initialize the common_utils instance for rate limiting

    def get_cik(self):
        # Implementation for getting CIK from SEC
        print(f"Getting CIK from SEC...")
        url = self.config["endpoints"]["sec_ticker_url"]
        data = self.edgar_request(url) # Call the helper method to make the request to SEC and get the data
        if data:
            cik_mapping_dict = {}
            for item in data.values():
                 ticker = item.get("ticker")
                 cik = str( item.get("cik_str") ).zfill(10)  # Ensure CIK is 10 digits
                 if cik and ticker in self.config["companies"]:
                     cik_mapping_dict[ticker] = cik
            print(f"Final CIK mapping: {cik_mapping_dict}")
            return cik_mapping_dict
        
    def fetch_10k_report_url(self, cik_mapping_dict):
        # Implementation for fetching 10-K report url for a list of companies
        submissions_url = self.config["endpoints"]["sec_submissions_url"]
        form_10k_url_dict = {}
        for company in self.config["companies"]:
            cik = cik_mapping_dict[company]
            if cik:
                print(f"Fetching 10-K report url for {company} (CIK: {cik})...")
                data = self.edgar_request(submissions_url.format(cik=cik)) # Call the helper method to make the request to SEC and get the data
                if data:
                    recent_filings = data['filings']['recent']
                    if recent_filings:
                        for i, form in enumerate(recent_filings['form']):
                            if form == '10-K':
                                accession_number = recent_filings['accessionNumber'][i].replace('-', '')
                                primary_doc = recent_filings['primaryDocument'][i]
                                report_url = self.config["endpoints"]["sec_filing_url"].format(
                                    cik=cik, accession_number=accession_number, filename=primary_doc)
                                print(f"10-K report URL for {company} found.")
                                form_10k_url_dict[company] = report_url
                                break
                    else:
                        print(f"No recent filings found for {company}.")
            else:
                print(f"CIK not found for {company}. Skipping...")
        print(f"Final 10-K report URLs: {form_10k_url_dict}")
        return form_10k_url_dict

    def edgar_request(self, url, **kwargs):
        # Helper method to make requests to the SEC EDGAR system
        request_timeout = self.config["requests"]["timeout_seconds"]
        retry_total = self.config["requests"]["retry_total"]
        retry_backoff_factor = self.config["requests"]["retry_backoff_factor"]
        response = None
        last_error = None
        for attempt in range(retry_total + 1):
            try:
                # Ensure only 10 requests per second to comply with SEC guidelines
                self.common_utils.rate_limit()
                response = self.session.get(url, headers=self.headers, timeout=request_timeout)
                response.raise_for_status()
                break
            except Exception as e:
                # Retry on any request exception, including timeouts and connection errors
                last_error = e
                if attempt == retry_total:
                    print(f"Error making request to {url}: {e}")
                    return None
                wait_time = retry_backoff_factor * (2 ** attempt)
                print(f"Request failed for {url}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        if response is None:
            return None

        output_format = kwargs.get("output_format", "json")
        output_path = kwargs.get("output_path", None)
        if output_format == "json":
            return response.json()
        elif output_format == "text":
            return response.text
        elif output_format == "pdf":
            options = {
                'custom-header': [('User-Agent', self.headers['User-Agent'])],
                'quiet': ''
            }
            path_to_wkhtmltopdf = self.config["local_directory"]["wkhtmltopdf_directory"]
            config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
            # Implementing retry logic for PDF generation with exponential backoff
            last_error = None
            for attempt in range(retry_total + 1):
                try:
                    pdfkit.from_url(url, output_path, options=options, configuration=config)
                    print(f"Successfully saved: {output_path}")
                    return output_path
                except Exception as e:
                    last_error = e
                    if attempt == retry_total:
                        break
                    wait_time = retry_backoff_factor * (2 ** attempt)
                    print(f"PDF generation failed for {url}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            print(f"Error generating PDF from {url}: {last_error}")
            return None
        else:
            print(f"Unsupported output format: {output_format}")
            return None
    
    def download_10k_reports(self, form_10k_url_dict):
        # Implementation for downloading 10-K reports for a list of companies
        directory = path.join(self.config["output"]["form_10k_directory"], 
                              datetime.now().strftime("%Y-%m-%d"))
        if not path.exists(directory):
            makedirs(directory)
        for company, url in form_10k_url_dict.items():
            print(f"Downloading 10-K report for {company} from {url}...")
            try:
                # Call the helper method to make the request to SEC and get the data in text format
                output_path = path.join(directory, f"{company}_10-K.pdf")
                self.edgar_request(url, output_format="pdf", output_path=output_path)
            except Exception as e:
                print(f"Error downloading 10-K report for {company}: {e}")