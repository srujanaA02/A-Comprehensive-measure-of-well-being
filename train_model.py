import os
import sys
import requests
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for generating plots without UI
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import joblib

# Import Config
from config import Config

def download_dataset():
    """Downloads the official UNDP HDI dataset or generates a synthetic one if download fails."""
    Config.init_app()
    print("Attempting to download official UNDP HDI dataset...")
    try:
        response = requests.get(Config.RAW_DATA_URL, timeout=15)
        if response.status_code == 200:
            with open(Config.RAW_DATA_PATH, 'wb') as f:
                f.write(response.content)
            print(f"Dataset successfully downloaded to {Config.RAW_DATA_PATH}")
            return True
        else:
            print(f"UNDP Server responded with status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
    
    # Fallback to local file check
    if os.path.exists(Config.RAW_DATA_PATH):
        print(f"Using existing raw dataset found at {Config.RAW_DATA_PATH}")
        return True
        
    print("Falling back to generating a realistic synthetic HDI dataset...")
    generate_synthetic_dataset()
    return False

def generate_synthetic_dataset():
    """Generates a realistic HDI dataset based on UNDP parameters and formulas."""
    np.random.seed(42)
    countries = [
        "United States", "Germany", "Japan", "United Kingdom", "Canada", "Australia", "France",
        "Norway", "Sweden", "Switzerland", "Singapore", "South Korea", "China", "India",
        "Brazil", "Russia", "South Africa", "Mexico", "Indonesia", "Nigeria", "Kenya",
        "Ethiopia", "Egypt", "Pakistan", "Bangladesh", "Vietnam", "Turkey", "Saudi Arabia",
        "Argentina", "Colombia", "Peru", "Chile", "Ghana", "Morocco", "Nepal", "Yemen"
    ]
    
    records = []
    # Generate 150 records per country across years 1990-2021 (approx 4500 samples)
    for country in countries:
        # Assign base country profiles
        if country in ["United States", "Germany", "Japan", "United Kingdom", "Canada", "Australia", "France", "Norway", "Sweden", "Switzerland", "Singapore", "South Korea"]:
            # Very High Development profile
            base_le = 78.0
            base_eys = 15.0
            base_mys = 11.5
            base_gni = 45000.0
            growth = 1.05 # slow growth
        elif country in ["China", "Brazil", "Russia", "Mexico", "Turkey", "Saudi Arabia", "Argentina", "Colombia", "Peru", "Chile", "Egypt", "South Africa"]:
            # High/Medium Development profile
            base_le = 68.0
            base_eys = 11.0
            base_mys = 8.0
            base_gni = 12000.0
            growth = 1.15 # moderate growth
        elif country in ["India", "Indonesia", "Pakistan", "Bangladesh", "Vietnam", "Morocco"]:
            # Medium Development profile
            base_le = 60.0
            base_eys = 9.0
            base_mys = 5.5
            base_gni = 3500.0
            growth = 1.25 # faster growth
        else:
            # Low Development profile
            base_le = 52.0
            base_eys = 7.0
            base_mys = 3.5
            base_gni = 1200.0
            growth = 1.30 # volatile growth
            
        for year in range(1990, 2022):
            year_factor = (year - 1990) / 32
            # Add growth and noise to indicators
            le = base_le + (10 * year_factor * (growth - 0.1)) + np.random.normal(0, 0.5)
            eys = base_eys + (4 * year_factor * (growth - 0.15)) + np.random.normal(0, 0.3)
            mys = base_mys + (3 * year_factor * (growth - 0.15)) + np.random.normal(0, 0.3)
            gni = base_gni * (1.0 + (growth - 1.0) * year_factor) + np.random.normal(0, base_gni * 0.05)
            
            # Clip indicators to physical ranges
            le = np.clip(le, 20.0, 85.0)
            eys = np.clip(eys, 0.0, 20.0)
            mys = np.clip(mys, 0.0, 15.0)
            gni = np.clip(gni, 100.0, 95000.0)
            
            # Calculate exact HDI using UN formula
            # Health index
            i_health = (le - 20.0) / (85.0 - 20.0)
            # Education index
            i_education = ((mys / 15.0) + (eys / 18.0)) / 2.0
            # Income index (capped at 75,000 for standard calculation)
            gni_clamped = min(gni, 75000.0)
            i_income = (np.log(gni_clamped) - np.log(100.0)) / (np.log(75000.0) - np.log(100.0))
            
            # Geometric mean
            hdi = (i_health * i_education * i_income) ** (1/3)
            # Add minor random variation/noise to represent real data variance
            hdi = np.clip(hdi + np.random.normal(0, 0.005), 0.0, 1.0)
            
            records.append({
                'country': country,
                'year': year,
                'life_expectancy': round(le, 1),
                'expected_years_schooling': round(eys, 1),
                'mean_years_schooling': round(mys, 1),
                'gni_per_capita': round(gni, 1),
                'hdi': round(hdi, 3)
            })
            
    df = pd.DataFrame(records)
    df.to_csv(Config.PROCESSED_DATA_PATH, index=False)
    print(f"Generated synthetic processed dataset with {len(df)} records at {Config.PROCESSED_DATA_PATH}")

def preprocess_raw_data():
    """Parses raw wide format UNDP file, reshapes it, and cleans it."""
    if not os.path.exists(Config.RAW_DATA_PATH):
        print("Raw dataset file does not exist. Using synthetic fallback.")
        if not os.path.exists(Config.PROCESSED_DATA_PATH):
            generate_synthetic_dataset()
        return
        
    print("Preprocessing raw UNDP dataset...")
    try:
        raw_df = pd.read_csv(Config.RAW_DATA_PATH)
        
        # Check columns
        required_cols = ['country', 'iso3']
        for col in required_cols:
            if col not in raw_df.columns:
                raise ValueError(f"Required identifier column '{col}' missing from raw data.")
                
        # We need: hdi, le, eys, mys, gni_pc for years 1990-2021
        years = list(range(1990, 2022))
        records = []
        
        for idx, row in raw_df.iterrows():
            country = row['country']
            iso3 = row['iso3']
            
            # Skip region/aggregate records (usually uppercase iso3 or specific categories)
            if pd.isna(iso3) or len(str(iso3).strip()) != 3:
                continue
                
            for year in years:
                # Check for headers in the format: hdi_YYYY, le_YYYY, eys_YYYY, mys_YYYY, gni_pc_YYYY
                hdi_col = f'hdi_{year}'
                le_col = f'le_{year}'
                eys_col = f'eys_{year}'
                mys_col = f'mys_{year}'
                gni_col = f'gni_pc_{year}'
                
                # Check if these exist in the columns
                if all(col in raw_df.columns for col in [hdi_col, le_col, eys_col, mys_col, gni_col]):
                    hdi_val = row[hdi_col]
                    le_val = row[le_col]
                    eys_val = row[eys_col]
                    mys_val = row[mys_col]
                    gni_val = row[gni_col]
                    
                    # Skip if variables are null or invalid
                    if pd.isna(hdi_val) or pd.isna(le_val) or pd.isna(eys_val) or pd.isna(mys_val) or pd.isna(gni_val):
                        continue
                        
                    try:
                        records.append({
                            'country': country,
                            'iso3': iso3,
                            'year': int(year),
                            'life_expectancy': float(le_val),
                            'expected_years_schooling': float(eys_val),
                            'mean_years_schooling': float(mys_val),
                            'gni_per_capita': float(gni_val),
                            'hdi': float(hdi_val)
                        })
                    except ValueError:
                        continue
                        
        if len(records) == 0:
            print("No valid records extracted from raw file. Falling back to synthetic.")
            generate_synthetic_dataset()
            return
            
        processed_df = pd.DataFrame(records)
        # Drop duplicates and clean missing values
        processed_df = processed_df.drop_duplicates()
        processed_df = processed_df.dropna()
        
        # Save processed dataset
        processed_df.to_csv(Config.PROCESSED_DATA_PATH, index=False)
        print(f"Preprocessed raw data. Created {len(processed_df)} tidy records in {Config.PROCESSED_DATA_PATH}")
        
    except Exception as e:
        print(f"Exception while preprocessing raw data: {e}. Generating synthetic fallback.")
        generate_synthetic_dataset()

def generate_eda_plots(df):
    """Generates all exploratory data analysis plots and saves them as images."""
    print("Generating EDA visualizations...")
    Config.init_app()
    
    # Use standard seaborn style context
    sns.set_theme(style="whitegrid")
    
    # 1. Heatmap / Correlation Matrix
    plt.figure(figsize=(8, 6))
    corr = df[['life_expectancy', 'expected_years_schooling', 'mean_years_schooling', 'gni_per_capita', 'hdi']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".3f", linewidths=0.5)
    plt.title('Correlation Matrix of HDI Components')
    plt.tight_layout()
    plt.savefig(os.path.join(Config.PLOTS_DIR, 'correlation_matrix.png'), dpi=150)
    plt.close()
    
    # 2. Distribution Plot for HDI
    plt.figure(figsize=(8, 5))
    sns.histplot(df['hdi'], kde=True, color='teal', bins=30)
    plt.title('Distribution of Human Development Index (HDI)')
    plt.xlabel('HDI Value')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(Config.PLOTS_DIR, 'hdi_distribution.png'), dpi=150)
    plt.close()

    # 3. Scatter Plot: GNI vs HDI (with log scale for GNI)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='gni_per_capita', y='hdi', hue='year', palette='viridis', alpha=0.7)
    plt.xscale('log')
    plt.title('Gross National Income (GNI) per Capita vs HDI')
    plt.xlabel('GNI per Capita (PPP $, Log Scale)')
    plt.ylabel('HDI')
    plt.tight_layout()
    plt.savefig(os.path.join(Config.PLOTS_DIR, 'gni_vs_hdi_scatter.png'), dpi=150)
    plt.close()
    
    # 4. Scatter Plot: Life Expectancy vs HDI
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='life_expectancy', y='hdi', color='coral', alpha=0.6)
    plt.title('Life Expectancy at Birth vs HDI')
    plt.xlabel('Life Expectancy (Years)')
    plt.ylabel('HDI')
    plt.tight_layout()
    plt.savefig(os.path.join(Config.PLOTS_DIR, 'life_expectancy_vs_hdi.png'), dpi=150)
    plt.close()

    # 5. Box Plots of features
    plt.figure(figsize=(12, 6))
    features = ['life_expectancy', 'expected_years_schooling', 'mean_years_schooling']
    for idx, feature in enumerate(features, 1):
        plt.subplot(1, 3, idx)
        sns.boxplot(y=df[feature], color=['skyblue', 'salmon', 'lightgreen'][idx-1])
        plt.title(f'Boxplot of {feature.replace("_", " ").title()}')
        plt.ylabel('')
    plt.tight_layout()
    plt.savefig(os.path.join(Config.PLOTS_DIR, 'box_plots.png'), dpi=150)
    plt.close()
    
    # 6. Pair Plot (subset of data for faster rendering)
    pair_df = df[['life_expectancy', 'expected_years_schooling', 'mean_years_schooling', 'gni_per_capita', 'hdi']].sample(
        min(800, len(df)), random_state=42
    )
    g = sns.pairplot(pair_df, diag_kind='kde', plot_kws={'alpha': 0.5})
    g.fig.suptitle('Pair Plot of HDI Features', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(Config.PLOTS_DIR, 'pair_plot.png'), dpi=150)
    plt.close()
    
    # 7. Strip Plot: HDI category vs GNI Per Capita
    # Define categories based on standard UN ranges
    df_cat = df.copy()
    def get_hdi_category(hdi):
        if hdi >= 0.800: return 'Very High'
        elif hdi >= 0.700: return 'High'
        elif hdi >= 0.550: return 'Medium'
        else: return 'Low'
    df_cat['hdi_category'] = df_cat['hdi'].apply(get_hdi_category)
    
    plt.figure(figsize=(8, 5))
    sns.stripplot(data=df_cat, x='hdi_category', y='gni_per_capita', hue='hdi_category', order=['Low', 'Medium', 'High', 'Very High'], jitter=0.2, alpha=0.5, legend=False)
    plt.yscale('log')
    plt.title('Distribution of GNI per Capita by HDI Category')
    plt.xlabel('HDI Category')
    plt.ylabel('GNI per Capita (PPP $, Log Scale)')
    plt.tight_layout()
    plt.savefig(os.path.join(Config.PLOTS_DIR, 'strip_plot.png'), dpi=150)
    plt.close()
    
    print("EDA Visualizations successfully generated and saved to static/plots/")

def train_and_save_model(df):
    """Trains the Linear Regression model, prints metrics, and serializes the model and scaler."""
    print("Training machine learning model...")
    # Features and Target
    X = df[['life_expectancy', 'expected_years_schooling', 'mean_years_schooling', 'gni_per_capita']]
    y = df['hdi']
    
    # Train-test split (80-20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    
    mae = metrics.mean_absolute_error(y_test, y_pred)
    mse = metrics.mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = metrics.r2_score(y_test, y_pred)
    
    print("\n" + "="*40)
    print("MODEL EVALUATION METRICS:")
    print("="*40)
    print(f"Mean Absolute Error (MAE):     {mae:.5f}")
    print(f"Mean Squared Error (MSE):       {mse:.5f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.5f}")
    print(f"R-squared (R2 Score):           {r2:.5f} ({r2*100:.2f}%)")
    print(f"Training R2 Score:              {model.score(X_train_scaled, y_train):.5f}")
    
    # Coefficients
    print("\nFeature Coefficients:")
    for feature, coef in zip(X.columns, model.coef_):
        print(f" - {feature:25}: {coef: .5f}")
    print(f" - Intercept                : {model.intercept_: .5f}")
    print("="*40 + "\n")
    
    # Create directory for models if missing
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    # Save model and scaler
    joblib.dump(model, Config.MODEL_PATH)
    joblib.dump(scaler, Config.SCALER_PATH)
    print(f"Model successfully saved to {Config.MODEL_PATH}")
    print(f"Scaler successfully saved to {Config.SCALER_PATH}")
    
    # Save evaluation report as a small text file for reference
    with open(os.path.join(Config.MODEL_DIR, 'evaluation_report.txt'), 'w') as f:
        f.write("HDI Predictor Model Evaluation Report\n")
        f.write("======================================\n")
        f.write(f"Model Type: Linear Regression\n")
        f.write(f"Train Dataset Size: {len(X_train)}\n")
        f.write(f"Test Dataset Size: {len(X_test)}\n\n")
        f.write(f"Mean Absolute Error (MAE):     {mae:.6f}\n")
        f.write(f"Mean Squared Error (MSE):       {mse:.6f}\n")
        f.write(f"Root Mean Squared Error (RMSE): {rmse:.6f}\n")
        f.write(f"R-squared (R2 Score):           {r2:.6f}\n\n")
        f.write("Coefficients:\n")
        for f_name, coef in zip(X.columns, model.coef_):
            f.write(f" - {f_name:25}: {coef: .6f}\n")
        f.write(f" - Intercept:                {model.intercept_: .6f}\n")
        
    return r2

def main():
    """Main execution function."""
    print("Starting HDI Predictor Pipeline...")
    
    # 1. Download/load dataset
    download_dataset()
    
    # 2. Preprocess data
    preprocess_raw_data()
    
    # 3. Read processed dataset
    if not os.path.exists(Config.PROCESSED_DATA_PATH):
        print(f"ERROR: Processed dataset not found at {Config.PROCESSED_DATA_PATH}")
        sys.exit(1)
        
    df = pd.read_csv(Config.PROCESSED_DATA_PATH)
    print(f"Dataset successfully loaded. Total records: {len(df)}")
    
    # Display dataset info & stats
    print("\nDataset Statistics Summary:")
    print(df.describe().to_string())
    print("\nMissing values in dataset:")
    print(df.isnull().sum())
    print(f"\nDuplicate records: {df.duplicated().sum()}")
    
    # 4. Generate EDA Visualizations
    generate_eda_plots(df)
    
    # 5. Train and serialize model
    train_and_save_model(df)
    
    print("HDI Predictor Pipeline completed successfully!")

if __name__ == '__main__':
    main()
