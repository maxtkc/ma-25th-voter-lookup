import pandas as pd

df = pd.read_excel("Just25th.xlsx")
df['Full Name'] = df['First Name'] + " " + df['Last Name']
json = df[['Full Name', 'Age']].to_json(orient='records', index=False)
with open("voters.json", "w") as f:
    if json:
        f.write(json)
