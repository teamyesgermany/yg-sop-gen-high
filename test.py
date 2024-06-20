# from docx import Document



# def read_docx(file):
#     doc = Document(file)
#     full_text = []
#     for para in doc.paragraphs:
#         full_text.append(para.text)
#     return '\n'.join(full_text)

# print(read_docx('templates4\CV_MANJU RAJU N_PS.docx'))

import textract
text = textract.process("templates4\CV_MANJU RAJU N_PS.docx")
print(text)