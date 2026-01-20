import pandas as pd

# Load the datasets
df1 = pd.read_csv("gaming_laptops.csv")
df2 = pd.read_csv("gaming_laptops2.csv")

print("--- Initial Missing Values in df2 ---")
print(df2[['CPU', 'GPU', 'Color']].isnull().sum())
print("-" * 30)

# Function to interactively fill missing values
def interactive_fill(df_target, df_source, columns):
    for col in columns:
        print(f"\nScanning for missing '{col}' values...")
        
        # Check for both pandas NaN and string "N/A"
        missing_mask = (df_target[col].isna()) | (df_target[col] == "N/A")
        
        indices = df_target[missing_mask].index
        
        if len(indices) == 0:
            print(f"No missing values found for {col}.")
            continue
            
        count = 0
        for idx in indices:
            path_val = df_source.at[idx, col]
            
            # Check if source also has missing data
            if pd.isna(path_val) or path_val == "N/A":
                continue

            current_val = df_target.at[idx, col]
            product_name = df_target.at[idx, 'Name']
            
            print(f"\n[Row {idx}] Product: {product_name}")
            print(f"Missing {col} in df2: {current_val}")
            print(f"Found value in df1:   {path_val}")
            
            response = input("Do you want to replace it? (y/n/all): ").strip().lower()
            
            if response == 'y':
                df_target.at[idx, col] = path_val
                print(">> Replaced.")
                count += 1
            elif response == 'all':
                df_target.at[idx, col] = path_val
                print(">> Replaced (and will auto-replace rest of this column).")
                # Apply to remaining matching indices for this column
                remaining = indices[indices > idx]
                for rem_idx in remaining:
                     rem_src_val = df_source.at[rem_idx, col]
                     if not (pd.isna(rem_src_val) or rem_src_val == "N/A"):
                        df_target.at[rem_idx, col] = rem_src_val
                        count += 1
                break # Exit the loop for this column
            else:
                print(">> Skipped.")
        
        print(f"Finished processing {col}. Replaced {count} values.")

# Run the interactive filler
columns_to_check = ['CPU','Color']
interactive_fill(df2, df1, columns_to_check)

print("\n" + "="*30)
print("Final Check on Missing Values in df2")
print(df2[['CPU', 'Color']].isin(['N/A', pd.NA, float('nan')]).sum()) # Check for N/A string too

# Clean price format for df2 as well
print("\nCleaning Price format...")
df2['Price'] = df2['Price'].astype(str).str.replace(r'[\xa0\s]', '', regex=True).str.replace('DT', '').str.replace(',', '.').astype(float).astype(int)

# Remove duplicates
print(" Duplicates Lines : ", df2.duplicated().sum())
df2.drop_duplicates(inplace=True)

print("\n--- Final Data Sample (df2) ---")
print(df2.head(), '\n')
print(df2.info(), '\n')
print("Null Values :","\n",df2.isnull().sum(), '\n')


# Calculate improvement
print("\n" + "="*40)
print("   DATA QUALITY IMPROVEMENT (df2 vs df1)   ")
print("="*40)

# Calculate non-null counts
total_rows = len(df2)
df1_nulls = df1.isnull().sum()
df2_nulls = df2.isnull().sum()

# improvement = current_nulls - new_nulls (positive means less nulls now)
improvement_counts = df1_nulls - df2_nulls
improvement_pct = (improvement_counts / total_rows) * 100

# Create a summary table
summary_df = pd.DataFrame({
    'Metric': improvement_pct.index,
    'Improvement': improvement_pct.values
})

# Filter only columns with changes and format them
summary_df = summary_df[summary_df['Improvement'] != 0].copy()
summary_df['Improvement'] = summary_df['Improvement'].apply(lambda x: f"+ {x:.2f} %" if x > 0 else f"{x:.2f} %")

print(summary_df.to_string(index=False))
print("-" * 40)

# handling missing values for df2 : GPU , Color 
# Refresh screen is not important for our analysis 
df2['GPU'] = df2['GPU'].fillna('GPU not listed')
df2['Color'] = df2['Color'].fillna('Color not listed')

#converting warranty to int
df2['Garentie'] = df2['Garentie'].astype(str).str.strip()
df2['Garentie'] = pd.to_numeric(df2['Garentie'], errors='coerce')
df2['Garentie'] = df2['Garentie'].fillna(0).astype(int)

# correcting the gpu vram shown in rtx 3050 4 :

df2['GPU'] = df2['GPU'].replace('RTX 3050 4', 'RTX 3050')

print("\nSaving updated gaming_laptops2.csv...")
df2.to_csv("gaming_laptops2_cleaned.csv", index=False)
print("Done! Saved to 'gaming_laptops2_cleaned.csv'")