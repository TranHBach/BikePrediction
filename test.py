import pandas as pd

# Read the CSV file
df = pd.read_csv('productInventory.csv')

# Set all quantities to 0
df['Quantity'] = 0

# Save the modified data back to CSV
# Keep the same formatting as original file
df.to_csv('productInventory.csv', index=False)