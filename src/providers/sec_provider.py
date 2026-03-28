from .base_provider import BaseProvider

class SECProvider(BaseProvider):
    def fetch_10k_report(self):
        # Implementation for fetching 10-K report from SEC
        print("Fetching 10-K report from SEC...")
