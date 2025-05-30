import json
import subprocess
from time import sleep


LINE_TITLE_SPACE = 0.9
TITLE_SIZE = 14
AFTER_TITLE_SPACE = 0.2

# Load data from JSON file
def load_data(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Generate LaTeX file
def generate_latex(data, output_file):
    header = data.get("header", {})
    if not header:
        return

    name = header.get("name", "")
    contact = header.get("contact", "")
    links = header.get("links", {})

    with open(output_file, 'w') as file:
        # Set default font size to 11pt
        file.write("\\documentclass[11pt,a4paper]{article}\n")
        file.write("\\usepackage{geometry}\n")
        file.write("\\usepackage{hyperref}\n")
        file.write("\\usepackage{mathpazo}\n")  # Palatino font, a popular choice for CVs
        file.write("\\usepackage[scaled=0.92]{helvet}\n")  # Helvetica for sans-serif
        file.write("\\usepackage{courier}\n")  # Courier for monospace
        file.write("\\usepackage{amssymb}\n")  # Include the amssymb package to define \blacksquare
        file.write("\\usepackage{enumitem}\n")
        file.write("\\usepackage{setspace}\n")
        file.write("\\geometry{top=0.3in, bottom=0.3in, left=0.3in, right=0.3in}\n")
        file.write("\\hypersetup{colorlinks=true, linkcolor=black, urlcolor=blue}\n")
        # Reduce the space between lines globally
        file.write("\\linespread{0.8}\n")
        file.write("\\begin{document}\n")

        # =============================
        # Header Section
        # =============================
        if name and contact and links:
            file.write("\\begin{center}\n")
            file.write(f"\\fontsize{{22}}{{22}}\\textbf{{{name}}}\\\\[0.2cm]\n")
            contact_and_links = "\\fontsize{11}{12}\\textbf{" + \
                f"{contact} " + \
                " \\texttt{{|}} ".join([f"\\href{{{url}}}{{{label}}}" for label, url in links.items()]) + "}\\\\[-0.1cm]\n"
            file.write(contact_and_links)
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")
            file.write("\\end{center}\n")

        # Reduce gap between sections to the minimum
        file.write(f"\\vspace{{-{LINE_TITLE_SPACE}cm}}\n")

        # =============================
        # Education Section
        # =============================
        education = data.get("education", [])
        if education:
            file.write("\\begin{center}\n")
            file.write(f"\\section*{{\\fontsize{{{TITLE_SIZE}}}{{18}}\\textbf\\selectfont EDUCATION}}\n")
            file.write("\\end{center}\n")

            file.write(f"\\vspace{{-{AFTER_TITLE_SPACE}cm}}\n")

            # Adjust vertical alignment of circular bullet points
            file.write("\\renewcommand\\labelitemi{\\raisebox{0.2ex}{\\scriptsize$\\bullet$}}\n")

            for edu in education:
                year = edu.get("year", "")
                title = edu.get("title", "")
                details = edu.get("details", [])

                if year and title:
                    file.write("\\begin{flushleft}\n")
                    file.write(f"\\textbf{{{title}}}\hfill\\textit{{{year}}}\\\\\n")
                    file.write("\\end{flushleft}\n")

                    file.write("\\vspace{-0.6cm}\n")

                # Details as sub bullet points
                if details:
                    file.write("\\begin{itemize}\n")
                    for detail in details:
                        file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                    file.write("\\end{itemize}\n")

                file.write("\\vspace{-0.3cm}\n")
            file.write("\\vspace{-0.2cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

            file.write(f"\\vspace{{-{LINE_TITLE_SPACE}cm}}\n")

        # =============================
        # Work Experience Section
        # =============================
        work_experience = data.get("work_experience", [])
        if work_experience:
            file.write("\\begin{center}\n")
            file.write(f"\\section*{{\\fontsize{{{TITLE_SIZE}}}{{ 18 }}\\textbf\\selectfont WORK EXPERIENCE}}\n")
            file.write("\\end{center}\n")

            file.write(f"\\vspace{{-{AFTER_TITLE_SPACE}cm}}\n")

            for work in work_experience:
                date = work.get("date", "")
                header = work.get("header", "")
                body = work.get("body", "")

                if date and header:
                    file.write("\\begin{flushleft}\n")
                    file.write(f"\\textbf{{{header}}}\\hfill\\textit{{{date}}}\\\\\n")
                    file.write("\\end{flushleft}\n")

                    file.write("\\vspace{-0.6cm}\n")

                # Body as a paragraph
                if body:
                    file.write("\\begin{itemize}\n")
                    file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {body}\n")
                    file.write("\\end{itemize}\n")

                file.write("\\vspace{-0.5cm}\n")

            file.write("\\vspace{0.2cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

        # =============================
        # Skills Section
        # =============================
        skills = data.get("skills", {})
        if skills:
            file.write(f"\\vspace{{-{LINE_TITLE_SPACE}cm}}\n")
            file.write("\\begin{center}\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont SKILLS}\n")
            file.write("\\end{center}\n")

            file.write(f"\\vspace{{-{2*AFTER_TITLE_SPACE}cm}}\n")

            # Create the skills section in a table format with proper alignment and spacing
            file.write("\\renewcommand{\\arraystretch}{1.8} % Adjust row spacing\n")
            file.write("\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}} l l}\n")
            for category, skill_data in skills.items():
                skill_list = skill_data.get("data", [])
                if skill_list:
                    file.write(f"\\textbf{{{category}:}} & {' - '.join(skill_list)} \\\\ \n")
            file.write("\\end{tabular*}\n")
            file.write("\\vspace{0.2cm}\\rule{\\textwidth}{0.3pt}\n")

        i = 0
        # =============================
        # Projects Section
        # =============================
        projects = data.get("projects", {})
        if projects:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont PROJECTS}\n")

            file.write("\\vspace{-0.3cm}\n")

            for category, project_list in projects.items():
                for project in project_list:
                    date = project.get("date", "")
                    title = project.get("title", "")
                    details = project.get("details", [])
                    
                    i += 1
                    if i % 8 == 0:
                        file.write("\\newpage\n")

                    if date and title:
                        file.write("\\begin{flushleft}\n")
                        file.write(f"\\textbf{{{title}}}")
                        if(project.get("link", "")):
                            file.write(f"\\texttt{{|}} {{\\href{{{project.get('link', '')}}}{{Link}}}}")
                        file.write(f"\\hfill\\textit{{{date}}}\\\\\n")
                        file.write("\\end{flushleft}\n")

                        file.write("\\vspace{-0.7cm}\n")

                    if details:
                        file.write("\\begin{itemize}\n")
                        for detail in details:
                            file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                        file.write("\\end{itemize}\n")

                    file.write("\\vspace{-0.5cm}\n")
            file.write("\\vspace{-0.1cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")
        
        # =============================
        # Other Projects Section
        # =============================
        other_projects = data.get("other_projects", [])
        if other_projects:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont OTHER PROJECTS}\n")

            file.write("\\vspace{-0.3cm}\n")
            
            file.write("\\begin{itemize}[noitemsep, left=0pt, itemsep=5pt]\n")
            for other_project in other_projects:
                file.write(f"\\item {other_project}\n")
            file.write("\\end{itemize}\n")

            file.write("\\vspace{-0.6cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

        # =============================
        # Courses Section
        # =============================
        courses = data.get("courses", {})
        if courses:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont COURSES}\n")

            file.write("\\vspace{-0.3cm}\n")

            for category, course_list in courses.items():
                for course in course_list:
                    date = course.get("date", "")
                    title = course.get("title", "")
                    details = course.get("description", [])

                    if date and title:
                        file.write("\\begin{flushleft}\n")
                        file.write(f"\\textbf{{{title}}}")
                        if(course.get("certificate", "")):
                            file.write(f"\\texttt{{|}} {{\\href{{{course.get('certificate', '')}}}{{Certificate}}}}")
                        file.write(f"\\hfill\\textit{{{date}}}\\\\\n")
                        file.write("\\end{flushleft}\n")

                        file.write("\\vspace{-0.7cm}\n")

                    if details:
                        file.write("\\begin{itemize}\n")
                        for detail in details:
                            file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                        file.write("\\end{itemize}\n")

                    file.write("\\vspace{-0.5cm}\n")
            file.write("\\vspace{-0.1cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

        # =============================
        # EXTRACURRICULAR ACTIVITY Section
        # =============================
        extra = data.get("extra", [])
        if extra:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont EXTRACURRICULAR ACTIVITY}\n")

            file.write("\\vspace{-0.3cm}\n")
            file.write("\\begin{itemize}[noitemsep, left=0pt, itemsep=5pt]\n")
            for extra_info in extra:
                file.write(f"\\item {extra_info}\n")
            file.write("\\end{itemize}\n")

            file.write("\\vspace{-0.6cm}\n")

        file.write("\\end{document}\n")

def generate_special_latex(data, category, output_file):
    header = data.get("header", {})
    if not header:
        return

    name = header.get("name", "")
    contact = header.get("contact", "")
    links = header.get("links", {})

    with open(output_file, 'w') as file:
        # Write LaTeX preamble and header
        file.write("\\documentclass[11pt,a4paper]{article}\n")
        file.write("\\usepackage{geometry}\n")
        file.write("\\usepackage{hyperref}\n")
        file.write("\\usepackage{mathpazo}\n")
        file.write("\\usepackage[scaled=0.92]{helvet}\n")
        file.write("\\usepackage{courier}\n")
        file.write("\\usepackage{amssymb}\n")
        file.write("\\usepackage{enumitem}\n")
        file.write("\\geometry{top=0.3in, bottom=0.3in, left=0.3in, right=0.3in}\n")
        file.write("\\hypersetup{colorlinks=true, linkcolor=black, urlcolor=blue}\n")
        file.write("\\linespread{0.8}\n")
        file.write("\\begin{document}\n")

        # Header Section
        if name and contact and links:
            file.write("\\begin{center}\n")
            file.write(f"\\fontsize{{22}}{{22}}\\textbf{{{name}}}\\\\[0.2cm]\n")
            contact_and_links = "\\fontsize{11}{12}\\textbf{" + \
                f"{contact} " + \
                " \\texttt{{|}} ".join([f"\\href{{{url}}}{{{label}}}" for label, url in links.items()]) + "}\\\\[-0.1cm]\n"
            file.write(contact_and_links)
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")
            file.write("\\end{center}\n")

        file.write(f"\\vspace{{-{LINE_TITLE_SPACE}cm}}\n")

        # Education Section
        education = data.get("education", [])
        if education:
            file.write("\\begin{center}\n")
            file.write(f"\\section*{{\\fontsize{{{TITLE_SIZE}}}{{18}}\\textbf\\selectfont EDUCATION}}\n")
            file.write("\\end{center}\n")

            file.write(f"\\vspace{{-{AFTER_TITLE_SPACE}cm}}\n")

            # Adjust vertical alignment of circular bullet points
            file.write("\\renewcommand\\labelitemi{\\raisebox{0.2ex}{\\scriptsize$\\bullet$}}\n")

            for edu in education:
                year = edu.get("year", "")
                title = edu.get("title", "")
                details = edu.get("details", [])

                if year and title:
                    file.write("\\begin{flushleft}\n")
                    file.write(f"\\textbf{{{title}}}\\hfill\\textit{{{year}}}\\\\\n")
                    file.write("\\end{flushleft}\n")

                    file.write("\\vspace{-0.6cm}\n")

                if details:
                    file.write("\\begin{itemize}\n")
                    for detail in details:
                        file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                    file.write("\\end{itemize}\n")

                file.write("\\vspace{-0.3cm}\n")
            file.write("\\vspace{-0.2cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

            file.write(f"\\vspace{{-{LINE_TITLE_SPACE}cm}}\n")

        # Work Experience Section
        work_experience = data.get("work_experience", [])
        if work_experience:
            file.write("\\begin{center}\n")
            file.write(f"\\section*{{\\fontsize{{{TITLE_SIZE}}}{{ 18 }}\\textbf\\selectfont WORK EXPERIENCE}}\n")
            file.write("\\end{center}\n")

            file.write(f"\\vspace{{-{AFTER_TITLE_SPACE}cm}}\n")

            for work in work_experience:
                date = work.get("date", "")
                header = work.get("header", "")
                body = work.get("body", "")

                if date and header:
                    file.write("\\begin{flushleft}\n")
                    file.write(f"\\textbf{{{header}}}\\hfill\\textit{{{date}}}\\\\\n")
                    file.write("\\end{flushleft}\n")

                    file.write("\\vspace{-0.6cm}\n")

                if body:
                    file.write("\\begin{itemize}\n")
                    file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {body}\n")
                    file.write("\\end{itemize}\n")

                file.write("\\vspace{-0.5cm}\n")

            file.write("\\vspace{0.2cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

        # Skills Section
        skills = data.get("skills", {})
        if skills:
            file.write(f"\\vspace{{-{LINE_TITLE_SPACE}cm}}\n")
            file.write("\\begin{center}\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont SKILLS}\n")
            file.write("\\end{center}\n")

            file.write(f"\\vspace{{-{2*AFTER_TITLE_SPACE}cm}}\n")

            file.write("\\renewcommand{\\arraystretch}{1.8} % Adjust row spacing\n")
            file.write("\\begin{tabular*}{\\textwidth}{@{\\extracolsep{\\fill}} l l}\n")

            # Reorder skills to start with the category
            reordered_skills = {category.capitalize(): skills.get(category.capitalize(), [])}
            for key, value in skills.items():
                if key != category.capitalize():
                    reordered_skills[key] = value

            for cat, skill_data in reordered_skills.items():
                skill_list = skill_data.get("data", [])
                for_ = skill_data.get("for", [])
                if category in for_ and skill_list:
                    file.write(f"\\textbf{{{cat}:}} & {' - '.join(skill_list)} \\\\ \n")

            file.write("\\end{tabular*}\n")
            file.write("\\vspace{0.2cm}\\rule{\\textwidth}{0.3pt}\n")
        
        # =============================
        # Projects Section
        # =============================
        projects = data.get("projects", {})
        if projects:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont PROJECTS}\n")

            file.write("\\vspace{-0.3cm}\n")

            # Start with the projects of the given category
            category_projects = projects.get(category.lower(), [])
            i = 0
            for project in category_projects:
                date = project.get("date", "")
                title = project.get("title", "")
                details = project.get("details", [])

                # Force a page break after a certain number of projects (e.g., every 5 projects)
                if i > 0 and i % 6 == 0:
                    file.write("\\newpage\n")

                if date and title:
                    file.write("\\begin{flushleft}\n")
                    file.write(f"\\textbf{{{title}}}")
                    if(project.get("link", "")):
                        file.write(f"\\texttt{{|}} {{\\href{{{project.get('link', '')}}}{{Link}}}}")
                    file.write(f"\\hfill\\textit{{{date}}}\\\\\n")
                    file.write("\\end{flushleft}\n")

                    file.write("\\vspace{-0.6cm}\n")

                if details:
                    file.write("\\begin{itemize}\n")
                    for detail in details:
                        file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                    file.write("\\end{itemize}\n")

                file.write("\\vspace{-0.3cm}\n")
                i += 1

            # Add the rest of the projects that include the category in their 'for' field
            for other_category, other_projects in projects.items():
                if other_category.lower() != category.lower():
                    for project in other_projects:
                        if category.lower() in [cat.lower() for cat in project.get("for", [])]:
                            date = project.get("date", "")
                            title = project.get("title", "")
                            details = project.get("details", [])

                            # Force a page break after a certain number of projects (e.g., every 5 projects)
                            if i > 0 and i % 7 == 0:
                                file.write("\\newpage\n")

                            if date and title:
                                file.write("\\begin{flushleft}\n")
                                file.write(f"\\textbf{{{title}}}")
                                if(project.get("link", "")):
                                    file.write(f"\\texttt{{|}} {{\\href{{{project.get('link', '')}}}{{Link}}}}")
                                file.write(f"\\hfill\\textit{{{date}}}\\\\\n")
                                file.write("\\end{flushleft}\n")

                                file.write("\\vspace{-0.6cm}\n")

                            if details:
                                file.write("\\begin{itemize}\n")
                                for detail in details:
                                    file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                                file.write("\\end{itemize}\n")

                            file.write("\\vspace{-0.3cm}\n")
                            i += 1

            file.write("\\vspace{-0.2cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

            if i <= 7:
                file.write("\\newpage\n")

        # =============================
        # Other Projects Section
        # =============================
        other_projects = data.get("other_projects", [])
        if other_projects or projects:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont OTHER PROJECTS}\n")

            file.write("\\vspace{-0.3cm}\n")
            
            file.write("\\begin{itemize}[noitemsep, left=0pt, itemsep=5pt]\n")
            for other_project in other_projects:
                file.write(f"\\item {other_project}\n")

            for category_p, project_list in projects.items():
                for project in project_list:
                    if category.lower() != category_p.lower() and category.lower() not in [cat.lower() for cat in project.get("for", [])]:
                        title = project.get("title", "")
                        if title:
                            file.write(f"\\item {title}")
                            if(project.get("link", "")):
                                file.write(f"\\texttt{{|}} {{\\href{{{project.get('link', '')}}}{{Link}}}}")
                            file.write("\n")

            file.write("\\end{itemize}\n")

            file.write("\\vspace{-0.6cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

        othercourses = []
        # =============================
        # Courses Section
        # =============================
        courses = data.get("courses", {})
        if courses:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont COURSES}\n")

            file.write("\\vspace{-0.3cm}\n")

            # Start with the courses of the given category
            category_courses = courses.get(category.lower(), [])
            for course in category_courses:
                date = course.get("date", "")
                title = course.get("title", "")
                details = course.get("description", [])

                if date and title:
                    file.write("\\begin{flushleft}\n")
                    file.write(f"\\textbf{{{title}}}")
                    if(course.get("certificate", "")):
                        file.write(f"\\texttt{{|}} {{\\href{{{course.get('certificate', '')}}}{{Certificate}}}}")
                    file.write(f"\\hfill\\textit{{{date}}}\\\\\n")
                    file.write("\\end{flushleft}\n")

                    file.write("\\vspace{-0.7cm}\n")

                if details:
                    file.write("\\begin{itemize}\n")
                    for detail in details:
                        file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                    file.write("\\end{itemize}\n")

                file.write("\\vspace{-0.5cm}\n")

            # Add the rest of the courses that include the category in their 'for' field
            for other_category, other_courses in courses.items():
                if other_category.lower() != category.lower():
                    for course in other_courses:
                        if category.lower() in [cat.lower() for cat in course.get("for", [])]:
                            date = course.get("date", "")
                            title = course.get("title", "")
                            details = course.get("description", [])

                            if date and title:
                                file.write("\\begin{flushleft}\n")
                                file.write(f"\\textbf{{{title}}}")
                                if(course.get("certificate", "")):
                                    file.write(f"\\texttt{{|}} {{\\href{{{course.get('certificate', '')}}}{{Certificate}}}}")
                                file.write(f"\\hfill\\textit{{{date}}}\\\\\n")
                                file.write("\\end{flushleft}\n")

                                file.write("\\vspace{-0.7cm}\n")

                            if details:
                                file.write("\\begin{itemize}\n")
                                for detail in details:
                                    file.write(f"\\item \\setlength{{\\itemsep}}{{-0.0em}} {detail}\n")
                                file.write("\\end{itemize}\n")

                            file.write("\\vspace{-0.5cm}\n")
                        else:
                            othercourses += [course.get("title", "")] 

            file.write("\\vspace{-0.1cm}\n")
            file.write("\\rule{\\textwidth}{0.3pt}\\\\\n")

        # =============================
        # EXTRACURRICULAR ACTIVITY Section
        # =============================
        extra = data.get("extra", [])
        if extra:
            file.write("\\vspace{-0.5cm}\n")
            file.write("\\centering\n")
            file.write("\\section*{\\fontsize{14}{18}\\textbf\\selectfont EXTRACURRICULAR ACTIVITY}\n")

            file.write("\\vspace{-0.3cm}\n")
            file.write("\\begin{itemize}[noitemsep, left=0pt, itemsep=5pt]\n")
            for extra_info in extra:
                file.write(f"\\item {extra_info}\n")
            file.write("\\end{itemize}\n")

            file.write("\\vspace{-0.6cm}\n")

        file.write("\\end{document}\n")

# Generate PDF from LaTeX file
def generate_pdf(latex_file):
    try:
        subprocess.run(["pdflatex", latex_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")

if __name__ == "__main__":
    data = load_data("data.json")

    # Generate main CV
    name = data.get("name", "")
    main_latex_file = name + "_CV.tex"
    generate_latex(data, main_latex_file)
    generate_pdf(main_latex_file)

    # Generate category-specific CVs
    for category in data.get("specialOrderFiles", []):
        category_latex_file = f"{name}_{category.capitalize()}_CV.tex"
        generate_special_latex(data, category, category_latex_file)
        generate_pdf(category_latex_file)