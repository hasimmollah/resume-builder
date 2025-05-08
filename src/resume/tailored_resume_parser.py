import re

from model.data_classes import ResumeData


def parse_resume(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define headers and map to output field names
    section_headers = [
        ("Summary", "professional_summary"),
        ("Key Strengths", "key_strengths"),
        ("Employment Summary", "employment_history"),
        ("Certifications", "certifications"),
        ("Education", "education_summary")
    ]

    # Extract name and contact info from the first two lines
    lines = content.splitlines()
    full_name = lines[0].strip()
    contact_info = lines[1].strip()

    parsed = {
        "name": full_name,
        "contact": contact_info
    }
    resume_data = ResumeData()
    setattr(resume_data, "name", full_name)
    setattr(resume_data, "contact", contact_info)

    # Use regex to split based on section headers
    pattern = r"(?<=\n)(?P<header>{})(?=\n)".format("|".join(re.escape(h[0]) for h in section_headers))
    parts = re.split(pattern, content)

    # parts will be: [before_first_header, header1, text1, header2, text2, ..., last_text]
    # we want to pair them as (header -> text)
    section_map = dict(section_headers)

    for i in range(1, len(parts) - 1, 2):
        header = parts[i].strip()
        text = parts[i + 1].strip()
        key = section_map.get(header)
        if key == "key_strengths" or key == "certifications":
            # Split by lines and remove bullets or dashes
            parsed[key] = [line.strip("•-* ").strip() for line in text.splitlines() if line.strip()]
            setattr(resume_data, key, [line.strip("•-* ").strip() for line in text.splitlines() if line.strip()])
        elif key == "employment_history":
            setattr(resume_data, 'company_data', parse_experience_blocks(text))
        else:
            parsed[key] = text
            setattr(resume_data, key, text)
    return resume_data

def parse_experience_blocks(text):
    lines = text.strip().splitlines()
    companies = []
    current_company = None

    # Regex pattern to identify header lines: "Designation | Company | Dates"
    header_pattern = re.compile(r'^\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(.+?)\s*$')

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        match = header_pattern.match(line)
        if match:
            # Save previous company entry if exists
            if current_company:
                companies.append(current_company)

            # Start a new company block
            current_company = {
                'designation': match.group(1).strip(),
                'company': match.group(2).strip(),
                'start_end': match.group(3).strip(),
                'responsibilities': []
            }
        else:
            # Add responsibility line to the current company
            if current_company:
                current_company['responsibilities'].append(line)

    # Add the last parsed company block
    if current_company:
        companies.append(current_company)

    return companies
