#!/usr/bin/env python3
"""
Smart File Organizer - Intelligent automation for organizing files
Automatically categorizes and moves files based on type, date, and patterns
Perfect for keeping Downloads, Desktop, or any folder clean and organized
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import argparse
import json
from collections import defaultdict


class SmartFileOrganizer:
    """Intelligently organize files with duplicate detection and smart categorization"""
    
    CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico', '.webp', '.heic'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.tex', '.md'],
        'Spreadsheets': ['.xlsx', '.xls', '.csv', '.ods', '.tsv'],
        'Presentations': ['.ppt', '.pptx', '.key', '.odp'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Code': ['.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs'],
        'Web': ['.html', '.css', '.scss', '.sass', '.json', '.xml', '.yml', '.yaml'],
        'Executables': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm'],
        'Fonts': ['.ttf', '.otf', '.woff', '.woff2', '.eot'],
        'Books': ['.epub', '.mobi', '.azw', '.azw3'],
    }
    
    def __init__(self, source_dir, organize_by='type', dry_run=False, detect_duplicates=True):
        """
        Initialize the organizer
        
        Args:
            source_dir: Directory to organize
            organize_by: 'type', 'date', or 'both'
            dry_run: If True, only show what would be done
            detect_duplicates: If True, detect and handle duplicate files
        """
        self.source_dir = Path(source_dir).resolve()
        self.organize_by = organize_by
        self.dry_run = dry_run
        self.detect_duplicates = detect_duplicates
        self.stats = defaultdict(int)
        self.file_hashes = {}
        
    def get_file_hash(self, filepath, chunk_size=8192):
        """Calculate MD5 hash of a file for duplicate detection"""
        md5 = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(chunk_size):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            print(f"⚠️  Error hashing {filepath}: {e}")
            return None
    
    def get_category(self, file_path):
        """Determine the category of a file based on its extension"""
        extension = file_path.suffix.lower()
        for category, extensions in self.CATEGORIES.items():
            if extension in extensions:
                return category
        return 'Others'
    
    def get_destination_path(self, file_path):
        """Determine where a file should be moved"""
        category = self.get_category(file_path)
        
        if self.organize_by == 'type':
            dest_dir = self.source_dir / category
        elif self.organize_by == 'date':
            file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
            year_month = file_date.strftime('%Y-%m')
            dest_dir = self.source_dir / 'Organized_by_Date' / year_month / category
        else:  # both
            file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
            year_month = file_date.strftime('%Y-%m')
            dest_dir = self.source_dir / category / year_month
        
        return dest_dir
    
    def handle_duplicate(self, file_path, file_hash):
        """Handle duplicate file detection"""
        if file_hash in self.file_hashes:
            original = self.file_hashes[file_hash]
            duplicates_dir = self.source_dir / 'Duplicates'
            duplicates_dir.mkdir(exist_ok=True)
            return duplicates_dir, True
        else:
            self.file_hashes[file_hash] = file_path
            return None, False
    
    def move_file(self, file_path, dest_dir):
        """Move a file to the destination directory"""
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / file_path.name
        
        # Handle filename conflicts
        counter = 1
        while dest_path.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            dest_path = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        if self.dry_run:
            print(f"   Would move: {file_path.name} → {dest_dir.relative_to(self.source_dir)}")
        else:
            shutil.move(str(file_path), str(dest_path))
            print(f"   ✓ Moved: {file_path.name} → {dest_dir.relative_to(self.source_dir)}")
        
        return dest_path
    
    def organize(self):
        """Main organization logic"""
        if not self.source_dir.exists():
            print(f"❌ Error: Directory '{self.source_dir}' does not exist!")
            return
        
        print(f"\n{'='*70}")
        print(f"🗂️  Smart File Organizer")
        print(f"{'='*70}")
        print(f"Source: {self.source_dir}")
        print(f"Mode: Organize by {self.organize_by}")
        print(f"Duplicate Detection: {'ON' if self.detect_duplicates else 'OFF'}")
        print(f"Dry Run: {'YES' if self.dry_run else 'NO'}")
        print(f"{'='*70}\n")
        
        # Get all files (excluding directories we might create)
        excluded_dirs = {'Images', 'Videos', 'Documents', 'Archives', 'Code', 
                        'Audio', 'Spreadsheets', 'Presentations', 'Web', 
                        'Executables', 'Others', 'Duplicates', 'Fonts', 'Books',
                        'Organized_by_Date'}
        
        files = [
            f for f in self.source_dir.iterdir() 
            if f.is_file() and f.parent.name not in excluded_dirs
        ]
        
        if not files:
            print("📭 No files to organize!")
            return
        
        print(f"Found {len(files)} file(s) to process...\n")
        
        for file_path in files:
            try:
                # Skip hidden files
                if file_path.name.startswith('.'):
                    continue
                
                # Duplicate detection
                is_duplicate = False
                if self.detect_duplicates:
                    file_hash = self.get_file_hash(file_path)
                    if file_hash:
                        dup_dir, is_duplicate = self.handle_duplicate(file_path, file_hash)
                        if is_duplicate:
                            print(f"⚠️  Duplicate detected: {file_path.name}")
                            self.move_file(file_path, dup_dir)
                            self.stats['duplicates'] += 1
                            continue
                
                # Regular organization
                dest_dir = self.get_destination_path(file_path)
                self.move_file(file_path, dest_dir)
                self.stats['organized'] += 1
                
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
                self.stats['errors'] += 1
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print organization summary"""
        print(f"\n{'='*70}")
        print(f"📊 Summary")
        print(f"{'='*70}")
        print(f"Files organized: {self.stats['organized']}")
        if self.detect_duplicates:
            print(f"Duplicates found: {self.stats['duplicates']}")
        if self.stats['errors']:
            print(f"Errors: {self.stats['errors']}")
        print(f"{'='*70}\n")
        
        if self.dry_run:
            print("ℹ️  This was a DRY RUN - no files were actually moved")
            print("   Run without --dry-run to apply changes\n")


def main():
    parser = argparse.ArgumentParser(
        description='Smart File Organizer - Intelligently organize your messy directories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Organize Downloads folder by file type
  python smart_file_organizer.py ~/Downloads
  
  # Organize by date, with dry run
  python smart_file_organizer.py ~/Desktop --organize-by date --dry-run
  
  # Organize by both type and date
  python smart_file_organizer.py ~/Documents --organize-by both
  
  # Disable duplicate detection
  python smart_file_organizer.py ~/Downloads --no-duplicates
        """
    )
    
    parser.add_argument(
        'directory',
        help='Directory to organize'
    )
    
    parser.add_argument(
        '--organize-by',
        choices=['type', 'date', 'both'],
        default='type',
        help='Organization method (default: type)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    parser.add_argument(
        '--no-duplicates',
        action='store_true',
        help='Disable duplicate detection'
    )
    
    args = parser.parse_args()
    
    organizer = SmartFileOrganizer(
        source_dir=args.directory,
        organize_by=args.organize_by,
        dry_run=args.dry_run,
        detect_duplicates=not args.no_duplicates
    )
    
    organizer.organize()


if __name__ == '__main__':
    main()