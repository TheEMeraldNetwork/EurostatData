# app.py
import csv
from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio
import pandas as pd

app = Flask(__name__)

def read_data(filename='Master.csv'):
    """Reads the relevant data from the CSV file."""
    data = {}
    try:
        with open(filename, mode='r', encoding='utf-8') as infile:
            # Skip header rows and read with semicolon delimiter
            reader = csv.reader(infile, delimiter=';')
            # Skip the first 7 header/info lines
            for _ in range(7):
                next(reader)
            
            headers = next(reader) # Read the actual header row
            
            # Find column indices (adjust if CSV structure changes)
            try:
                country_col = headers.index('Country')
                aic_gdp_col = headers.index('AIC ON GPD')
                aic_cad_col = headers.index('AIC ON CAD')
                cad_ins_col = headers.index('CAD on INS')
                ins_fa_col = headers.index('Ins on FA')
                fa_gdp_col = headers.index('FA ON GDP')
            except ValueError as e:
                print(f"Error finding column headers: {e}")
                return None

            relevant_cols = [
                country_col, aic_gdp_col, aic_cad_col, 
                cad_ins_col, ins_fa_col, fa_gdp_col
            ]

            for row in reader:
                # Ensure row has enough columns before accessing indices
                if len(row) > max(relevant_cols):
                    country = row[country_col].strip()
                    if country in ["Italy", "EU"]:
                        try:
                            # Clean percentage signs and convert to float
                            data[country] = {
                                'AIC_GDP': float(row[aic_gdp_col].replace('%', '').strip()) / 100 if row[aic_gdp_col].strip() else None,
                                'AIC_CAD': float(row[aic_cad_col].replace('%', '').strip()) / 100 if row[aic_cad_col].strip() else None,
                                'CAD_INS': float(row[cad_ins_col].replace('%', '').strip()) / 100 if row[cad_ins_col].strip() else None,
                                'INS_FA': float(row[ins_fa_col].replace('%', '').strip()) / 100 if row[ins_fa_col].strip() else None,
                                # FA_GDP might not have '%', handle potential errors
                                'FA_GDP': float(row[fa_gdp_col].replace(',', '.').strip()) if row[fa_gdp_col].strip() else None 
                            }
                        except (ValueError, IndexError) as e:
                            print(f"Warning: Could not parse data for {country}: {e} - Row: {row}")
                            data[country] = {} # Or handle error appropriately

        # Check if both Italy and EU data were found
        if "Italy" not in data or "EU" not in data:
             print("Warning: Could not find data for both Italy and EU in the CSV.")
             return None
             
        return data

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except Exception as e:
        print(f"An error occurred during CSV processing: {e}")
        return None


def create_bar_chart(data, y_col, title, y_format='.1%'):
    """Creates a Plotly bar chart comparing Italy and EU for a given metric."""
    if not data or not data.get("Italy") or not data.get("EU"):
        return "<div>Error generating chart: Data unavailable</div>"
        
    plot_data = [
        {'Region': 'Italy', 'Value': data['Italy'].get(y_col)},
        {'Region': 'EU', 'Value': data['EU'].get(y_col)}
    ]
    # Filter out entries with None values
    plot_data = [item for item in plot_data if item['Value'] is not None]
    
    if not plot_data:
         return f"<div>Error generating chart '{title}': No valid data for Italy or EU</div>"

    df = pd.DataFrame(plot_data)
    
    fig = px.bar(df, x='Region', y='Value', title=title,
                 color='Region', color_discrete_map={'Italy': 'green', 'EU': 'red'},
                 labels={'Value': title.split('(')[0].strip()}) # Use cleaner label
    fig.update_layout(yaxis_tickformat=y_format, showlegend=False)
    
    # Convert figure to HTML div
    chart_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')
    return chart_html

@app.route('/')
def index():
    """Renders the infographic page."""
    household_data = read_data()
    
    if household_data is None:
        # Render a basic error page or message if data loading fails
        return "<h1>Error loading data from Master.csv</h1><p>Please check the file and Flask console output.</p>", 500

    # Generate charts
    chart_aic_gdp = create_bar_chart(household_data, 'AIC_GDP', 'Actual Individual Consumption / GDP')
    chart_aic_cad = create_bar_chart(household_data, 'AIC_CAD', 'Actual Individual Consumption / Currency & Deposits')
    chart_cad_ins = create_bar_chart(household_data, 'CAD_INS', 'Currency & Deposits / Insurance & Pensions')
    chart_ins_fa = create_bar_chart(household_data, 'INS_FA', 'Insurance & Pensions / Financial Assets')
    chart_fa_gdp = create_bar_chart(household_data, 'FA_GDP', 'Financial Assets / GDP', y_format = '.1f') # Not a percentage

    return render_template('index.html',
                           chart_aic_gdp=chart_aic_gdp,
                           chart_aic_cad=chart_aic_cad,
                           chart_cad_ins=chart_cad_ins,
                           chart_ins_fa=chart_ins_fa,
                           chart_fa_gdp=chart_fa_gdp)

if __name__ == '__main__':
    app.run(debug=True) # debug=True is helpful for development 