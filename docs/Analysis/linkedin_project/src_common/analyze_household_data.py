import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from pathlib import Path

# Ensure paths work regardless of where script is called from
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "charts"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the CSV file with semicolon delimiter
def read_master_data(filename='Master.csv'):
    """Reads the relevant data from the CSV file."""
    try:
        file_path = DATA_DIR / filename
        # Read the file as text first to analyze its structure
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Print first few lines to debug
        print("First 10 lines of the CSV file:")
        for i, line in enumerate(lines[:10]):
            print(f"{i}: {line.strip()}")
        
        # Skip the first 7 rows which are headers
        data_lines = lines[7:]
        
        # Find where the actual data stops (before the notes section)
        end_idx = next((i for i, line in enumerate(data_lines) if 'tree - simulating' in line), len(data_lines))
        
        # Extract only the actual data rows
        data_rows = data_lines[:end_idx]
        
        # Parse the data manually
        countries = []
        currency_deposits = []
        insurance_pensions = []
        aic_gdp = []
        aic_cad = []
        cad_ins = []
        ins_fa = []
        fa_gdp = []
        
        for line in data_rows:
            if not line.strip():
                continue
                
            parts = line.strip().split(';')
            if len(parts) < 15:  # Ensure the line has enough columns
                continue
                
            country = parts[0].strip()
            curr_dep = parts[1].strip()
            ins_pen = parts[5].strip()
            
            # Check for GDP data (column 8/9)
            gdp_col = 8
            aic_col = 9
            aic_gdp_col = 10
            aic_cad_col = 11
            cad_ins_col = 12
            ins_fa_col = 13
            fa_gdp_col = 14
            
            # Only include rows that have a country name
            if country and country not in ('Country', ''):
                countries.append(country)
                currency_deposits.append(curr_dep)
                insurance_pensions.append(ins_pen)
                
                # Get the ratio values if they exist
                aic_gdp_val = parts[aic_gdp_col].strip() if aic_gdp_col < len(parts) else ''
                aic_cad_val = parts[aic_cad_col].strip() if aic_cad_col < len(parts) else ''
                cad_ins_val = parts[cad_ins_col].strip() if cad_ins_col < len(parts) else ''
                ins_fa_val = parts[ins_fa_col].strip() if ins_fa_col < len(parts) else ''
                fa_gdp_val = parts[fa_gdp_col].strip() if fa_gdp_col < len(parts) else ''
                
                aic_gdp.append(aic_gdp_val)
                aic_cad.append(aic_cad_val)
                cad_ins.append(cad_ins_val)
                ins_fa.append(ins_fa_val)
                fa_gdp.append(fa_gdp_val)
        
        # Create DataFrame
        df = pd.DataFrame({
            'Country': countries,
            'Currency and deposits': currency_deposits,
            'Insurance, pensions and standardised guarantees': insurance_pensions,
            'AIC ON GPD': aic_gdp,
            'AIC ON CAD': aic_cad,
            'CAD on INS': cad_ins,
            'Ins on FA': ins_fa,
            'FA ON GDP': fa_gdp
        })
        
        print("\nDataFrame created with shape:", df.shape)
        print("\nFirst few rows:")
        print(df.head())
        
        return df
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

# Create a bar chart comparing Italy and EU
def create_comparison_chart(df, column, title, filename):
    """Creates a bar chart comparing Italy and EU for a given metric."""
    # Filter for Italy and EU
    chart_data = df[df['Country'].isin(['Italy', 'EU'])].copy()
    
    # Clean the data - remove % signs and convert to float
    if chart_data[column].dtype == object:
        # European format handling: replace dots in thousands with nothing, then replace comma with dot
        chart_data[column] = chart_data[column].str.replace('%', '')
        chart_data[column] = chart_data[column].apply(lambda x: 
            float(x.replace('.', '').replace(',', '.')) if isinstance(x, str) else x
        )
    
    # Create a bar chart
    fig = px.bar(chart_data, x='Country', y=column, title=title,
                 color='Country', color_discrete_map={'Italy': 'green', 'EU': 'red'},
                 text_auto='.1%' if '%' in title else '.2f')
    
    # Update layout
    fig.update_layout(
        xaxis_title="",
        yaxis_title=title.split('(')[0].strip() if '(' in title else title,
        legend_title_text="",
        font=dict(size=14),
        height=500,
        width=800
    )
    
    # Save the chart
    output_path = OUTPUT_DIR / f"{filename}.png"
    html_path = OUTPUT_DIR / f"{filename}.html"
    fig.write_image(output_path)
    fig.write_html(html_path)
    
    return filename

# Create a bar chart showing EU countries ranking
def create_eu_ranking(df, column, title, filename, highlight_country='Italy'):
    """Creates a bar chart showing EU country rankings for a metric."""
    # Sort by the column value
    sorted_df = df.copy()
    
    # Clean the data - remove % signs and convert to float
    if sorted_df[column].dtype == object:
        # European format handling: replace dots in thousands with nothing, then replace comma with dot
        sorted_df[column] = sorted_df[column].str.replace('%', '')
        sorted_df[column] = sorted_df[column].apply(lambda x: 
            float(x.replace('.', '').replace(',', '.')) if isinstance(x, str) else x
        )
    
    # Sort after conversion
    sorted_df = sorted_df.sort_values(by=column, ascending=False)
    
    # Create a bar chart
    fig = px.bar(sorted_df, x='Country', y=column, title=title,
                 color='Country', color_discrete_map={highlight_country: 'green'},
                 text_auto='.1%' if '%' in title else '.2f')
    
    # Update layout
    fig.update_layout(
        xaxis_title="",
        yaxis_title=title.split('(')[0].strip() if '(' in title else title,
        legend_title_text="",
        font=dict(size=14),
        height=500,
        width=1200,
        showlegend=False
    )
    
    # Update axis - rotate country labels for readability
    fig.update_xaxes(tickangle=45)
    
    # Save the chart
    output_path = OUTPUT_DIR / f"{filename}.png"
    html_path = OUTPUT_DIR / f"{filename}.html"
    fig.write_image(output_path)
    fig.write_html(html_path)
    
    return filename

# Create a radar chart comparing Italy to EU
def create_radar_chart(df, columns, title, filename):
    """Creates a radar chart comparing Italy and EU across multiple metrics."""
    # Filter for Italy and EU
    chart_data = df[df['Country'].isin(['Italy', 'EU'])].copy()
    
    # Clean the data for each column
    for col in columns:
        if chart_data[col].dtype == object:
            # European format handling: replace dots in thousands with nothing, then replace comma with dot
            chart_data[col] = chart_data[col].str.replace('%', '')
            chart_data[col] = chart_data[col].apply(lambda x: 
                float(x.replace('.', '').replace(',', '.')) if isinstance(x, str) else x
            )
    
    # Create radar chart for Italy and EU
    fig = go.Figure()
    
    for i, country in enumerate(chart_data['Country']):
        fig.add_trace(go.Scatterpolar(
            r=chart_data.iloc[i][columns].values,
            theta=columns,
            fill='toself',
            name=country,
            line_color='green' if country == 'Italy' else 'red'
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            ),
        ),
        title=title,
        height=600,
        width=800
    )
    
    # Save the chart
    output_path = OUTPUT_DIR / f"{filename}.png"
    html_path = OUTPUT_DIR / f"{filename}.html"
    fig.write_image(output_path)
    fig.write_html(html_path)
    
    return filename

# Create inflation impact visualization
def create_inflation_impact(initial_amount=1.5, inflation_rate=0.053, years=5, filename='inflation_impact'):
    """Creates a chart showing the impact of inflation on cash holdings."""
    # Calculate the erosion of value over 5 years with 5.3% inflation
    years_range = list(range(years + 1))
    values = [initial_amount * (1 - inflation_rate) ** year for year in years_range]
    lost_value = [initial_amount - value for value in values]
    
    # Create the visualization
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add value over time line
    fig.add_trace(
        go.Scatter(
            x=years_range,
            y=values,
            name="Remaining Value",
            line=dict(color="green", width=3)
        )
    )
    
    # Add bar chart showing lost value
    fig.add_trace(
        go.Bar(
            x=years_range,
            y=lost_value,
            name="Lost Value",
            marker_color="red"
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_layout(
        title_text=f"Impact of {inflation_rate*100:.1f}% Annual Inflation on €{initial_amount:.1f} Trillion",
        xaxis_title="Years",
    )
    
    # Update y-axes
    fig.update_yaxes(title_text="Remaining Value (Trillion €)", secondary_y=False)
    fig.update_yaxes(title_text="Lost Value (Trillion €)", secondary_y=True)
    
    # Save the chart
    output_path = OUTPUT_DIR / f"{filename}.png"
    html_path = OUTPUT_DIR / f"{filename}.html"
    fig.write_image(output_path)
    fig.write_html(html_path)
    
    return filename

# Main function
def main():
    # Read the data
    df = read_master_data()
    
    if df is not None:
        # Create comparison charts
        create_comparison_chart(df, 'Currency and deposits', 'Currency and Deposits (Trillion €)', 'italy_eu_deposits')
        create_comparison_chart(df, 'Insurance, pensions and standardised guarantees', 'Insurance & Pensions (Trillion €)', 'italy_eu_insurance')
        create_comparison_chart(df, 'CAD on INS', 'Currency & Deposits to Insurance Ratio (%)', 'italy_eu_cad_ins_ratio')
        create_comparison_chart(df, 'Ins on FA', 'Insurance to Financial Assets Ratio (%)', 'italy_eu_ins_fa_ratio')
        
        # Create EU rankings
        create_eu_ranking(df, 'Currency and deposits', 'EU Countries by Cash Holdings (Trillion €)', 'eu_deposits_ranking')
        create_eu_ranking(df, 'CAD on INS', 'EU Countries by Cash to Insurance Ratio (%)', 'eu_cad_ins_ranking')
        create_eu_ranking(df, 'Ins on FA', 'EU Countries by Insurance to Financial Assets Ratio (%)', 'eu_ins_fa_ranking')
        
        # Create radar chart
        radar_columns = ['AIC ON GPD', 'AIC ON CAD', 'CAD on INS', 'Ins on FA', 'FA ON GDP']
        create_radar_chart(df, radar_columns, 'Financial Indicators - Italy vs EU', 'italy_eu_radar')
        
        # Create inflation impact chart
        create_inflation_impact()
        
        print("Charts created successfully")
    else:
        print("Failed to read data")

if __name__ == "__main__":
    main() 