# 🧬 Biomedical Papers Searcher

Specialized search system for biomedical scientific articles with support for multiple databases and a modern dark mode graphical interface.

## 📋 Description

**Biomedical Papers Searcher** is a powerful tool that searches three of the world's leading biomedical databases:

- **PubMed (NCBI)**: 35+ million biomedical articles
- **bioRxiv**: Recent biomedical preprints
- **Europe PMC**: 42+ million European articles

The system searches articles by keywords, ranks results by relevance, and can export data in professional DOCX format. Available in both command-line and modern dark mode graphical interface versions.

## ✨ Features

- 🔍 Simultaneous search across 3 biomedical databases
- 📊 Article ranking by number of keyword matches
- 📄 Export to formatted Word document (.docx)
- 🎯 Search in title, abstract, MeSH terms, and full text
- ⏰ Flexible date filtering (days, years, or specific year ranges)
- 🔗 Direct links to original articles
- 📈 Results statistics by source
- 🎨 **Modern dark mode interface** with responsive design
- 💻 **Fully responsive layout** - adapts from 650px to fullscreen

## 🛠️ Requirements

- Python 3.7 or higher
- Internet connection

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/nickpippi/biomedical-papers-searcher.git
cd biomedical-papers-searcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Graphical Interface (Recommended)

Simply run the GUI application:

```bash
python browse_papers_gui.py
```

**GUI Features:**
- ✨ Modern dark mode design with cyan accents
- 📐 Responsive layout (800px default, expands to fullscreen)
- 📅 Three time range options:
  - **Last N Days**: Quick selection (7, 14, 30, 60, 90, 180, 365 days) or custom
  - **Years Back**: Search 1-30 years back
  - **Specific Year Range**: Select start and end years (last 30 years available)
- 💾 Optional DOCX export with folder selection
- 📊 Real-time progress monitoring with animated progress bar
- 🖥️ Terminal-style results display with syntax highlighting
- 🖱️ Mouse wheel scroll support

**Interface Colors:**
- Background: Dark blue (#1a1a2e)
- Cards: Navy blue (#0f3460)
- Accent: Cyan (#00adb5)
- Success: Neon green (#06ffa5)
- Danger: Pink (#ff006e)
- Terminal: Matrix green (#00ff88)

### Command Line Interface

For automated scripts or power users:

#### Basic search

```bash
python browse_papers.py --keywords "breast cancer" "immunotherapy" --days 30
```

#### Search with DOCX export

```bash
python browse_papers.py --keywords "oncogene" "mutation" "p53" --days 14 --export /path/to/folder
```

### Practical examples

**Breast cancer research:**
```bash
python browse_papers.py --keywords "breast cancer" "treatment" --days 30
```

**Oncology and genetics:**
```bash
python browse_papers.py --keywords "oncogene" "mutation" "p53" --days 14
```

**Chemotherapy:**
```bash
python browse_papers.py --keywords "chemotherapy" "tolerance" "side effects" --days 7 --export ./results
```

**Last 5 years research (CLI):**
```bash
python browse_papers.py --keywords "immunotherapy" --days 1825
```

## 📊 Output Format

### Graphical Interface
Results are displayed in a modern dark terminal-style window with:
- Animated progress bar during search
- Color-coded status messages with prefixes: `[+]`, `[-]`, `[*]`, `[!]`
- Organized results by relevance
- Summary statistics
- Responsive layout that adapts to window size

### Console (CLI)
Results are displayed in the terminal organized by relevance (number of matches), showing:
- Article title
- Authors (first 3)
- Publication date
- Source (PubMed, bioRxiv, or Europe PMC)
- Matched keywords
- Abstract
- Article link

### DOCX Document (optional)
Generates a professional Word document containing:
- Header with search parameters
- General statistics
- Articles grouped by relevance
- Formatting with colors and hyperlinks
- Export timestamp

## 🔧 Parameters (CLI)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--keywords` | Yes | List of keywords to search |
| `--days` | Yes | Number of days to look back |
| `--export` | No | Folder path to export DOCX |

## 📚 Databases

### PubMed (NCBI)
- **Coverage**: Medicine, Biology, Public Health, Oncology
- **Search fields**: Title, Abstract, MeSH Terms, Keywords
- **Volume**: 35+ million articles

### bioRxiv
- **Coverage**: Molecular Biology, Genetics, Neuroscience, Cancer
- **Search fields**: Title, Abstract, Full Text
- **Type**: Preprints (non-peer-reviewed articles)

### Europe PMC
- **Coverage**: Life Sciences in general
- **Search fields**: Title, Abstract, Full Text, Grants
- **Volume**: 42+ million articles

## 🎨 GUI Screenshots

The modern dark mode interface features:
- Sleek dark blue background with cyan accents
- Card-based layout for easy navigation
- Three flexible date selection modes
- Real-time animated progress indicator
- Matrix-style terminal display for results
- Fully responsive design (expands from 650px to fullscreen)
- Modern Segoe UI font throughout

## 🖥️ Creating an Executable

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable (Windows - no console)
pyinstaller --onefile --windowed --name="BiomedicalPapersSearcher" browse_papers_gui.py

# Create executable (with console for debugging)
pyinstaller --onefile --name="BiomedicalPapersSearcher" browse_papers_gui.py
```

The executable will be in the `dist/` folder.

See `EXECUTABLE_GUIDE.md` for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ⚠️ Warnings

- Respect API rate limits
- PubMed allows maximum 3 requests per second
- Use the system responsibly and ethically
- Some articles may require subscription for full access

## 🐛 Known Issues

If you encounter any problems, please open an [issue](https://github.com/nickpippi/biomedical-papers-searcher/issues).

## 🆕 Recent Updates

### v2.1 - Dark Mode & Responsive Design (Current)
- Implemented beautiful dark mode interface
- Fixed layout to be fully responsive (adapts to any window size)
- Improved fonts with Segoe UI for better readability
- Removed emoji dependency for universal compatibility
- Added mouse wheel scroll support
- Optimized card-based layout
- Enhanced terminal-style results display

### v2.0 - Modern GUI
- Added graphical interface
- Enhanced date range selection with multiple modes
- Improved user experience with real-time feedback
- Maintained full backward compatibility with CLI

## 👨‍💻 Author

Níckolas Pippi - [ORCID: 0009-0008-3312-7645](https://orcid.org/0009-0008-3312-7645)

---

⭐ If this project was useful to you, consider giving it a star!
