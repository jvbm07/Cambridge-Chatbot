import PyPDF2

def pdf_to_text_pypdf2(pdf_file, txt_file):
    # Create a PDF file reader object
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        # Extract text from each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n"

    # Save the extracted text to a .txt file
    with open(txt_file, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

# Example usage
pdf_to_text_pypdf2('execed-brochure-alp-v8.pdf', 'output.txt')