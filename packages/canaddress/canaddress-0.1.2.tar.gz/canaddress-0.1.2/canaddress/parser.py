import pandas as pd
import re

class AddressParser:
    def __init__(self, df, address_column):
        self.df = df
        self.address_column = address_column
    
    def clean_address(self, address):
        address = address.upper()
        address = re.sub(r'\s+', ' ', address).strip()
        abbreviations = {
            'ST': 'STREET', 'RD': 'ROAD', 'AVE': 'AVENUE', 'BLVD': 'BOULEVARD',
            'CRES': 'CRESCENT', 'CT': 'COURT', 'DR': 'DRIVE', 'LN': 'LANE',
            'PL': 'PLACE', 'PKWY': 'PARKWAY', 'HWY': 'HIGHWAY'
        }
        for abbr, full in abbreviations.items():
            address = re.sub(r'\b{}\b'.format(abbr), full, address)
        address = re.sub(r'[^\w\s,|]', '', address)
        address = address.replace('|', ',')
        return address

    def split_address(self, address):
        match = re.match(r'(\d+)\s*[-/]?\s*(\d+)\s+([^,]+),\s*([^,]+),\s*([^,]+)\s+([A-Z]\d[A-Z]\s*\d[A-Z]\d)', address)
        if match:
            unit_no = match.group(1)
            street_no = match.group(2)
            street_name = match.group(3)
            city = match.group(4)
            province = match.group(5)
            postal_code = match.group(6)
            return {
                'unit_no': unit_no,
                'street_no': street_no,
                'street_name': street_name,
                'city': city,
                'province': province,
                'postal_code': postal_code
            }
        else:
            return {
                'unit_no': '', 'street_no': '', 'street_name': '',
                'city': '', 'province': '', 'postal_code': ''
            }

    def clean_and_process_data(self):
        self.df['Cleaned_Address'] = self.df[self.address_column].apply(self.clean_address)
        address_components = self.df['Cleaned_Address'].apply(self.split_address)
        df_address_components = pd.DataFrame(address_components.tolist())
        df_address_components.columns = [
            'unit_no', 'street_no', 'street_name', 'city', 'province', 'postal_code'
        ]
        self.df = pd.concat([self.df, df_address_components], axis=1)

    def save_cleaned_data(self, output_path):
        self.df.to_csv(output_path, index=False)

    def display_data(self):
        return self.df.head()
