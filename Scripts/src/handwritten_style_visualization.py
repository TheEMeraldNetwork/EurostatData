#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a handwritten-style visualization of financial ratios for Italian households
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patheffects as path_effects
from matplotlib import font_manager
import os
from pathlib import Path

# Add handwriting-like font
plt.rcParams['font.family'] = 'sans-serif'

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
# Use Master.csv from root directory
DATA_PATH = PROJECT_ROOT / "Master.csv"
# Create assets directory in the root if it doesn't exist
OUTPUT_DIR = PROJECT_ROOT / "assets" / "handwritten_style"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to make lines look hand-drawn
def make_wiggly_line(x1, y1, x2, y2, wiggles=10, amplitude=0.03):
    """Create a wiggly line that looks hand-drawn."""
    # Create base line
    length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    t = np.linspace(0, 1, 100)
    
    # Add slight random variations for hand-drawn effect
    random_variations = np.sin(t * wiggles * np.pi) * amplitude * length
    
    # Calculate line points with variations
    x = x1 + (x2-x1) * t
    y = y1 + (y2-y1) * t
    
    # Add perpendicular variations
    angle = np.arctan2(y2-y1, x2-x1) + np.pi/2
    x += np.cos(angle) * random_variations
    y += np.sin(angle) * random_variations
    
    return x, y

# Function to create hand-drawn text
def hand_drawn_text(ax, x, y, text, fontsize=12, color='black', ha='center', va='center'):
    """Create text that looks hand-drawn by adding a slight offset shadow."""
    txt = ax.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va,
                 fontweight='bold', zorder=10)
    
    # Add a slight path effect to simulate hand-drawn text
    txt.set_path_effects([
        path_effects.SimpleLineShadow(offset=(1, -1), alpha=0.3),
        path_effects.Normal()
    ])
    return txt

# Function to create a hand-drawn rectangle
def hand_drawn_rect(ax, x, y, width, height, **kwargs):
    """Create a rectangle that looks hand-drawn by adding wobbles to the edges."""
    
    # Create corner points with slight randomness
    corners = [
        (x, y),  # bottom left
        (x + width, y),  # bottom right
        (x + width, y + height),  # top right
        (x, y + height),  # top left
        (x, y)  # back to start
    ]
    
    # Create path points with wobbles
    path_points = []
    codes = []
    
    for i in range(len(corners)-1):
        x1, y1 = corners[i]
        x2, y2 = corners[i+1]
        
        # Create wiggly lines for each edge
        wiggle_x, wiggle_y = make_wiggly_line(x1, y1, x2, y2, wiggles=5, amplitude=0.01)
        
        if i == 0:
            codes.append(Path.MOVETO)
            path_points.append((wiggle_x[0], wiggle_y[0]))
        
        for j in range(1, len(wiggle_x)):
            codes.append(Path.LINETO)
            path_points.append((wiggle_x[j], wiggle_y[j]))
    
    # Create path
    path = Path(path_points, codes)
    patch = plt.PathPatch(path, **kwargs, linewidth=1.5, fill=False)
    
    ax.add_patch(patch)
    return patch

# Function to create a hand-drawn arrow
def hand_drawn_arrow(ax, x1, y1, x2, y2, **kwargs):
    """Create an arrow that looks hand-drawn."""
    # Create wiggly line for arrow shaft
    wiggle_x, wiggle_y = make_wiggly_line(x1, y1, x2, y2, wiggles=8, amplitude=0.01)
    
    # Draw the line
    line, = ax.plot(wiggle_x, wiggle_y, **kwargs, linewidth=1.5)
    
    # Add arrowhead
    arrow_head = FancyArrowPatch((wiggle_x[-2], wiggle_y[-2]), (wiggle_x[-1], wiggle_y[-1]),
                                 arrowstyle='-|>', mutation_scale=15, 
                                 color=kwargs.get('color', 'k'), linewidth=1.5)
    ax.add_patch(arrow_head)
    
    return line, arrow_head

# Function to create hand-drawn bar chart
def hand_drawn_bars(ax, x, heights, color=None, label=None, width=0.3):
    """Create bars that look hand-drawn."""
    bars = []
    
    for i, h in enumerate(heights):
        # Add slight variation to bar width and position
        bar_width = width * (0.95 + 0.1 * np.random.random())
        bar_x = x[i] - bar_width/2 + 0.02 * np.random.random()
        
        # Create the bar as a hand-drawn rectangle
        bar = hand_drawn_rect(ax, bar_x, 0, bar_width, h, color=color, alpha=0.7, label=label if i==0 else None)
        bars.append(bar)
        
        # Add slight text offset for hand-drawn look
        text_x = bar_x + bar_width/2
        text_y = h + 0.02
        text_offset_x = 0.01 * (np.random.random() - 0.5)
        text_offset_y = 0.01 * (np.random.random() - 0.5)
        
        hand_drawn_text(ax, text_x + text_offset_x, text_y + text_offset_y, 
                       f"{h:.1f}" if h < 10 else f"{int(h)}", fontsize=10)
    
    return bars

def create_financial_ratios_sketch():
    """Create a sketch-like visualization of financial ratios for Italy and EU."""
    # Print paths for debugging
    print(f"Looking for data file at: {DATA_PATH}")
    
    # Read and prepare data
    try:
        # Read directly from the file, manually parsing it
        with open(DATA_PATH, 'r') as f:
            lines = f.readlines()
            
        # Parse to find Italy and EU data
        italy_data = None
        eu_data = None
        
        for line in lines:
            if line.strip().startswith('Italy;'):
                parts = line.strip().split(';')
                italy_data = {
                    'Currency and deposits': parts[1].strip(),
                    'Insurance': parts[5].strip(),
                    'AIC ON GPD': parts[10].strip().replace('%', ''),
                    'AIC ON CAD': parts[11].strip().replace('%', ''),
                    'CAD on INS': parts[12].strip().replace('%', ''),
                    'Ins on FA': parts[13].strip().replace('%', ''),
                    'FA ON GDP': parts[14].strip()
                }
            elif line.strip().startswith('EU;'):
                parts = line.strip().split(';')
                eu_data = {
                    'Currency and deposits': parts[1].strip(),
                    'Insurance': parts[5].strip(),
                    'AIC ON GPD': parts[10].strip().replace('%', ''),
                    'AIC ON CAD': parts[11].strip().replace('%', ''),
                    'CAD on INS': parts[12].strip().replace('%', ''),
                    'Ins on FA': parts[13].strip().replace('%', ''),
                    'FA ON GDP': parts[14].strip()
                }
                
        if not italy_data or not eu_data:
            raise ValueError("Could not find Italy or EU data in the CSV file")
            
        # Convert string values to float
        for data in [italy_data, eu_data]:
            for key in data:
                try:
                    # Handle European number format: replace dot in thousands and comma decimal separator
                    value = data[key].replace('.', '').replace(',', '.')
                    data[key] = float(value)
                except:
                    print(f"Warning: Could not convert {key}={data[key]} to float")
                    data[key] = 0
                    
        # Create figure with grid background
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Set background to light blue grid paper
        ax.set_facecolor('#f0f5ff')
        
        # Add grid lines
        ax.grid(True, linestyle='-', alpha=0.3, color='blue', linewidth=0.5)
        
        # Main title
        hand_drawn_text(ax, 0.5, 0.95, 'The €1.5 Trillion Trap: Italian Household Financial Ratios', 
                      fontsize=18, ha='center', va='top')
        
        # Draw the sketch layout
        # Left side - Actual individual consumption
        hand_drawn_text(ax, 0.2, 0.8, 'Actual Individual', fontsize=14)
        hand_drawn_text(ax, 0.2, 0.77, 'Consumption', fontsize=14)
        
        # Line from AIC to AIC/GDP
        hand_drawn_arrow(ax, 0.2, 0.75, 0.2, 0.65, color='black')
        
        # AIC/GDP
        hand_drawn_text(ax, 0.2, 0.63, 'AIC', fontsize=14)
        wiggly_x, wiggly_y = make_wiggly_line(0.15, 0.6, 0.25, 0.6)
        ax.plot(wiggly_x, wiggly_y, 'k-', linewidth=2)
        hand_drawn_text(ax, 0.2, 0.57, 'GDP', fontsize=14)
        
        # GDP explanation
        hand_drawn_text(ax, 0.2, 0.5, 'Gross Domestic', fontsize=14)
        hand_drawn_text(ax, 0.2, 0.47, 'Product', fontsize=14)
        
        # Central branch
        hand_drawn_arrow(ax, 0.3, 0.7, 0.4, 0.7, color='black')
        
        # AIC/CAD
        hand_drawn_text(ax, 0.5, 0.83, 'AIC', fontsize=14)
        wiggly_x, wiggly_y = make_wiggly_line(0.45, 0.8, 0.55, 0.8)
        ax.plot(wiggly_x, wiggly_y, 'k-', linewidth=2)
        hand_drawn_text(ax, 0.5, 0.77, 'CAD', fontsize=14)
        
        # Currency and Deposits
        hand_drawn_text(ax, 0.56, 0.83, 'Currency', fontsize=12)
        hand_drawn_text(ax, 0.56, 0.8, 'and Deposits', fontsize=12)
        
        # First bar chart - AIC/CAD
        x_pos = [0.7, 0.8, 0.9, 1.0]  # Positions for Italy, EU
        bar_heights = [
            float(italy_data['AIC ON CAD']),
            float(eu_data['AIC ON CAD'])
        ]
        hand_drawn_bars(ax, x_pos[:2], bar_heights, color='green')
        
        # Labels for countries
        hand_drawn_text(ax, 0.7, -0.05, 'I', fontsize=12)
        hand_drawn_text(ax, 0.8, -0.05, 'EU', fontsize=12)
        
        # CAD/INS
        hand_drawn_arrow(ax, 0.3, 0.6, 0.4, 0.6, color='black')
        hand_drawn_text(ax, 0.5, 0.63, 'CAD', fontsize=14)
        wiggly_x, wiggly_y = make_wiggly_line(0.45, 0.6, 0.55, 0.6)
        ax.plot(wiggly_x, wiggly_y, 'k-', linewidth=2)
        hand_drawn_text(ax, 0.5, 0.57, 'INS', fontsize=14)
        
        # Insurance, Pensions
        hand_drawn_text(ax, 0.56, 0.6, 'Insurance, Pensions,', fontsize=12)
        hand_drawn_text(ax, 0.56, 0.57, 'Guarantees', fontsize=12)
        
        # Second bar chart - CAD/INS
        bar_heights = [
            float(italy_data['CAD on INS']),
            float(eu_data['CAD on INS'])
        ]
        hand_drawn_bars(ax, x_pos[:2], bar_heights, color='red')  # Changed to red to match instruction
        
        # INS/FA
        hand_drawn_arrow(ax, 0.3, 0.5, 0.4, 0.5, color='black')
        hand_drawn_text(ax, 0.5, 0.53, 'INS', fontsize=14)
        wiggly_x, wiggly_y = make_wiggly_line(0.45, 0.5, 0.55, 0.5)
        ax.plot(wiggly_x, wiggly_y, 'k-', linewidth=2)
        hand_drawn_text(ax, 0.5, 0.47, 'FA', fontsize=14)
        
        # Financial Assets
        hand_drawn_text(ax, 0.56, 0.5, 'Financial', fontsize=12)
        hand_drawn_text(ax, 0.56, 0.47, 'Assets', fontsize=12)
        
        # Third bar chart - INS/FA
        bar_heights = [
            float(italy_data['Ins on FA']),
            float(eu_data['Ins on FA'])
        ]
        hand_drawn_bars(ax, x_pos[:2], bar_heights, color='red')  # Changed to red to match instruction
        
        # FA/GDP
        hand_drawn_arrow(ax, 0.3, 0.4, 0.4, 0.4, color='black')
        hand_drawn_text(ax, 0.5, 0.43, 'FA', fontsize=14)
        wiggly_x, wiggly_y = make_wiggly_line(0.45, 0.4, 0.55, 0.4)
        ax.plot(wiggly_x, wiggly_y, 'k-', linewidth=2)
        hand_drawn_text(ax, 0.5, 0.37, 'GDP', fontsize=14)
        
        # Fourth bar chart - FA/GDP
        bar_heights = [
            float(italy_data['FA ON GDP']),
            float(eu_data['FA ON GDP'])
        ]
        hand_drawn_bars(ax, x_pos[:2], bar_heights, color='red')  # Changed to red to match instruction
        
        # Add a handwritten style logo at the bottom left
        hand_drawn_text(ax, 0.1, 0.05, 'Data Analysis by', fontsize=10)
        hand_drawn_text(ax, 0.1, 0.02, 'Davide Consiglio', fontsize=10)
        
        # Remove axis ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Add main insights
        hand_drawn_text(ax, 0.75, 0.25, "Key Insights:", fontsize=14, ha='left')
        hand_drawn_text(ax, 0.75, 0.21, "1. Italians hold 50% more cash vs insurance", fontsize=12, ha='left')
        hand_drawn_text(ax, 0.75, 0.18, "   compared to EU average", fontsize=12, ha='left')
        hand_drawn_text(ax, 0.75, 0.14, "2. With 5% inflation, €1.5T in cash", fontsize=12, ha='left')
        hand_drawn_text(ax, 0.75, 0.11, "   loses €75B in value annually", fontsize=12, ha='left')
        
        plt.tight_layout(pad=2.0)
        
        # Create templates directory if it doesn't exist
        templates_dir = PROJECT_ROOT / "templates" / "charts"
        os.makedirs(templates_dir, exist_ok=True)
        
        # Save the figure in multiple locations to ensure it's available
        output_path = OUTPUT_DIR / "financial_ratios_sketch.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Saved handwritten-style visualization to {output_path}")
        
        # Save for the LinkedIn post (as referenced in the post)
        linkedin_output_path = templates_dir / "inflation_impact.png"
        plt.savefig(linkedin_output_path, dpi=300, bbox_inches='tight')
        print(f"Saved for LinkedIn post at {linkedin_output_path}")
        
        # Save a version with transparent background for GitHub display
        output_path_transparent = OUTPUT_DIR / "financial_ratios_sketch_transparent.png"
        plt.savefig(output_path_transparent, dpi=300, bbox_inches='tight', transparent=True)
        print(f"Saved transparent version to {output_path_transparent}")
        
        plt.close()
        
    except Exception as e:
        print(f"Error creating visualization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_financial_ratios_sketch() 