import gspread
from oauth2client.service_account import ServiceAccountCredentials

# authorise the API, TODO add in file name with credentials as file_name. Share sheet with service account email
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

file_name = 'testcreds.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)


class DataManager:
    def __init__(self):
        self.sheet_data = client.open('Flight Deals').sheet1

    def get_data(self):
        """returns all data from self.sheet_data"""
        return self.sheet_data.get_all_records()

    def put_data(self, row, col, update):
        """puts data passed as update to cell specified by row and col """
        self.sheet_data.update_cell(row, col, update)
        self.sheet_data = client.open('Flight Deals').sheet1

    def get_cell(self, row, col):
        """returns cell data as int specified by row and col"""
        return int(self.sheet_data.cell(row, col).value)
