# from datetime import datetime, timedelta

# cookie_expiry_time_db = "12/04/23 15:20"
# cookie_expiry_time_db = datetime.strptime(cookie_expiry_time_db, '%d/%m/%y %H:%M')
# time_diff = datetime.utcnow() - cookie_expiry_time_db

# # Check if an hour has passed
# if time_diff >= timedelta(hours=1):
#     print("An hour has passed since", cookie_expiry_time_db)
# else:
#     print("Less than an hour has passed since", cookie_expiry_time_db)

# now = datetime.utcnow()
# formatted_time = now.strftime('%d/%m/%y %H:%M')

# print(cookie_expiry_time_db)
# print(formatted_time)


string1 = "admin"
string2 = "iralosco"

if "admin1" == string1 or  "admin" == string2:
    print("authorized")