#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Project Runner - Content Manager
----------------------------------------
This script serves as the central entry point for the LinkedIn content projects.

Created by: Davide Consiglio
Date: April 2025
"""

import os
import sys
import importlib.util
from pathlib import Path
import webbrowser

# Project Constants
PROJECT_ROOT = Path(__file__).parent
TITLE = "LinkedIn Content Manager"
CURRENT_POST = "The €1.5 Trillion Paradox: Italian Household Finances"
PUBLICATION_DATE = "April 29, 2025, 10:00 CET"

# Project Briefing
PROJECT_BRIEFING = """
LINKEDIN CONTENT STRATEGY

GOAL:
Strengthen position as thought leader in applied AI for financial services
through structured, data-driven LinkedIn posts.

TARGET AUDIENCE:
Executives and headhunters in financial services industry

POST FREQUENCY:
Biweekly posts on Monday mornings (8:30-9:30 AM CET)

CONTENT THEMES:
1. AI ethics and governance
2. Business transformation through AI
3. Technical innovation with practical applications
4. Leadership vision and strategic thinking
5. Team development and talent acquisition

KEY METRICS:
- Average engagement target: 600+ likes per post
- Impressions target: 12,000+ per post
- Conversion: Profile visits and connections from target audience
"""

def show_menu():
    """Display the main menu of the project."""
    print("\n" + "=" * 80)
    print(f"LinkedIn Project: {TITLE}")
    print("=" * 80)
    print(PROJECT_BRIEFING)
    print("\n" + "=" * 80)
    print("OPTIONS:")
    print("1. View LinkedIn content calendar")
    print("2. View/edit posts")
    print("3. Run post-specific scripts")
    print("4. Show project structure")
    print("5. View project briefing")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-5): ")
    return choice

def view_content_calendar():
    """Display the LinkedIn content calendar."""
    try:
        calendar_path = PROJECT_ROOT / "linkedin_posts_calendar.md"
        
        with open(calendar_path, 'r', encoding='utf-8') as f:
            print("\n" + "=" * 80)
            print(f.read())
            print("=" * 80)
    except Exception as e:
        print(f"\nError viewing content calendar: {e}")

def view_or_edit_posts():
    """Navigate and manage posts."""
    try:
        posts_path = PROJECT_ROOT / "posts"
        posts = [p for p in os.listdir(posts_path) if os.path.isdir(posts_path / p)]
        
        print("\nAvailable posts:")
        for i, post in enumerate(posts, 1):
            # Get the post status from its README.md
            readme_path = posts_path / post / "README.md"
            status = "Unknown"
            if os.path.exists(readme_path):
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "**Status**:" in content:
                        status = content.split("**Status**:")[1].split("\n")[0].strip()
            
            print(f"{i}. {post} ({status})")
        
        print("\nOptions:")
        print("1. Open post folder")
        print("2. View post drafts")
        print("3. View post publication plan")
        print("4. Run post data analysis")
        print("0. Back to main menu")
        
        choice = input("\nEnter your choice (0-4): ")
        
        if choice == "0":
            return
        elif choice == "1":
            open_post_folder(posts_path, posts)
        elif choice == "2":
            view_post_drafts(posts_path, posts)
        elif choice == "3":
            view_post_plan(posts_path, posts)
        elif choice == "4":
            run_post_analysis(posts_path, posts)
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"\nError managing posts: {e}")

def open_post_folder(posts_path, posts):
    """Open a post folder in the file explorer."""
    try:
        choice = input(f"\nSelect post number (1-{len(posts)}): ")
        
        try:
            post_idx = int(choice) - 1
            if 0 <= post_idx < len(posts):
                selected_post = posts[post_idx]
                post_path = (posts_path / selected_post).resolve()
                
                # Open file explorer to the selected post directory
                if sys.platform == 'darwin':  # macOS
                    os.system(f"open {post_path}")
                elif sys.platform == 'win32':  # Windows
                    os.system(f"explorer {post_path}")
                else:  # Linux
                    os.system(f"xdg-open {post_path}")
                
                print(f"\nOpened {selected_post} folder.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    except Exception as e:
        print(f"\nError opening post folder: {e}")

def view_post_drafts(posts_path, posts):
    """View drafts for a selected post."""
    try:
        choice = input(f"\nSelect post number (1-{len(posts)}): ")
        
        try:
            post_idx = int(choice) - 1
            if 0 <= post_idx < len(posts):
                selected_post = posts[post_idx]
                post_docs_path = posts_path / selected_post / "docs"
                
                # Get available draft files
                drafts = []
                if os.path.exists(post_docs_path):
                    for file in os.listdir(post_docs_path):
                        if file.endswith(".md") and "post" in file:
                            drafts.append(file)
                
                if drafts:
                    print("\nAvailable drafts:")
                    for i, draft in enumerate(drafts, 1):
                        print(f"{i}. {draft}")
                    
                    draft_choice = input(f"\nSelect draft number (1-{len(drafts)}): ")
                    try:
                        draft_idx = int(draft_choice) - 1
                        if 0 <= draft_idx < len(drafts):
                            draft_path = post_docs_path / drafts[draft_idx]
                            with open(draft_path, 'r', encoding='utf-8') as f:
                                print("\n" + "=" * 80)
                                print(f.read())
                                print("=" * 80)
                        else:
                            print("Invalid choice.")
                    except ValueError:
                        print("Please enter a number.")
                else:
                    print("\nNo drafts found for this post.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    except Exception as e:
        print(f"\nError viewing post drafts: {e}")

def view_post_plan(posts_path, posts):
    """View publication plan for a selected post."""
    try:
        choice = input(f"\nSelect post number (1-{len(posts)}): ")
        
        try:
            post_idx = int(choice) - 1
            if 0 <= post_idx < len(posts):
                selected_post = posts[post_idx]
                plan_path = posts_path / selected_post / "docs" / "linkedin_post_plan.md"
                
                if os.path.exists(plan_path):
                    with open(plan_path, 'r', encoding='utf-8') as f:
                        print("\n" + "=" * 80)
                        print(f.read())
                        print("=" * 80)
                else:
                    print("\nNo publication plan found for this post.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    except Exception as e:
        print(f"\nError viewing post plan: {e}")

def run_post_analysis(posts_path, posts):
    """Run the data analysis script for a selected post."""
    try:
        choice = input(f"\nSelect post number (1-{len(posts)}): ")
        
        try:
            post_idx = int(choice) - 1
            if 0 <= post_idx < len(posts):
                selected_post = posts[post_idx]
                analysis_path = posts_path / selected_post / "src" / "analyze_household_data.py"
                
                if os.path.exists(analysis_path):
                    print(f"\nRunning analysis for {selected_post}...")
                    
                    # Dynamically import and run the analysis script
                    spec = importlib.util.spec_from_file_location("analysis_module", analysis_path)
                    analysis_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(analysis_module)
                    analysis_module.main()
                    
                    print("\nData analysis completed successfully.")
                else:
                    print("\nNo analysis script found for this post.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    except Exception as e:
        print(f"\nError running post analysis: {e}")

def run_post_specific_scripts():
    """Run scripts for specific posts."""
    try:
        posts_path = PROJECT_ROOT / "posts"
        posts = [p for p in os.listdir(posts_path) if os.path.isdir(posts_path / p)]
        
        print("\nSelect a post to run scripts for:")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post}")
        
        choice = input(f"\nSelect post number (1-{len(posts)}): ")
        
        try:
            post_idx = int(choice) - 1
            if 0 <= post_idx < len(posts):
                selected_post = posts[post_idx]
                src_path = posts_path / selected_post / "src"
                
                if os.path.exists(src_path):
                    scripts = [f for f in os.listdir(src_path) if f.endswith(".py")]
                    
                    if scripts:
                        print(f"\nAvailable scripts for {selected_post}:")
                        for i, script in enumerate(scripts, 1):
                            print(f"{i}. {script}")
                        
                        script_choice = input(f"\nSelect script number (1-{len(scripts)}): ")
                        try:
                            script_idx = int(script_choice) - 1
                            if 0 <= script_idx < len(scripts):
                                selected_script = scripts[script_idx]
                                script_path = src_path / selected_script
                                
                                print(f"\nRunning {selected_script}...")
                                
                                # Dynamically import and run the script
                                spec = importlib.util.spec_from_file_location("script_module", script_path)
                                script_module = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(script_module)
                                
                                if hasattr(script_module, "main"):
                                    script_module.main()
                                
                                print(f"\n{selected_script} execution completed.")
                            else:
                                print("Invalid choice.")
                        except ValueError:
                            print("Please enter a number.")
                    else:
                        print(f"\nNo Python scripts found for {selected_post}.")
                else:
                    print(f"\nNo src directory found for {selected_post}.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a number.")
    except Exception as e:
        print(f"\nError running post scripts: {e}")

def show_project_structure():
    """Display the project structure."""
    try:
        print("\nProject Structure:")
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Skip the large directories
            if "__pycache__" in root or ".git" in root:
                continue
                
            level = root.replace(str(PROJECT_ROOT), '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            
            # Only show files at the top level or important files
            if level <= 1 or os.path.basename(root) in ["docs", "src", "data"]:
                for file in files:
                    if not file.startswith('.'):
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
            view_content_calendar()
        elif choice == '2':
            view_or_edit_posts()
        elif choice == '3':
            run_post_specific_scripts()
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