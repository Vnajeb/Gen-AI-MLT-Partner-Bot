import requests

# This class grabs company data (like name, ticker, and CIK) from the SEC's public JSON file.
# It also lets you look up company info by name or stock ticker.
class SecEdgar:
    def __init__(self, json_url):
        self.json_url = json_url
        self.name_to_cik_map = {}
        self.ticker_to_cik_map = {}
        self.all_company_data = {}

        # SEC requires a user-agent header, so we include that here
        headers = {'user-agent': 'MLT CB najeb101@icloud.com'}
        response = requests.get(self.json_url, headers=headers)
        data = response.json()

        # Loop through each company entry and organize the useful info
        for entry in data.values():
            cik = entry.get('cik_str')
            ticker = entry.get('ticker')
            name = entry.get('title')

            # Skip entries that are missing critical info
            if not name or not ticker:
                continue

            self.all_company_data[cik] = (cik, ticker, name)
            self.name_to_cik_map[name.lower()] = cik
            self.ticker_to_cik_map[ticker.lower()] = cik

    # Find a company's CIK info using its name
    def get_by_name(self, company_name):
        try:
            cik = self.name_to_cik_map[company_name.lower()]
            return self.all_company_data[cik]
        except KeyError:
            return 'No company found with that name.'

    # Find a company's CIK info using its stock ticker
    def get_by_ticker(self, ticker_symbol):
        try:
            cik = self.ticker_to_cik_map[ticker_symbol.lower()]
            return self.all_company_data[cik]
        except KeyError:
            return 'No ticker match found.'


# Example usage
sec_lookup = EdgarCompanyLookup('https://www.sec.gov/files/company_tickers.json')
print(sec_lookup.get_by_name('Salesforce Inc.'))
print(sec_lookup.get_by_ticker('CRM'))
