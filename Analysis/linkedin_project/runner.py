#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Project Runner - The €1.5 Trillion Paradox
---------------------------------------------------
This script serves as the central entry point for the LinkedIn content project
on Italian household finances.

Created by: Davide Consiglio
Date: April 2025
"""

import os
import sys
import importlib.util
from pathlib import Path

# Project Constants
PROJECT_ROOT = Path(__file__).parent
TITLE = "The €1.5 Trillion Paradox: Italian Household Finances"
PUBLICATION_DATE = "April 29, 2025, 10:00 CET"

# Project Briefing
PROJECT_BRIEFING = """
BRIEFING: LinkedIn Post - The €1.5 trillion euros paradox of Italian households

GOAL:
Draft a LinkedIn post titled "The 1.5 trillion euros paradox of Italian households," 
with a structured narrative focused on situation, complication, solution, and impact, 
while maintaining a thought leader tone.

KEY POINTS:
1. Italian households hold more than €1.5 trillion in cash deposits, representing a 
   significant portion of their financial assets.
2. Compared to other EU countries, Italy shows a disproportionately high ratio of 
   currency and deposits to insurance products.
3. Current inflation (>5% in recent years) erodes the real value of these liquid assets over time.
4. Advanced data analytics can help the insurance industry better understand household needs 
   across their lifecycle.

DELIVERABLES:
1. A LinkedIn post with visual charts supporting the key points
2. Data analysis to support the narrative
3. A social media publication plan for April 29th, 2025 at 10:00 AM CET
"""

def show_menu():
    """Display the main menu of the project."""
    print("\n" + "=" * 80)
    print(f"LinkedIn Project: {TITLE}")
    print("=" * 80)
    print(PROJECT_BRIEFING)
    print("\n" + "=" * 80)
    print("OPTIONS:")
    print("1. Run data analysis and generate charts")
    print("2. View LinkedIn post drafts")
    print("3. View social media plan")
    print("4. Show project structure")
    print("5. View project briefing")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-5): ")
    return choice

def run_data_analysis():
    """Run the household data analysis script."""
    try:
        # Dynamically import and run the analysis script
        analysis_path = PROJECT_ROOT / "src" / "analyze_household_data.py"
        spec = importlib.util.spec_from_file_location("analysis_module", analysis_path)
        analysis_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analysis_module)
        analysis_module.main()
        print("\nData analysis completed successfully.")
    except Exception as e:
        print(f"\nError running data analysis: {e}")

def view_linkedin_posts():
    """Display the LinkedIn post drafts."""
    try:
        posts = {
            "1": PROJECT_ROOT / "docs" / "linkedin_post_draft.md",
            "2": PROJECT_ROOT / "docs" / "linkedin_post_concise.md"
        }
        
        print("\nAvailable LinkedIn post drafts:")
        print("1. Detailed draft")
        print("2. Concise version")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice in posts:
            with open(posts[choice], 'r', encoding='utf-8') as f:
                print("\n" + "=" * 80)
                print(f.read())
                print("=" * 80)
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"\nError viewing LinkedIn posts: {e}")

def view_social_media_plan():
    """Display the social media publication plan."""
    try:
        plan_path = PROJECT_ROOT / "docs" / "linkedin_post_plan.md"
        with open(plan_path, 'r', encoding='utf-8') as f:
            print("\n" + "=" * 80)
            print(f.read())
            print("=" * 80)
    except Exception as e:
        print(f"\nError viewing social media plan: {e}")

def show_project_structure():
    """Display the project structure."""
    try:
        print("\nProject Structure:")
        for root, dirs, files in os.walk(PROJECT_ROOT):
            level = root.replace(str(PROJECT_ROOT), '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")
    except Exception as e:
        print(f"\nError showing project structure: {e}")

def main():
    """Main function to run the project."""
    while True:
        choice = show_menu()
        
        if choice == '0':
            print("\nExiting the LinkedIn Project Runner. Goodbye!")
            sys.exit(0)
        elif choice == '1':
            run_data_analysis()
        elif choice == '2':
            view_linkedin_posts()
        elif choice == '3':
            view_social_media_plan()
        elif choice == '4':
            show_project_structure()
        elif choice == '5':
            print("\n" + "=" * 80)
            print(PROJECT_BRIEFING)
            print("=" * 80)
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 