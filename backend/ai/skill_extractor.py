import re


SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Flask",
    "Django",
    "Spring Boot",
    "React",
    "Node.js",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "NLP",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "DSA",
    "OOP",
    "DBMS",
    "Operating Systems"
]


def extract_skills(text):

    if not text:
        return []


    technical_skills_section = extract_technical_skills_section(
        text
    )


    if not technical_skills_section:
        return []


    detected_skills = []


    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )


        if re.search(
            pattern,
            technical_skills_section,
            re.IGNORECASE
        ):

            detected_skills.append(
                skill
            )


    return detected_skills


def extract_technical_skills_section(text):

    """
    Extract only the content between the
    Technical Skills heading and the next
    major resume section.
    """

    section_pattern = re.compile(
        r"""
        (?:technical\s+skills|technical\s+skill)
        \s*[:\-]?\s*
        (.*?)
        (?=
            \n\s*
            (?:
                projects|
                education|
                experience|
                work\s+experience|
                certifications?|
                additional\s+information|
                achievements?|
                coursework|
                interests?|
                hobbies?|
                summary|
                objective|
                professional\s+summary|
                declaration|
                references?
            )
            \s*:?\s*
            \n
            |
            $
        )
        """,
        re.IGNORECASE | re.DOTALL | re.VERBOSE
    )


    match = section_pattern.search(text)


    if not match:
        return ""


    return match.group(1).strip()