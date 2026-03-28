from .base_provider import BaseProvider

class SECProvider(BaseProvider):
    def __init__(self, user_agent):
        self.user_agent = user_agent
        
    def fetch_10k_report(self):
        # Implementation for fetching 10-K report from SEC
        print("Fetching 10-K report from SEC...")
