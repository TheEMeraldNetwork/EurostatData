#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a driver tree visualization of financial ratios for Italian households
Resembling the handwritten sketch in IMG_3757.png
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patheffects as path_effects
from matplotlib.path import Path
from matplotlib.patches import Rectangle, FancyArrowPatch, ConnectionPatch
import os
from pathlib import Path as PathLib
import csv

# Project structure
DATA_PATH = "Master.csv"
OUTPUT_DIR = PathLib("assets") / "driver_tree"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_csv_data():
    """Parse the CSV data to extract Italy and EU information."""
    italy_data = {}
    eu_data = {}
    
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Find header row to identify column positions
        header_row = None
        for i, line in enumerate(lines):
            if line.strip().startswith('Country;'):
                header_row = i
                break
        
        if header_row is None:
            raise ValueError("Could not find header row in CSV file")
        
        # Helper function to safely convert European number format
        def safe_convert(value_str):
            if not value_str.strip():
                return 0.0
            
            # Remove % if present
            value_str = value_str.replace('%', '').strip()
            
            try:
                # Replace dot in thousands and comma decimal separator with standard format
                # First, remove dots (thousands separators)
                value_str = value_str.replace('.', '')
                # Then replace comma with dot for decimal point
                value_str = value_str.replace(',', '.')
                return float(value_str)
            except ValueError:
                print(f"Warning: Could not convert '{value_str}' to float")
                return 0.0
        
        # Parse each line to find Italy and EU data
        for line in lines:
            if line.strip().startswith('Italy;'):
                parts = line.strip().split(';')
                italy_data = {
                    'Currency and deposits': safe_convert(parts[1]),
                    'Insurance': safe_convert(parts[5]),
                    'AIC ON GPD': safe_convert(parts[10]),
                    'AIC ON CAD': safe_convert(parts[11]),
                    'CAD on INS': safe_convert(parts[12]),
                    'Ins on FA': safe_convert(parts[13]),
                    'FA ON GDP': safe_convert(parts[14])
                }
            elif line.strip().startswith('EU;'):
                parts = line.strip().split(';')
                eu_data = {
                    'Currency and deposits': safe_convert(parts[1]),
                    'Insurance': safe_convert(parts[5]),
                    'AIC ON GPD': safe_convert(parts[10]),
                    'AIC ON CAD': safe_convert(parts[11]),
                    'CAD on INS': safe_convert(parts[12]),
                    'Ins on FA': safe_convert(parts[13]),
                    'FA ON GDP': safe_convert(parts[14])
                }
        
        if not italy_data or not eu_data:
            print("Warning: Could not find Italy or EU data in the CSV file. Using default values.")
            # If parsing failed, use hardcoded values
            italy_data = {
                'Currency and deposits': 1577.4,
                'Insurance': 1050.4,
                'AIC ON GPD': 69.0,
                'AIC ON CAD': 78.4,
                'CAD on INS': 150.2,
                'Ins on FA': 19.0,
                'FA ON GDP': 3.1
            }
            
            eu_data = {
                'Currency and deposits': 11627.3,
                'Insurance': 10020.7,
                'AIC ON GPD': 66.0,
                'AIC ON CAD': 80.4,
                'CAD on INS': 116.0,
                'Ins on FA': 27.0,
                'FA ON GDP': 2.6
            }
        
        print(f"Successfully parsed data: Italy CAD/INS={italy_data['CAD on INS']}, EU CAD/INS={eu_data['CAD on INS']}")
        return italy_data, eu_data
        
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        # Return default values if parsing fails
        return {
            'Currency and deposits': 1577.4,
            'Insurance': 1050.4,
            'AIC ON GPD': 69.0,
            'AIC ON CAD': 78.4,
            'CAD on INS': 150.2,
            'Ins on FA': 19.0,
            'FA ON GDP': 3.1
        }, {
            'Currency and deposits': 11627.3,
            'Insurance': 10020.7,
            'AIC ON GPD': 66.0,
            'AIC ON CAD': 80.4,
            'CAD on INS': 116.0,
            'Ins on FA': 27.0,
            'FA ON GDP': 2.6
        }

def create_bar_chart(ax, x_position, y_position, width, height, title, italy_value, eu_value, max_value=None):
    """Create a small bar chart at the specified position."""
    # If max_value is not specified, use the maximum of the two values plus 20%
    if max_value is None:
        max_value = max(italy_value, eu_value) * 1.2
    
    # Create a nested axes for the bar chart
    chart_ax = plt.axes([x_position, y_position, width, height], frameon=True)
    chart_ax.set_facecolor('white')
    chart_ax.set_title(title, fontsize=9)
    
    # Create bars
    bar_width = 0.35
    positions = [0, 1]
    chart_ax.bar(positions[0], italy_value, bar_width, color='green', label='Italy')
    chart_ax.bar(positions[1], eu_value, bar_width, color='red', label='EU')
    
    # Set labels and limits
    chart_ax.set_xticks(positions)
    chart_ax.set_xticklabels(['I', 'EU'], fontsize=8)
    chart_ax.set_ylim(0, max_value)
    chart_ax.tick_params(axis='y', labelsize=8)
    
    # Add values on top of bars
    chart_ax.text(positions[0], italy_value + max_value*0.02, f"{italy_value:.1f}", 
                  ha='center', va='bottom', fontsize=7)
    chart_ax.text(positions[1], eu_value + max_value*0.02, f"{eu_value:.1f}", 
                  ha='center', va='bottom', fontsize=7)
    
    # Remove top and right spines
    chart_ax.spines['top'].set_visible(False)
    chart_ax.spines['right'].set_visible(False)
    
    return chart_ax

def draw_connection(ax, x1, y1, x2, y2, label=None, label_pos=0.5, connection_style="arc3,rad=0.0"):
    """Draw a connection between two points with an optional label."""
    connection = ConnectionPatch(
        xyA=(x1, y1), xyB=(x2, y2),
        coordsA="data", coordsB="data",
        axesA=ax, axesB=ax,
        arrowstyle="-|>", color="black",
        lw=1.5, 
        connectionstyle=connection_style
    )
    ax.add_artist(connection)
    
    if label is not None:
        # Calculate position for label
        x_pos = x1 + (x2 - x1) * label_pos
        y_pos = y1 + (y2 - y1) * label_pos
        
        # Draw text with white background for readability
        ax.text(x_pos, y_pos, label, 
                ha='center', va='center', 
                fontsize=9, fontweight='bold',
                bbox=dict(facecolor='white', edgecolor='none', pad=1, alpha=0.8))

def create_driver_tree_visualization():
    """Create a driver tree visualization based on the handwritten sketch."""
    print("Creating driver tree visualization...")
    
    # Parse data from CSV
    italy_data, eu_data = parse_csv_data()
    
    # Create figure with blue grid paper background (like the sketch)
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#e6f2ff')
    ax.set_facecolor('#e6f2ff')
    
    # Add grid lines
    ax.grid(True, linestyle='-', alpha=0.3, color='blue', linewidth=0.5)
    
    # Set axis limits and remove ticks
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add SDA Bocconi logo text (as in the sketch)
    plt.figtext(0.05, 0.95, "SDA\nBocconi", 
               fontsize=12, fontweight='bold', va='top', ha='left',
               bbox=dict(facecolor='none', edgecolor='none', pad=0))
    plt.figtext(0.05, 0.90, "SCHOOL OF MANAGEMENT", 
               fontsize=6, va='top', ha='left')
    
    # Draw the main driver tree structure
    # 1. Start with Actual Individual Consumption
    ax.text(0.18, 0.85, "ACTUAL INDIVIDUAL\nCONSUMPTION", fontsize=10, ha='center', va='center')
    
    # AIC/GDP - Left branch
    # 2. Connection to AIC/GDP
    draw_connection(ax, 0.18, 0.8, 0.18, 0.7, connection_style="arc3,rad=0.0")
    ax.text(0.18, 0.65, "AIC\n––––\nGDP", fontsize=10, ha='center', va='center')
    
    # 3. GDP explanation
    ax.text(0.18, 0.55, "GROSS DOMESTIC\nPRODUCT", fontsize=10, ha='center', va='center')
    
    # 1. AIC/GDP chart 
    create_bar_chart(ax, 0.87, 0.65, 0.2, 0.15, 
                    "AIC/GDP", 
                    italy_data['AIC ON GPD'], 
                    eu_data['AIC ON GPD'])
    
    # Right branches - horizontal connections
    # 4. Horizontal connection from AIC to AIC/CAD
    draw_connection(ax, 0.22, 0.85, 0.35, 0.85, connection_style="arc3,rad=0.0")
    
    # 5. AIC/CAD ratio and description
    ax.text(0.45, 0.85, "AIC\n––––\nCAD", fontsize=10, ha='center', va='center')
    ax.text(0.55, 0.85, "CURRENCY\nAND DEPOSITS", fontsize=9, ha='left', va='center')
    
    # 2. AIC/CAD chart - Position to right of ratio 
    create_bar_chart(ax, 0.65, 0.85, 0.2, 0.15, 
                    "AIC/CAD", 
                    italy_data['AIC ON CAD'], 
                    eu_data['AIC ON CAD'])
    
    # 6. CAD/INS ratio and connection
    draw_connection(ax, 0.22, 0.65, 0.35, 0.65, connection_style="arc3,rad=0.0")
    ax.text(0.45, 0.65, "CAD\n––––\nINS", fontsize=10, ha='center', va='center')
    ax.text(0.55, 0.65, "INSURANCE, PENSIONS,\nGUARANTEES", fontsize=9, ha='left', va='center')
    
    # 3. CAD/INS chart - Position to right of ratio
    create_bar_chart(ax, 0.65, 0.65, 0.2, 0.15, 
                    "CAD/INS", 
                    italy_data['CAD on INS'], 
                    eu_data['CAD on INS'])
    
    # 7. INS/FA ratio and connection
    draw_connection(ax, 0.22, 0.45, 0.35, 0.45, connection_style="arc3,rad=0.0")
    ax.text(0.45, 0.45, "INS\n––––\nFA", fontsize=10, ha='center', va='center')
    ax.text(0.55, 0.45, "FINANCIAL\nASSETS", fontsize=9, ha='left', va='center')
    
    # 4. INS/FA chart - Position to right of ratio
    create_bar_chart(ax, 0.65, 0.45, 0.2, 0.15, 
                    "INS/FA", 
                    italy_data['Ins on FA'], 
                    eu_data['Ins on FA'])
    
    # 8. FA/GDP ratio and connection
    draw_connection(ax, 0.22, 0.25, 0.35, 0.25, connection_style="arc3,rad=0.0")
    ax.text(0.45, 0.25, "FA\n––––\nGDP", fontsize=10, ha='center', va='center')
    
    # 5. FA/GDP chart - Position to right of ratio
    create_bar_chart(ax, 0.65, 0.25, 0.2, 0.15, 
                    "FA/GDP", 
                    italy_data['FA ON GDP'], 
                    eu_data['FA ON GDP'])
    
    # Add legend with correct colors (Italy - Green, EU - Red)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', edgecolor='green', label='Italy'),
        Patch(facecolor='red', edgecolor='red', label='EU')
    ]
    ax.legend(handles=legend_elements, loc='upper right', frameon=True, 
              facecolor='white', edgecolor='black', fontsize=9)
    
    # Add key insights about the €1.5 trillion paradox
    insights_box = plt.text(0.18, 0.15, 
                "Key Insights:\n\n" + 
                "• Italians hold 50% more cash vs insurance\n" +
                "  compared to EU average (150% vs 116%)\n\n" +
                "• With 5% inflation, €1.5T in cash\n" +
                "  loses €75B in value annually",
                fontsize=9, ha='left', va='center',
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.8, pad=10))
    
    # Add small map of Italy icon
    ax.text(0.05, 0.15, "MAP", fontsize=8, ha='center')
    map_rect = Rectangle((0.03, 0.07), 0.04, 0.05, 
                       facecolor='none', edgecolor='black')
    ax.add_patch(map_rect)
    
    # Add title
    plt.suptitle("The €1.5 Trillion Paradox: Italian Household Financial Ratios", 
                fontsize=16, y=0.98)
    
    # Save the figure
    output_path = OUTPUT_DIR / "financial_driver_tree.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved driver tree visualization to {output_path}")
    
    # Create interactive version for web embedding
    plt.savefig(OUTPUT_DIR / "financial_driver_tree_transparent.png", 
               dpi=300, bbox_inches='tight', transparent=True)
    
    # Show it
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()
    
    print("Visualization created successfully!")

if __name__ == "__main__":
    create_driver_tree_visualization() 