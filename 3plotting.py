import matplotlib.pyplot as plt
import seaborn as sns

# First approach : Using individual plots

def individual_plots(df):
    #Histogram of Prices
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Price'], bins=20, kde=True, color='blue')
    plt.title('Distribution of Gaming Laptop Prices')
    plt.xlabel('Price (DT)')
    plt.show()

    # Boxplot: Price vs. GPU
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='GPU', y='Price', data=df)
    plt.xticks(rotation=45)
    plt.title('Price Distribution by GPU Type')
    plt.show()

    # Count plot for RAM configurations
    sns.countplot(x='RAM', data=df, palette='viridis')
    plt.title('Most Common RAM Sizes')
    plt.show()

    # Heatmap of correlations
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
    plt.show()

    # Boxplot: Price vs. Storage
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Storage', y='Price', data=df)
    plt.xticks(rotation=45)
    plt.title('Price Distribution by Storage Type')
    plt.show()

    # --- PIE CHART: Availability ---
    plt.figure(figsize=(12,6))
    # Get the counts for each status (e.g., "En stock")
    availability_counts = df['Availability'].value_counts()

    # Create the pie chart
    plt.pie(availability_counts, 
            labels=availability_counts.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=['#66b3ff','#99ff99','#ffcc99']) # Custom colors

    plt.title('Laptop Availability Distribution')
    plt.axis('equal')  # Ensures the pie is a circle
    plt.show()


# Second approach : Using subplots 
def subplots(df):
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle("Gaming Laptops EDA Dashboard", fontsize=18)

    # Price distribution
    sns.histplot(df['Price'], bins=20, kde=True,color='blue', ax=axes[0, 0])
    axes[0, 0].set_title("Price Distribution")

    # Price vs GPU
    sns.boxplot(x='GPU', y='Price', data=df, ax=axes[0, 1])
    axes[0, 1].set_title("Price by GPU")
    axes[0, 1].tick_params(axis='x', rotation=45)

    # RAM count
    sns.countplot(x='RAM', data=df,palette='viridis',  ax=axes[0, 2])
    axes[0, 2].set_title("RAM Distribution")

    # Correlation heatmap
    sns.heatmap(df.corr(numeric_only=True),
                annot=True,
                cmap='coolwarm',
                ax=axes[1, 0])
    axes[1, 0].set_title("Correlation Matrix")

    # Price vs Storage
    sns.boxplot(x='Storage', y='Price', data=df, ax=axes[1, 1])
    axes[1, 1].set_title("Price by Storage")
    axes[1, 1].tick_params(axis='x', rotation=45)

    # Availability
    availability_counts = df['Availability'].value_counts()
    axes[1, 2].pie(
        availability_counts,
        colors=['#66b3ff','#99ff99','#ffcc99'],
        labels=availability_counts.index,
        autopct='%1.1f%%',
        startangle=140
    )
    axes[1, 2].set_title("Availability Distribution")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()