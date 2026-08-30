import csv
import gspread

# 1. Authenticate using your credentials
gc = gspread.service_account(filename="credentials.json")

# 2. Open the spreadsheet
spreadsheet = gc.open("Daily Sheet Site4people")

# 3. Select your specific worksheet
# Option A: Select by name (Recommended)
worksheet = spreadsheet.worksheet("Lead Generation")  # Change "Sheet1" to your specific sheet tab name

# Option B: Or keep using the first sheet tab
# worksheet = spreadsheet.sheet1

# 4. Fetch ALL values from the sheet as a list of lists
all_values = worksheet.get_all_values()

# 5. Write the data to a local CSV file
csv_filename = "downloaded_sheet.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(all_values)

print(f"Successfully downloaded and saved to {csv_filename}!")
