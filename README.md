# CV Generation Script

This repository contains Python scripts to generate CVs in both DOCX and PDF formats, as well as LaTeX and PDF formats. The scripts read data from a JSON file and create a general CV as well as specialized CVs for different fields such as software, embedded, digital, and web.

## Table of Contents

1. [Requirements](#requirements)
2. [Usage](#usage)
3. [File Structure](#file-structure)
4. [Customization](#customization)
5. [Contact](#contact)

## Requirements

### For DOCX and PDF Generation

- Python 3.x
- `python-docx` library
- `docx2pdf` library

You can install the required Python libraries using pip:

```sh
pip install python-docx docx2pdf
```

### For LaTeX and PDF Generation

- LaTeX distribution (e.g., TeX Live, MiKTeX) with `pdflatex`

## Usage

1. Ensure your data is correctly formatted in `data.json`.
2. Navigate to the appropriate folder before running the script.

### For DOCX and PDF Generation

Navigate to the `Word` folder and run:

```sh
cd Word
python generate_cvs.py
```

### For LaTeX and PDF Generation

Navigate to the `latex` folder and run:

```sh
cd latex
python generate_latex.py
```

The scripts will generate the following files:
- `Salah_CV.docx` and `Salah_CV.pdf` (General CV)
- `Salah_Software_CV.docx` and `Salah_Software_CV.pdf` (Software CV)
- `Salah_Embedded_CV.docx` and `Salah_Embedded_CV.pdf` (Embedded CV)
- `Salah_Digital_CV.docx` and `Salah_Digital_CV.pdf` (Digital CV)
- `Salah_Web_CV.docx` and `Salah_Web_CV.pdf` (Web CV)
- `Salah_Eldin_Hassen_CV.pdf` (General CV in PDF via LaTeX)
- Specialized LaTeX-based CVs (e.g., `Salah_Eldin_Hassen_Software_CV.pdf`)

## File Structure

- `Word/generate_cvs.py`: The main script for generating CVs in DOCX and PDF formats.
- `latex/generate_latex.py`: The script for generating CVs in LaTeX and PDF formats.
- `data.json`: The JSON file containing all the data for the CVs.
- `README.md`: This file.

## Customization

You can customize the content and style of the CVs by modifying the `data.json` file and the helper functions in `generate_cvs.py` and `generate_latex.py`.

### JSON Structure

The `data.json` file should follow this structure for DOCX and PDF generation:

```json
{
  "specialities": ["software", "embedded", "digital", "web"],
  "specialOrderProj": ["embedded", "software", "digital", "web"],
  "specialOrderCourse": ["embedded", "software", "digital"],
  "header": {
    "name": "Your Name",
    "contact": "your.email@example.com - City / Country - (+CountryCode) PhoneNumber",
    "links": "LinkedIn URL - GitHub URL"
  },
  "summary": ["Your summary here."],
  "education": ["Your education details here."],
  "work_experience": [
    {
      "header": "Job Title // Company // Employment Type // Date Range",
      "body": "Job description here."
    }
  ],
  "skills": {
    "software": ["Skill1", "Skill2"],
    "embedded": ["Skill1", "Skill2"],
    "digital": ["Skill1", "Skill2"],
    "web": ["Skill1", "Skill2"]
  },
  "tools": ["Tool1", "Tool2"],
  "projects": {
    "embedded": [
      {
        "title": "Project Title",
        "main": {
          "description": "Detailed project description.",
          "key_elements": ["Element1", "Element2"]
        },
        "shortend": {
          "description": "Short project description.",
          "key_elements": ["Element1", "Element2"]
        }
      }
    ]
  },
  "courses": {
    "embedded": [
      {
        "title": "Course Title",
        "main_description": ["Detailed course description."],
        "shortend_description": ["Short course description."]
      }
    ]
  },
  "competitions": "Your competitions and activities here."
}
```

For LaTeX and PDF generation, the `data.json` file should follow this structure:

```json
{
  "specialities": ["software", "digital", "embedded", "web"],
  "specialOrderFiles": ["embedded", "software", "digital"],
  "header": {
    "name": "Your Name",
    "contact": " (+CountryCode) PhoneNumber | City / Country ",
    "links": {
      "Email": "mailto:your.email@example.com",
      "LinkedIn Profile": "LinkedIn URL",
      "Github Profile": "GitHub URL"
    }
  },
  "education": [
    {
      "year": "Year Range",
      "title": "Degree // Institution",
      "details": ["Detail 1", "Detail 2"]
    }
  ],
  "work_experience": [
    {
      "date": "Date Range",
      "header": "Job Title // Company // Employment Type",
      "body": "Job description here."
    }
  ],
  "skills": {
    "Software": ["Skill1", "Skill2"]
  },
  "projects": {
    "embedded": [
      {
        "date": "Year",
        "title": "Project Title",
        "details": ["Detail 1", "Detail 2"],
        "for": ["Category1", "Category2"],
        "link": "Project Link"
      }
    ]
  },
  "other_projects": ["Project 1", "Project 2"],
  "courses": {
    "embedded": [
      {
        "date": "Year Range",
        "title": "Course Title // Instructor",
        "for": ["Category1", "Category2"],
        "description": ["Detail 1", "Detail 2"],
        "certificate": "Certificate Link"
      }
    ]
  },
  "other_courses": ["Course 1", "Course 2"],
  "extra": ["Activity 1", "Activity 2"]
}
```

## Contact

For any questions or feedback, please reach out via [GitHub](https://github.com/salah0eldin/) or [Linkedin](https://linkedin.com/in/salah-eldin-hassen-5bba10250/).
