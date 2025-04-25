import pandas as pd
import plotly.graph_objects as go
import country_converter as coco
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import base64
import os
from scipy import stats
import math

def convert_european_number(x):
    if pd.isna(x):
        return np.nan
    try:
        # Remove any leading/trailing whitespace and tabs
        x = str(x).strip().replace('\t', '')
        # Remove % sign if present
        x = x.rstrip('%')
        # Replace comma with dot for decimal point
        x = x.replace('.', '').replace(',', '.')
        return float(x)
    except:
        return np.nan

def calculate_trendline(x, y):
    """Calculate trendline and R-squared value"""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r_squared = r_value**2
    line_x = np.array([min(x), max(x)])
    line_y = slope * line_x + intercept
    return line_x, line_y, r_squared

# Read the data
df = pd.read_csv('Fonti per post linkedin liquidità/Master Dati Eurostat.csv', 
                 skiprows=1,  # Skip only the first row to get proper column alignment
                 sep=';', 
                 na_values=[':'])

# Clean up the data - now include all countries except the EU row (which is at the end)
df = df[df['Country'].notna() & (df['Country'] != 'EU')]  # Remove empty rows and EU row

# Convert all relevant columns
columns_to_convert = {
    'Legend': 0,  # Column A
    'Country': 1,  # Column B
    'Currency and deposits': 2,  # Column C
    'Debt securities': 3,  # Column D
    'Loans': 4,  # Column E
    'Equity and investment fund shares': 5,  # Column F
    'Insurance, pensions and standardised guarantees': 6,  # Column G
    'Financial derivatives and employee stock options': 7,  # Column H
    'Other accounts receivable/\npayable': 8,  # Column I
    'GDP 2023 Billion Euro': 9,  # Column J
    'AIC 2023': 10,  # Column K
    'pop M': 16,  # Column Q
    'AIC per person': 17,  # Column R
    'Ins on FA': 14,  # Column O
}

# Create clean DataFrame with converted values
clean_df = pd.DataFrame()
for col_name, col_idx in columns_to_convert.items():
    if col_name in ['Legend', 'Country']:
        clean_df[col_name] = df.iloc[:, col_idx].str.strip()
    else:
        clean_df[col_name] = df.iloc[:, col_idx].apply(convert_european_number)

# Calculate total financial assets and percentages for pie charts
financial_columns = [
    'Currency and deposits',
    'Equity and investment fund shares',
    'Insurance, pensions and standardised guarantees',
    'Debt securities',
    'Loans',
    'Financial derivatives and employee stock options',
    'Other accounts receivable/\npayable'
]

# Calculate total financial assets
clean_df['Total Financial Assets'] = clean_df[financial_columns].sum(axis=1)

# Calculate percentages for each financial asset type
for col in financial_columns:
    clean_df[f'{col}_pct'] = clean_df[col] / clean_df['Total Financial Assets'] * 100

# Create simplified categories for pie chart
clean_df['Other Financial Assets_pct'] = clean_df[[
    'Debt securities_pct', 
    'Loans_pct', 
    'Financial derivatives and employee stock options_pct', 
    'Other accounts receivable/\npayable_pct'
]].sum(axis=1)

# Convert Insurance ratio to percentage
clean_df['Ins on FA'] = clean_df['Ins on FA'] / 100

# Get ISO codes for flags
clean_df['ISO'] = coco.convert(names=clean_df['Country'].tolist(), to='ISO2')
clean_df.loc[clean_df['Country'] == 'EU', 'ISO'] = 'EU'

# Create flag emoji Unicode strings
clean_df['flag'] = clean_df['ISO'].apply(lambda x: '🇪🇺' if x == 'EU' else 
    ''.join(chr(ord(c) + 127397) for c in x))

# Calculate bubble sizes
max_bubble_size = 60
min_bubble_size = 20
clean_df['bubble_size'] = clean_df['AIC 2023']

# Create a color map for continents
continent_colors = {
    'Europe': '#1f77b4',
    'Asia': '#ff7f0e',
    'North America': '#2ca02c',
    'Oceania': '#d62728',
    'South America': '#9467bd',
    'Africa': '#8c564b'
}

# Function to create hover text
def create_hover_text(row):
    return (
        f"<b>{row['Country']} {row['flag']}</b><br><br>"
        f"AIC per person: {row['AIC per person']:,.2f}K€<br>"
        f"Insurance on Financial Assets: {row['Ins on FA'] * 100:.1f}%<br>"
        f"AIC 2023: {row['AIC 2023']:,.0f}M€<br>"
        f"<br>"
        f"Total FA: {row['Total Financial Assets']:,.1f}B€<br>"
        f"Financial Assets Distribution:<br>"
        f"Cash & dep share: {row['Currency and deposits_pct']:.1f}%<br>"
        f"Ins share: {row['Insurance, pensions and standardised guarantees_pct']:.1f}%<br>"
        f"Equity share: {row['Equity and investment fund shares_pct']:.1f}%<br>"
        f"Other: {row['Other Financial Assets_pct']:.1f}%"
    )

# Function to add a trace for a group of countries
def add_country_trace(data, color, name):
    hover_texts = data.apply(create_hover_text, axis=1)
    
    # Add the bubbles
    fig.add_trace(go.Scatter(
        x=data['AIC per person'],
        y=data['Ins on FA'],
        mode='markers+text',
        name=name,
        text=data.apply(lambda x: f"{x['Country']} {x['flag']}", axis=1),
        textposition='top center',
        textfont=dict(
            size=11,
            color='rgba(50, 50, 50, 0.8)'
        ),
        hovertext=hover_texts,
        hoverinfo='text',
        marker=dict(
            size=data['bubble_size'],
            sizeref=max(clean_df['AIC 2023']) / (60**2),
            sizemode='area',
            color=color,
            line=dict(color='white', width=1),
            opacity=0.7
        ),
        showlegend=True
    ))
    
    # Add trend line for this group
    if len(data) > 1:  # Only add trend line if we have more than one point
        line_x, line_y, r_squared = calculate_trendline(data['AIC per person'], data['Ins on FA'])
        fig.add_trace(go.Scatter(
            x=line_x,
            y=line_y,
            mode='lines',
            name=f'{name} trend (R² = {r_squared:.2f})',
            line=dict(
                color=color,
                dash='dot',
                width=1
            ),
            opacity=0.7,
            showlegend=True
        ))

# Create the main figure
fig = go.Figure()

# Split data into regions based on Legend column
italy_data = clean_df[clean_df['Legend'] == 'Italy']
top_17_data = clean_df[clean_df['Legend'] == 'Top 17']
other_countries = clean_df[clean_df['Legend'] == 'Other']

# Sort data by x-value for better label placement
italy_data = italy_data.sort_values('AIC per person')
top_17_data = top_17_data.sort_values('AIC per person')
other_countries = other_countries.sort_values('AIC per person')

# Add traces for each region with specific colors
add_country_trace(italy_data, '#008C45', 'Italy')  # Green for Italy
add_country_trace(top_17_data, '#1f77b4', 'Top 17 Countries')  # Blue for top countries
add_country_trace(other_countries, '#D3D3D3', 'Other Countries')  # Light grey for others

# Add overall trend line for all visible points
all_data = pd.concat([italy_data, top_17_data, other_countries])
line_x, line_y, r_squared = calculate_trendline(all_data['AIC per person'], all_data['Ins on FA'])
fig.add_trace(go.Scatter(
    x=line_x,
    y=line_y,
    mode='lines',
    name=f'Overall trend (R² = {r_squared:.2f})',
    line=dict(
        color='black',
        dash='dot',
        width=1.5
    ),
    opacity=0.5,
    showlegend=True
))

# Update layout
fig.update_layout(
    title=dict(
        text='European Household Financial Indicators 2023',
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='top',
        font=dict(size=24)
    ),
    xaxis_title=dict(
        text='AIC per person (K€)',
        font=dict(size=14)
    ),
    yaxis_title=dict(
        text='Insurance on Financial Assets (%)',
        font=dict(size=14)
    ),
    hovermode='closest',
    template='plotly_white',
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor="Black",
        borderwidth=1,
        itemsizing='constant',
        itemclick='toggle',
        itemdoubleclick=False
    ),
    margin=dict(l=80, r=80, t=100, b=100),
    width=1200,
    height=800
)

# Add custom JavaScript for legend-label sync
fig.update_layout(
    updatemenus=[{
        'buttons': [],
        'direction': 'left',
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'y': 1.1,
        'xanchor': 'right',
        'yanchor': 'top'
    }],
    annotations=[
        dict(
            text='',
            showarrow=False,
            x=0,
            y=1.1,
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top'
        )
    ]
)

# Update the watermark/source annotation
fig.add_annotation(
    text="Sources: Eurostat - Households statistics on financial assets and liabilities, 2023;<br>Eurostat - GDP per capita, consumption per capita and price level indices<br>Author analysis",
    xref="paper",
    yref="paper",
    x=0.98,
    y=0.02,
    showarrow=False,
    font=dict(size=10, color="gray"),
    xanchor="right",
    yanchor="bottom",
    align="right"
)

# Add bubble size legend
fig.add_annotation(
    text="Bubble size represents<br>Actual Individual<br>Consumption (AIC)",
    xref="paper",
    yref="paper",
    x=0.98,
    y=0.15,
    showarrow=False,
    font=dict(size=10),
    xanchor="right",
    yanchor="bottom",
    align="right",
    bgcolor="rgba(255, 255, 255, 0.8)",
    bordercolor="gray",
    borderwidth=1,
    borderpad=4
)

# Create the HTML outputs directory if it doesn't exist
os.makedirs("HTML outputs", exist_ok=True)

# Save the figure
fig.write_html("HTML outputs/household_financial_indicators.html")
print("Visualization has been saved to 'HTML outputs/household_financial_indicators.html'") 