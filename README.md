# 🎮 Gaming Laptops Data Science Project (Tunisia)

## 📌 Project Overview 

This **Data Science project** aims to help **gamers, students, and general users in Tunisia** choose the **best price / quality gaming laptop**.
### website : https://www.tunisianet.com.tn/

The project follows the **full data science pipeline**:
- Data collection (web scraping)
- Data cleaning & preprocessing
- Exploratory Data Analysis (EDA)
- Machine learning model (future step)
- Dashboard & deployment

All steps are implemented using **Python and its data science libraries**.

---

## 🧰 Technologies & Libraries Used

- Python  
- Pandas, NumPy  
- Selenium (Web Scraping)  
- Matplotlib, Seaborn  
- Plotly & Dash  

---

## ⚙️ How to Run the Project

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
## 📂 Project Structure
````text
DS-project/
│├── assets/
           ├──custom.css
├── 1scrap.py # Data collection (web scraping)
├── 2cleaning.py # Data cleaning & preprocessing
├── 3plotting.py # Visualization functions
├── 4app.py # Dash dashboard
├── 4EDA.py # Exploratory Data Analysis
├── 5model.py
├── EDA_Using_BI.pbix
├── gaming_laptops.csv # df using first scraping method-(Title Split)
├── gaming_laptops2.csv # df using second scraping method-(Description Parsing)
├── gaming_laptops2_cleaned.csv
�   links.txt # HTML code ! 
├── requirements.txt
└── README.md
````

---

## 🕷️ 1. Data Collection (Scrapping.py)

Data was collected using **Selenium** because the source website is **dynamic**, so traditional scraping tools like *BeautifulSoup* were not suitable.

### Key Points:
- Selenium was used to navigate pages and handle pagination
- Website structure was inspected to identify required HTML classes
- Pandas was used to store the data in a DataFrame
- The final dataset was saved as a CSV file

### Scraping Methods:
Two scraping approaches were used:
1. **Title-based extraction** (string splitting)
2. **Description parsing**

After comparison, the **title-based method contained more missing values**, so the description-based method was not used.

---

## 🧹 2. Data Cleaning & Preprocessing

Data cleaning was performed to improve data quality and consistency.

### Cleaning Steps:
- Used the first DataFrame to fill missing values in the second DataFrame
- Converted **Price** and **Warranty (Garentie)** to correct numeric formats
- Removed duplicate records
- Fixed GPU naming inconsistencies  
  Example: `RTX 3050 4GB` and `RTX 3050` were treated as the same GPU
- Filled missing categorical values:
  - `GPU` and `Color` were filled with `"Not Listed"`  
  - These represented less than **1%** of the data

### Notes:
- The **Refresh Rate** feature had many missing values
- No imputation was done because most screens had **144Hz or higher**
- This feature was not used in further analysis

---

## 📊 3.4. Exploratory Data Analysis (EDA)

EDA was conducted using:
1- PowerBI
2- Dash and Plotly
3- Python libraries : 
  - Matplotlib
  - Seaborn
  - Pandas built-in functions

### Visualizations:
I used PowerBI to create the dashboard, because it is more user-friendly and it is easier to create interactive dashboards ! And i have created an interactive dashboard using Dash and Plotly. Some of the visualizations are:

- Price distribution
- Price vs GPU
- Price vs Storage
- RAM distribution
- Correlation heatmap
- Availability distribution

### Plotting Strategy:
Two visualization approaches were implemented in `plotting.py`:
1. `individual_plots()` – single charts
2. `subplots()` – grouped dashboard-style figures

These functions were later used in `EDA.py`.

Additionally, Pandas functions such as:
- `head()`
- `describe()`
- `value_counts()`

were used for quick statistical insights.

---

## 📊 5. Machine Learning Model

## 🤖 5. Machine Learning & Price Prediction

In this phase, I developed a predictive model to estimate gaming laptop prices in the Tunisian market. The goal was to transform technical specifications into a reliable price valuation tool.

### 🛠️ Modeling Workflow
My code implements a robust pipeline to handle categorical text data and non-linear price distributions:

1.  **Feature Engineering:** * Converted **RAM** and **Storage** strings into numeric integers.
    * Extracted **Brand** names using a custom mapping function.
    * Converted **Availability** into a binary format (1 for "En stock", 0 for others).
2.  **Categorical Encoding:** Applied `pd.get_dummies` with `drop_first=True` to the **Brand, CPU, and GPU** columns. This created a high-dimensional numeric matrix suitable for regression.
3.  **Target Optimization:** To address the right-skewed nature of laptop prices, I applied a **Log Transformation** (`np.log1p`) to the Price. This stabilized the model and significantly reduced error margins.

### 📊 Model Comparison & Results
I evaluated three different algorithms to find the best fit for this dataset:

| Model | MAE (Mean Absolute Error) | R² Score (Accuracy) |
| :--- | :--- | :--- |
| **Linear Regression (Baseline)** | 312.38 DT | 0.8301 |
| **Random Forest** | 347.43 DT | - |
| **Gradient Boosting** | 432.30 DT | - |
| **Optimized Linear Regression (Log)** | **259.49 DT** | **0.8647** |



### 📈 Final Output Analysis
The optimized model achieved an **86.47% accuracy**, meaning it explains nearly 87% of the price variations on the website.

#### Top 5 Price Drivers (Highest Positive Impact)
These features add the most value to a laptop's price in Tunisia:
1.  **GPU: RTX 5090** (Weight: 1.08)
2.  **GPU: RTX 5080** (Weight: 0.85)
3.  **CPU: Intel Core i9-14900HX** (Weight: 0.80)
4.  **GPU: RTX 4090** (Weight: 0.80)
5.  **CPU: Intel Core I7-13650HX** (Weight: 0.61)

#### Top 5 Value Indicators (Highest Negative Impact)
Features that signify entry-level or budget-friendly pricing:
1.  **GPU: RTX 2050** (Weight: -0.23)
2.  **Brand: LENOVO** (Weight: -0.18)
3.  **GPU: RTX 3050** (Weight: -0.10)
4.  **Brand: DELL** (Weight: -0.03)
5.  **Brand: GIGABYTE** (Weight: -0.005)



---
**Conclusion:** The model proves that while the GPU is the primary driver of cost, brand positioning (like LENOVO's aggressive pricing) plays a significant role in market valuation.


---

## 🚀 6. Deployment
The last step is to deploy the model to a web application. I used Streamlit to create a simple web application that can be used to predict the price of a laptop.
To run the app, copy this command in the terminal : 

```bash
streamlit run 6deploy.py
```

---

## 👤 Author

**Wissem Sahli**  




















