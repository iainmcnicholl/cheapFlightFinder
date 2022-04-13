import flight_search, data_manager, flight_data, notification_manager

# initialise objects
data_manager = data_manager.DataManager()
flight_search = flight_search.FlightSearch()
flight_data = flight_data.FlightData()
notification_manager = notification_manager.NotificationManager()

# set main.py sheet_data variable from sheet at opening
sheet_data = data_manager.get_data()

# check sheet has all iata codes for each city on sheet, and if not update sheet with iata from Kiwi API
row_count = 2
col_count = 2
for row in sheet_data:
    if row['IATA Code'] == "":
        data_manager.put_data(row_count, col_count, flight_search.return_iata_code(row['City']))
        row_count += 1

# sets notification_data to a list of treated values needed for notification, to be passed to notification manager
city_flight_data = flight_data.get_city_flight_data()
notification_data = flight_data.output_flight_data(city_flight_data)

# reset counters to work through price col
row_count = 2
col_count = 3

# loop through treat notification data, and check if price is < max price on sheet. If true, trigger SMS notification with
# flight details to target number

# list count used to access correct data from notification_data and tracks loop iteration
list_count = 0
for city in notification_data:
    if data_manager.get_cell(row_count, col_count) >= city['price']:
        notification_manager.send_notification(notification_data, list_count)
    row_count += 1
    list_count += 1
