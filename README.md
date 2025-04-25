# European Household Financial Indicators Visualization

This project creates an interactive visualization of European household financial indicators using data from Eurostat. The visualization is a bubble chart that combines multiple dimensions of financial data to provide insights into household financial patterns across European countries.

## Features

### Main Visualization
- **Interactive Bubble Chart** showing the relationship between:
  - X-axis: Actual Individual Consumption (AIC) per person (K€)
  - Y-axis: Insurance on Financial Assets (%)
  - Bubble size: Actual Individual Consumption (AIC)

### Country Groupings
- Italy (highlighted)
- Top 17 European countries
- Other European countries

### Interactive Elements
- Hover information for each country showing:
  - Country name with flag
  - AIC per person
  - Insurance on Financial Assets percentage
  - AIC 2023
  - Total Financial Assets
  - Detailed breakdown of financial asset distribution

### Statistical Analysis
- Trend lines for each group with R² values
- Overall trend line showing the general relationship

## Data Sources
- Eurostat - Households statistics on financial assets and liabilities, 2023
- Eurostat - GDP per capita, consumption per capita and price level indices

## Requirements
```
pandas
plotly
country_converter
numpy
scipy
```

## Usage
1. Ensure all required packages are installed
2. Run the script:
```bash
python Scripts/create_bubble_chart.py
```
3. The visualization will be saved as an HTML file in the 'HTML outputs' directory

## Output
The script generates an interactive HTML file (`household_financial_indicators.html`) that can be opened in any modern web browser. The visualization is fully interactive, allowing for:
- Zooming
- Panning
- Hovering for detailed information
- Toggling different country groups and trend lines

## Analysis Features
- Comparison of financial asset allocation across countries
- Relationship between consumption levels and insurance penetration
- Country-specific detailed financial breakdowns
- Statistical trend analysis with R² values

## Project Structure

```
├── Fonti per post linkedin liquidità/   # Source data files
│   └── Master Dati Eurostat.csv        # Main Eurostat dataset
├── Scripts/                            # Python scripts
│   └── create_bubble_chart.py          # Bubble chart visualization script
├── HTML outputs/                       # Generated visualizations
│   └── household_financial_indicators.html  # Interactive bubble chart
├── requirements.txt                    # Python dependencies
└── README.md                          # Project documentation
```

## Setup Instructions

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Generate visualizations:
```bash
python Scripts/create_bubble_chart.py
```

## Dependencies

- pandas==2.1.4
- plotly==5.18.0
- numpy==1.26.2
- country_converter==1.0.0
- Other supporting libraries (see requirements.txt)

## Usage

1. The visualization can be viewed by opening `HTML outputs/household_financial_indicators.html` in a web browser
2. Interactive features:
   - Hover over bubbles for detailed information
   - Click legend items to show/hide groups
   - Use mouse wheel or touch gestures to zoom
   - Double-click to reset view

## Data Processing

The script handles:
- European number format conversion (comma as decimal separator)
- Proper scaling of bubble sizes
- Country code to flag emoji conversion
- Formatted number displays (currency and percentages)

## Future Enhancements

Potential areas for enhancement:
- Additional visualizations for other financial metrics
- Time series analysis of key indicators
- Comparative analysis tools
- Export capabilities to various formats

## Security Note

This repository contains data analysis and visualization code. No sensitive API keys or personal data are included.

## Overview

The strategy outlined in this repository is designed to:
- Strengthen the executive's position as a thought leader in applied AI for financial services
- Build visibility among target audiences (executives and headhunters)
- Demonstrate expertise through data-driven insights
- Subtly signal openness to new career opportunities

## Core Components

### Content Plan

The file `linkedin_post_plan_2025_revised.txt` contains a detailed posting schedule with:
- Post titles aligned with industry trends
- Content ideas for each post
- Optimal posting schedules (Monday mornings)
- Expected engagement metrics
- Relevant hashtags for maximum visibility

### Data Integration 

The `data_fetcher.py` script uses the Finnhub and NewsAPI services to:
- Gather real-time financial market data
- Track AI technology trends
- Monitor company performance
- Source relevant news articles
- Generate data-driven insights for post content

## Usage

1. Reference the LinkedIn post schedule for upcoming content topics
2. Two weeks before each scheduled post:
   - Run the data fetcher to gather current insights
   - Draft post content incorporating real-time market and technology trends
   - Refine based on current events and news
3. Post at scheduled time (Monday mornings between 8:30-9:30 AM CET)
4. Engage with comments within 2 hours of posting

## Content Strategy Guidelines

- Focus on thought leadership rather than self-promotion
- Share insights that demonstrate both technical and business understanding
- Balance deep expertise with accessible language for broad appeal
- Subtly signal openness to new opportunities through forward-looking statements
- Maintain professional tone while showcasing personality and leadership philosophy

## Security Note

This repository contains API keys and personal brand strategy. Handle with appropriate security measures:
- Add `news_config.json` to `.gitignore`
- Use environment variables in production environments
- Consider repository privacy settings 

# LinkedIn Financial Analysis Assistant

## Progress Log

### Bubble Chart Development (Version 1.0)
- Created interactive bubble chart showing European household financial indicators
- Features:
  - X-axis: AIC per person ($)
  - Y-axis: Insurance on Financial Assets (%)
  - Bubble size: Proportional to AIC 2023
  - Color coding: Italy (green), Other countries (light grey)
  - Interactive hover information showing:
    - Total Financial Assets
    - Financial asset distribution percentages
    - Country flags
    - Detailed financial metrics

### Next Planned Improvements
1. Update legend categories to:
   - Italy
   - Top 17 countries (Germany to Ireland)
   - Other countries
2. Add dynamic regression trend line
3. Optimize label positioning to prevent overlap
4. Add country flags next to labels in the chart 