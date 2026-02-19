import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

def load_website(url: str):

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise ValueError("Failed to fetch website")

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator="\n")

    # Clean empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    cleaned_text = "\n".join(lines)

    return [Document(page_content=cleaned_text)]
