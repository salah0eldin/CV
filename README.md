# CV Generation Script

This repository contains a Python script to generate CVs in both DOCX and PDF formats. The script reads data from a JSON file and creates a general CV as well as specialized CVs for different fields such as software, embedded, digital, and web.

## Table of Contents

1. [Requirements](#requirements)
2. [Usage](#usage)
3. [File Structure](#file-structure)
4. [Customization](#customization)
5. [Contact](#contact)

## Requirements

- Python 3.x
- `python-docx` library
- `docx2pdf` library

You can install the required libraries using pip:

```sh
pip install python-docx docx2pdf
```

## Usage

1. Ensure your data is correctly formatted in `data.json`.
2. Run the script to generate the CVs:

```sh
python generate_cvs.py
```

The script will generate the following files:
- `Salah_CV.docx` and `Salah_CV.pdf` (General CV)
- `Salah_Software_CV.docx` and `Salah_Software_CV.pdf` (Software CV)
- `Salah_Embedded_CV.docx` and `Salah_Embedded_CV.pdf` (Embedded CV)
- `Salah_Digital_CV.docx` and `Salah_Digital_CV.pdf` (Digital CV)
- `Salah_Web_CV.docx` and `Salah_Web_CV.pdf` (Web CV)

## File Structure

- `generate_cvs.py`: The main script for generating CVs.
- `data.json`: The JSON file containing all the data for the CVs.
- `README.md`: This file.

## Customization

You can customize the content and style of the CVs by modifying the `data.json` file and the helper functions in `generate_cvs.py`.

### JSON Structure

The `data.json` file should follow this structure:

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

## Contact

For any questions or feedback, please reach out via [GitHub](https://github.com/salah0eldin/) or [Linkedin](edin.com/in/salah-eldin-hassen-5bba10250/).

---
