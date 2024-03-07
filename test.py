import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Sample Data
data = {
    'Employee Code': [1, 2, 3],
    'Manager Employee Code': [np.nan, 1, 1],
    'Date of Joining': ['2021-01-01', '2021-01-01', '2021-01-01'],
    'Date of Exit': [np.nan, np.nan, '2023-12-31'],
    'Compensation': [20000, 20000, 20000],
    'Compensation 1': [np.nan, 10000, 10000],
    'Compensation 1 date': [np.nan, '2022-01-01', '2022-01-01'],
    'Compensation 2': [np.nan, 20000, 20000],
    'Compensation 2 date': [np.nan, '2023-01-01', '2023-01-01'],
    'Review 1': [np.nan, 9, 9],
    'Review 1 date': [np.nan, '2021-06-01', '2021-06-01'],
    'Review 2': [np.nan, 9.5, 9.5],
    'Review 2 date': [np.nan, '2022-06-01', '2022-06-01'],
    'Engagement 1': [np.nan, 4, 4],
    'Engagement 1 date': [np.nan, '2021-03-01', '2021-03-01'],
    'Engagement 2': [np.nan, 5, 5],
    'Engagement 2 date': [np.nan, '2022-03-01', '2022-03-01'],
}

df = pd.DataFrame(data)

# Helper function to get all dates for changes
def get_dates(row):
    dates = [row['Date of Joining']]
    if pd.notna(row['Date of Exit']):
        dates.append(row['Date of Exit'])
    for col in df.columns:
        if 'date' in col.lower() and pd.notna(row[col]):
            dates.append(row[col])
    unique_sorted_dates = sorted(set(dates))
    return unique_sorted_dates

# Process each employee
all_rows = []
for _, row in df.iterrows():
    dates = get_dates(row)
    for i, date in enumerate(dates):
        if i < len(dates) - 1:
            end_date = datetime.strptime(dates[i+1], '%Y-%m-%d') - timedelta(days=1)
        else:  # For the last record, set a far-future end date
            end_date = datetime(2100, 1, 1)
        temp_row = {
            'Employee Code': row['Employee Code'],
            'Manager Employee Code': row['Manager Employee Code'],
            'Last Compensation': row['Compensation'] if date == row['Date of Joining'] else None,
            'Compensation': row['Compensation'],
            'Last Pay Raise Date': row['Review 2 date'] if date == row['Review 2 date'] else row['Review 1 date'] if date == row['Review 1 date'] else None,
            'Performance Rating': row['Review 2'] if date == row['Review 2 date'] else row['Review 1'] if date == row['Review 1 date'] else None,
            'Engagement Score': row['Engagement 2'] if date == row['Engagement 2 date'] else row['Engagement 1'] if date == row['Engagement 1 date'] else None,
            'Compensation Change': row['Compensation 1'] if date == row['Compensation 1 date'] else (row['Compensation 2'] if date == row['Compensation 2 date'] else None),
            'Effective Date': date,
            'End Date': end_date.strftime('%Y-%m-%d'),
        }
        all_rows.append(temp_row)

# Convert all_rows to a DataFrame
output_df = pd.DataFrame(all_rows)

# Drop duplicates to remove unnecessary rows
output_df = output_df.drop_duplicates()

# Adjust columns as per the requirements
output_df = output_df[['Employee Code', 'Manager Employee Code', 'Last Compensation', 'Compensation', 
                       'Last Pay Raise Date', 'Performance Rating', 'Engagement Score', 'Compensation Change', 
                       'Effective Date', 'End Date']]

print(output_df)

# Save the DataFrame to CSV
output_df.to_csv('Output.csv', index=False)
