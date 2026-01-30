# 🧬 Biomedical Papers Searcher

Specialized search system for biomedical scientific articles with support for multiple databases.

## 📋 Description

**Biomedical Papers Searcher** is a command-line tool that searches three of the world's leading biomedical databases:

- **PubMed (NCBI)**: 35+ million biomedical articles
- **bioRxiv**: Recent biomedical preprints
- **Europe PMC**: 42+ million European articles

The system searches articles by keywords, ranks results by relevance, and can export data in professional DOCX format.

## ✨ Features

- 🔍 Simultaneous search across 3 biomedical databases
- 📊 Article ranking by number of keyword matches
- 📄 Export to formatted Word document (.docx)
- 🎯 Search in title, abstract, MeSH terms, and full text
- ⏰ Date filtering (last N days)
- 🔗 Direct links to original articles
- 📈 Results statistics by source

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

### Basic search

```bash
python browse_papers.py --keywords "breast cancer" "immunotherapy" --days 30
```

### Search with DOCX export

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

## 📊 Output Format

### Console
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

## 🔧 Parameters

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

## 👨‍💻 Author

Níckolas Pippi - [ORCID: 0009-0008-3312-7645](https://orcid.org/0009-0008-3312-7645)

---

⭐ If this project was useful to you, consider giving it a star!
