from abc import ABC, abstractmethod

# BaseProvider is an abstract base class that defines the interface for fetching 10-K reports.
class BaseProvider(ABC):
    @abstractmethod
    # This method should be implemented by subclasses to fetch the 10-K report for a given company.
    def fetch_10k_report(self, company):
        pass

    @abstractmethod
    # This method should be implemented by subclass to get the CIK (Central Index Key) for a list of companies.
    def get_cik(self):
        pass

    @abstractmethod
    # This method should be implemented by subclasses to fetch the 10-K report for a given company.
    def fetch_10k_report(self):
        pass