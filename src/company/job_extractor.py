import json
import logging

import requests
from bs4 import BeautifulSoup, Tag

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)


def extract_job_description_no_headless(url):
    with sync_playwright() as p:
        # Launch the browser in non-headless mode to see what happens
        browser = p.chromium.launch(headless=False)  # Set headless=False to see the browser window
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = browser.new_page()

        # Hide webdriver property to avoid detection
        page.evaluate("navigator.__defineGetter__('webdriver', function(){return undefined;})")

        # Go to the URL and wait until the DOM is loaded completely
        page.goto(url, wait_until='networkidle')

        # Wait a bit to ensure all JavaScript content has loaded
        page.wait_for_timeout(5000)  # wait for 5 seconds if there's heavy JavaScript loading
        html_content = page.content()
        logger.info(html_content)

        json_ld_script = page.query_selector('script[type="application/ld+json"]')

        if json_ld_script:
            json_content = json_ld_script.inner_html()
            job_data = json.loads(json_content)

            # Extract the job description
            job_description = job_data.get('description', None)

            if job_description:
                soup = BeautifulSoup(job_description, "html.parser")
                job_description = soup.get_text(separator="\n", strip=True)
            else:
                logger.info("Job description not found in the JSON-LD script.")
        else:
            # Try to extract the job description from possible places
            job_description = page.inner_text('div.job-description')  # Try div with class 'job-description'
            if not job_description:
                job_description = page.inner_text('div')  # Try extracting content from any div
            if not job_description:
                job_description = page.inner_text('label')  # Check if it's inside a label

        logger.info("Job Description Extracted: ", job_description)

        # Close the browser after extraction
        browser.close()
        return job_description

def extract_job_description(url):
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Visit the job URL
        page.goto(url, wait_until='domcontentloaded')
        page.wait_for_timeout(5000)  # Allow JS to load

        # Get the full page content
        html_content = page.content()
        logger.info(html_content)
        browser.close()

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 1. Extract from known classes
        known_classes = ['job-description', 'description', 'content', 'jd', 'posting-description']
        for cls in known_classes:
            desc = soup.find('div', class_=cls)
            if desc:
                return desc.get_text(separator="\n", strip=True)

        # 2. Extract from general <div> without a specific class
        for div in soup.find_all('div'):
            text = div.get_text(separator="\n", strip=True)
            if "job description" in text.lower() and len(text) > 100:
                return text

        # 3. Extract from headings within divs
        for heading in soup.find_all(['h1', 'h2', 'h3', 'strong', 'b']):
            if "description" in heading.get_text(strip=True).lower():
                description = ""
                sibling = heading.find_next_sibling()
                while sibling and sibling.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    description += sibling.get_text(separator="\n", strip=True) + "\n"
                    sibling = sibling.find_next_sibling()
                if description.strip():
                    return description.strip()

        # 4. Extract from <label> within <div>
        for div in soup.find_all('div'):
            labels = div.find_all('label')
            if labels:
                description = "\n".join(label.get_text(strip=True) for label in labels)
                if "description" in description.lower() and len(description) > 100:
                    return description

        # Fallback if nothing found
        return "Job description not found."

def extract_job_details(url):
    # Fetch the webpage content
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the job title
    job_title = soup.find('h1')
    job_title = job_title.get_text(strip=True) if job_title else "Not Found"

    # Extract the location
    location = soup.find('div', class_='location')
    location = location.get_text(strip=True) if location else "Not Found"

    # Extract the company name
    company_name = soup.find('meta', attrs={'name': 'og:site_name'})
    company_name = company_name['content'].strip() if company_name else "Not Found"

    # Extract job description - multiple strategies
    job_description = ""

    # Strategy 1: Known classes like "job-description"
    known_description_classes = ['job-description', 'description', 'job-desc', 'jd', 'content']
    for cls in known_description_classes:
        desc = soup.find('div', class_=cls)
        if desc:
            job_description = desc.get_text(separator="\n", strip=True)
            break

    # Strategy 2: Heading-based extraction
    if not job_description:
        for heading in soup.find_all(['h1', 'h2', 'h3', 'strong', 'b']):
            if 'description' in heading.get_text(strip=True).lower():
                # Capture everything following the heading
                job_description = ""
                sibling = heading.find_next_sibling()
                while sibling and isinstance(sibling, Tag):
                    job_description += sibling.get_text(separator="\n", strip=True) + "\n"
                    sibling = sibling.find_next_sibling()
                break

    # Clean up the description
    job_description = job_description.strip() if job_description else "Not Found"

    # Extract skills from bullet points within the job description
    skills = []
    if job_description != "Not Found":
        for line in job_description.split("\n"):
            if line.startswith("•") or line.startswith("-") or line.startswith("*"):
                skills.append(line.strip())

    # Return the extracted details
    return {
        "Job Title": job_title,
        "Location": location,
        "Company Name": company_name,
        "Job Description": job_description,
        "Skills": skills
    }

if __name__ == "__main__":
    # Example usage
    url = "https://jobs.ashbyhq.com/caribou/354a2cf7-640b-43a4-b6f6-3da7be834ca6"
    details = extract_job_description_no_headless(url)

    # Print the extracted details
    for key, value in details.items():
        logger.info(f"{key}:")
        if isinstance(value, list):
            for item in value:
                logger.info(f"  - {item}")
        else:
            logger.info(value)
        logger.info("\n")
