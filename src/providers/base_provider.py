from abc import ABC, abstractmethod

# BaseProvider is an abstract base class that defines the interface for fetching 10-K reports.
class BaseProvider(ABC):
    @abstractmethod
    # This method should be implemented by subclass to get the CIK (Central Index Key) for a list of companies.
    def get_cik(self):
        pass

    @abstractmethod
    # This method should be implemented by subclasses to fetch the 10-K report url for a list of companies.
    def fetch_10k_report_url(self):
        pass
    
    @abstractmethod
    # This method should be implemented by subclasses to download the 10-K reports for a list of companies.
    def download_10k_reports(self):
        pass