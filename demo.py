#!/usr/bin/env python3
"""
Demo script to test the Smart File Organizer
Creates sample files and runs the organizer in dry-run mode
"""

import os
from pathlib import Path
import random

def create_demo_files():
    """Create sample files for testing"""
    demo_dir = Path("demo_files")
    demo_dir.mkdir(exist_ok=True)
    
    # Sample files with different extensions
    sample_files = [
        "vacation_photo.jpg",
        "family_pic.png",
        "report_2024.pdf",
        "meeting_notes.txt",
        "budget.xlsx",
        "presentation.pptx",
        "song.mp3",
        "movie.mp4",
        "script.py",
        "website.html",
        "data.json",
        "archive.zip",
        "installer.exe",
        "document.docx",
        "spreadsheet.csv",
    ]
    
    print("Creating demo files...")
    for filename in sample_files:
        filepath = demo_dir / filename
        # Create file with some content
        with open(filepath, 'w') as f:
            f.write(f"Sample content for {filename}\n" * random.randint(1, 10))
        print(f"  Created: {filename}")
    
    # Create a duplicate
    duplicate = demo_dir / "report_2024_copy.pdf"
    original = demo_dir / "report_2024.pdf"
    with open(duplicate, 'w') as f:
        with open(original, 'r') as orig:
            f.write(orig.read())
    print(f"  Created: report_2024_copy.pdf (duplicate)")
    
    print(f"\n✅ Created {len(sample_files) + 1} demo files in '{demo_dir}/'")
    print(f"\nNow run:")
    print(f"  python smart_file_organizer.py demo_files --dry-run")
    print(f"\nTo actually organize them:")
    print(f"  python smart_file_organizer.py demo_files")

if __name__ == '__main__':
    create_demo_files()