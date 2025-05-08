# Resume Builder – Tailored Job Description Generator

Resume Builder is a powerful, customizable tool designed to generate tailored resumes and cover letters based on job descriptions. It can work directly from a job posting URL, a local job description file, or an existing tailored resume. This project is perfect for job seekers looking to stand out by aligning their application documents with specific job requirements.

## ✨ Features

- Tailored Resume and Cover Letter Generation: Generate personalized resumes and cover letters based on job descriptions.

- Multiple Input Methods: Use a URL to fetch the job description or provide a local text file.

- PDF Generation: Convert the generated resumes and cover letters to polished, professional PDFs.

- Extensive Customization: Supports fine-tuning of prompts for summary, key strengths, responsibilities and cover letter in resources/instructions.yml


## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- Python
- ollama 


### Installation

#### Run the model
ollama run gemma3:1b

#### Clone the repository:

git clone git@github.com:hasimmollah/resume-builder.git
cd resume-builder

### Install dependencies:

pip install -r requirements.txt

### Run the main app:

python -m src.generate_application_resources --url=https://jobs.ashbyhq.com/caribou/354a2cf7-640b-43a4-b6f6-3da7be834ca6 --output_path=c:\data --prompt_mode=False --job_description_path=c:\jd




## 🛠️ Usage

Add your personal information, work experience, education, and skills in yml format sample is under resources folder

Provide the job description in the file under resources folder or provide the url of the JD as an input to the program

Preview and export your resume & cover letter as a PDF.



## 📧 Contact

For questions or support, please reach out to hasim.mollah@gmail.com or LinkedIn: https://www.linkedin.com/in/hasim-abdul-halim-mollah-a9b54521/

Happy Building! 🚀