# Smart File Organizer

A Python script that cleans up messy folders by automatically sorting files into categories. Built this because my Downloads folder was a disaster.

## What it does

Automatically organizes files by type (images, documents, videos, etc.) or by date. Also finds duplicate files using MD5 hashing so you don't waste space.

Main features:
- Sorts files into categories automatically
- Detects duplicates 
- Can organize by type, date, or both
- Dry-run mode to preview changes
- Handles filename conflicts

## Installation

Just Python 3.6+ needed. No pip installs or anything.

```bash
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer
python smart_file_organizer.py ~/Downloads
```

## Usage

Basic examples:

```bash
# organize your downloads folder
python smart_file_organizer.py ~/Downloads

# see what would happen without actually moving files
python smart_file_organizer.py ~/Downloads --dry-run

# organize by date instead of type
python smart_file_organizer.py ~/Desktop --organize-by date

# organize by both type AND date
python smart_file_organizer.py ~/Documents --organize-by both

# skip duplicate detection if you want it faster
python smart_file_organizer.py ~/Downloads --no-duplicates
```

## Supported file types

Images (jpg, png, gif, svg, webp), Videos (mp4, avi, mkv, mov), Documents (pdf, docx, txt, md), Spreadsheets (xlsx, csv), Presentations (pptx, key), Audio (mp3, wav, flac), Archives (zip, rar, 7z, tar), Code files (py, js, java, cpp, go), Web files (html, css, json), Executables (exe, dmg, deb), Fonts (ttf, otf, woff), eBooks (epub, mobi)

Anything else goes into "Others" folder.

## How it works

The script scans your target directory and categorizes each file based on extension. If you enable duplicate detection, it hashes each file and moves duplicates to a separate folder. Files are moved into organized subdirectories, and if there's a naming conflict it appends a number.

Example output:
```
Found 45 file(s) to process...

   ✓ Moved: vacation.jpg → Images
   ✓ Moved: report.pdf → Documents
   ⚠️  Duplicate detected: report_copy.pdf
   ✓ Moved: script.py → Code

Files organized: 42
Duplicates found: 3
```

## Testing

Run `create_demo.py` to generate test files, then try the organizer in dry-run mode:

```bash
python create_demo.py
python smart_file_organizer.py demo_files --dry-run
```

## License

MIT - you can do whatever you want with it
