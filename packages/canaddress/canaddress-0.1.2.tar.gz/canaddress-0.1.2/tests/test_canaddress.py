import pandas as pd
from canaddress import AddressParser

def test_address_parser():
    data = {
        'Property_Address': [
            '1801  3077 WESTON ROAD, TORONTO, ONTARIO M9M3A1',
            '711  4673 JANE STREET, TORONTO, ONTARIO M3N2L1',
            '105  55 NEPTUNE DRIVE, TORONTO, ONTARIO M6A1X2',
            '104  5949 YONGE STREET, TORONTO, ONTARIO M2M3V8'
        ]
    }
    df = pd.DataFrame(data)
    parser = AddressParser(df, 'Property_Address')
    parser.clean_and_process_data()
    result = parser.display_data()
    assert 'street_no' in result.columns
    assert 'street_name' in result.columns
    assert 'city' in result.columns
    assert 'province' in result.columns
    assert 'postal_code' in result.columns

if __name__ == '__main__':
    test_address_parser()
