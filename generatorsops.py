import streamlit as st
import io
import os
import openai as ai
from PyPDF2 import PdfReader
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.

ai.api_key = os.getenv("OPENAI_API_KEY")






def generate_sop(template_text, res_text,programme,user_name,university):
    completion = ai.ChatCompletion.create(
      #model="gpt-3.5-turbo-16k", 
      model = "gpt-4o-2024-05-13",
      temperature=ai_temp,
          messages=[
        {"role": "user", "content": "Generate a statement of purpose based on the provided details, following a specific structure and style."},
        {"role": "user", "content": f"Template for guidance: {template_text}. You should reproduce the exact same structure"},
        {"role": "user", "content": f"Resume information: {res_text}"},
        {"role": "user", "content": f"Study programme name: {programme}"},
        {"role": "user", "content": f"Candidate's name: {user_name}"},
        {"role": "user", "content": f"University name: {university}"},
        # {"role": "user", "content": f"Description of the university: {university_desc}"},
        # {"role": "user", "content": f"Content of the study programme: {programme_content}"},
        {"role": "user", "content": "1st Paragraph:  introduction about your name, background, and programme and university you are applying and also mention the reason within one line why to choose this programme"},
        {"role": "user", "content": """2nd Paragraph: Discuss the candidate's academic and professional background :
         IF CGPA score is more than 7 and his Bachelor graduation date is PAST : Mention his CGPA score.
         Mention ALL his work experiences and the different roles and responsibilities he held
         Retrieve ALL extra curricular activites and workshops he has attended and list them like a bulleted list
         Mention all his certificates
         """},
        {"role": "user", "content": f"""3rd Paragraph: Based on the information from Internet about the programme and based on the resume : {res_text}, do the following : :
            Show a Strong motivation by evoking a storytelling from your past that led you to want to study this programme
         	Explain also why you are STRONGLY MOTIVATED to pursue this programme by relating to your previous experience
            Select some modules proposed by the programme and describe their contents, then explain why you are HIGHLY motivated to study them.
	        Explain Why this programme can help you build your career and prepare you for your future  
         
         """},
        {"role": "user", "content": f"""4th Paragraph: Based on the information from Internet, you should retrieve the following data :
                                                        Exact ranking of the University and the source of ranking
	                                                    Number of students
	                                                    facilities, faculties , campus location
	                                                    Precise you have relatives and friends there
	                                                    Names of research centers linked to the programme
        You should use ALL these data and invent for each one an element of motivation make you want to integrate the University
            
        In this paragraph you should also mention why you want to study in the city of the University , mention :  Some cool spots in the city you would like to see
                                                                                                                   names of companies in the city of the same field of your study        
         """},
        {"role": "user", "content": """5th Paragraph: Explain why you chose to study in Germany :
         You should mention :
         Intention to stay in Germany because the field education comparative is far better to others destinations,
	     Good exposure, diversity and culture 
	     Mention examples of cooperations between indian and germany linked to your area of study and how you see yourself participating in it in the future ! Search for last news information you have
         """},
        {"role": "user", "content": "6th Paragraph: Describe your future career perspectives and aspirations post-study. Show your intentions and reasons to stay and work in Germany"},
        {"role": "user", "content": "Last Paragraph: A brief conclusion summarizing why you are the ideal applicant and show again your interest."},
        {"role": "user", "content": "Finish with a closing line with consideration of this statement of purpose and add your name signature bellow"},
        {"role": "user", "content": "Please ensure each paragraph transitions smoothly into the next, maintaining a logical flow throughout the document."},
        {"role": "user", "content": "The statement of purpose should consist of seven paragraphs, totaling a minimum of 500 words, using simple language that appears human-written."},
        {"role": "user", "content": "MOST IMPORTANT : Make sure the tone is warm, simple and human-like. Use simple words. Simple please."}

    ]
    )

    response_out = completion['choices'][0]['message']['content']
    st.write(response_out)
    return response_out
    



def create_word_document(phrase, font_name, font_size):
    doc = Document()
    doc.add_paragraph(phrase)

    # Set font properties
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
            
        # Set paragraph alignment to justified
    for paragraph in doc.paragraphs:
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY

    return doc

def save_doc_to_buffer(doc):
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
    
    










st.markdown("""
# 📝 AI-Powered SOP Generator

Generate a sop letter : JUST READ THE INSTRUCTIONS BRO
"""
)

# radio for upload or copy paste option         
res_format = st.radio(
    "Do you want to upload or paste your resume/key experience",
    ('Upload', 'Paste'))

if res_format == 'Upload':
    # upload_resume
    res_file = st.file_uploader('📁 Upload your resume in pdf format')
    if res_file:
        pdf_reader = PdfReader(res_file)

        # Collect text from pdf
        res_text = ""
        for page in pdf_reader.pages:
            res_text += page.extract_text()
else:
    # use the pasted contents instead
    res_text = st.text_input('Pasted resume elements')
    
 
 
# radio for upload or copy paste option         
template_format = st.radio(
    "Do you want to upload or paste the template",
    ('Upload', 'Paste'))

if template_format == 'Upload':     
        # upload_resume
    template_file = st.file_uploader('📁 Upload your template in pdf format')
    if template_file:
        pdf_reader = PdfReader(template_file)

        # Collect text from pdf
        template_text = ""
        for page in pdf_reader.pages:
            template_text += page.extract_text()
else:
    # use the pasted contents instead
    template_text = st.text_input('Pasted template elements')
            
            

with st.form('input_form'):
    # other inputs
    programme = st.text_input('Programme name')
    user_name = st.text_input('name')
    university = st.text_input('University name')
    # programme_content = st.text_input('Programme content')
    # university_desc = st.text_input('University Description')
    ai_temp = st.number_input('AI Temperature (0.0-1.0) Input how creative the API can be',value=.6)

    # submit button
    submitted = st.form_submit_button("Generate the SOP")

# if the form is submitted run the openai completion   
if submitted:
    response = generate_sop(template_text, res_text,programme,user_name,university)
    # include an option to download a txt file
    # st.download_button('Download the statement of purpose', response)
    doc_download1 = create_word_document(response, 'Arial', 11)
    st.download_button(
            label="Download SOP",
            data=save_doc_to_buffer(doc_download1),
            file_name=f"{res_file.name}_{university}_{programme}_SOP.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


    

