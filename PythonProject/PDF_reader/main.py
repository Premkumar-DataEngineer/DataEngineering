from pypdf import PdfReader
from llm import markdown
import pdfplumber

# Initialize the reader object
reader = PdfReader("/Users/navyadev/Documents/GitHub/DataEngineering/PythonProject/PDF_reader/Source/sample.pdf")

# Get total page count
print(f"Total Pages: {len(reader.pages)}")

# Extract text from the first page (index 0)
first_page = reader.pages[0]
text = first_page.extract_text()

print("\n--- First Page Content ---")
print(text)
markdown_text = md(text)
print(markdown_text)