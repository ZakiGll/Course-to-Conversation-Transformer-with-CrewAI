from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import os
import PyPDF2
import pytesseract 

from elevenlabs import generate, save, voices
from elevenlabs import set_api_key



load_dotenv(find_dotenv())
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

gemini = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.5,google_api_key=GOOGLE_API_KEY)


def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

    return text




def start_working(context):

    reader = Agent(
    role='Academic Content expert',
    goal='Craft compelling content for academic purpose',
    backstory="""You are a renowned Academic Content expert, known for
    your insightful and engaging ways to simplify things for students.
    You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True,
    llm=gemini
    )

    examples_giver = Agent(
    role='Expert teacher',
    goal='Simplify and give real word examples',
    backstory="""You are a teacher with extensive experience, known for the insightful real-world examples you provide to simplify concepts for your students.""",
    verbose=True,
    allow_delegation=True,
    llm=gemini
    )

    narrator = Agent(
    role='Expert narrator',
    goal='Transform the content to a narative conversation',
    backstory="""You are an expert narrator known for your ability to create a special type of story as a conversation between two persons, bringing the narrative to life.""",
    verbose=True,
    allow_delegation=True,
    llm=gemini
    )
    task1 = Task(
        description=f"""Analyze the content of the following academic course : \n {context} \n\n, Extract essential points for a comprehensive overview. Identify key insights, noteworthy information, and significant details from the document. The extracted content will be utilized to deliver a clear and informative explanation of the subject matter to students. Your final output must be a detailed analysis report.You don't need to use any other tool!
        """,
        agent=reader
    )

    task2 = Task(
        description="""Using the insights provided, generate clear and insightful real-world examples that enhance understanding. Your examples should be relatable, engaging, and effective in making the subject matter more accessible to students.""",
        agent=examples_giver
    )

    task3 = Task(
        description=""""Create a simulated conversation between a teacher and a student using the extracted data, trends, and real-world examples provided earlier. The teacher should initiate the conversation by explaining a concept or trend related to the analyzed content. The student responds with questions or requests for clarification, and the teacher continues the dialogue by providing further insights, explanations, or additional examples. The conversation should reflect a dynamic interaction, with the teacher guiding the student's understanding in a clear and engaging manner. Ensure that the dialogue format is teacher: '...' student: '...'.And make sure to don't add any other text expect the conversation""",
        agent=examples_giver
    )

    crew = Crew(
        agents=[reader, examples_giver, narrator],
        tasks=[task1, task2, task3],
        verbose=2, 
        )
    
    result = crew.kickoff()

    return result

def text_to_list(text):
    text = remove_empty_lines(text)
    dialogues = []
    lines = text.strip().split("\n")
    for line in lines:
        character, dialogue = line.split(": ", 1)
        dialogue = dialogue.strip().strip('"')
        dialogues.append((character, dialogue))

    return dialogues

def remove_empty_lines(text):
    lines = text.splitlines() 
    non_empty_lines = [line for line in lines if line.strip() != ""]  
    result = "\n".join(non_empty_lines) 
    return result


def text_to_audio(dialogue):
    dialogue = text_to_list(dialogue)
    generated_audio_chunks = []
    for character, dialogue in dialogue:
            if character == 'Student':
                audio = generate(
                    text = dialogue,
                    voice = "Patricia - smooth",
                    model = 'eleven_multilingual_v1',
                    )
                generated_audio_chunks.append(audio)
            else :
                audio = generate(
                    text = dialogue,
                    voice = "Dan Dan",
                    model = 'eleven_multilingual_v1',
                    )
                generated_audio_chunks.append(audio)
        
        
    combined_audio = b''.join(generated_audio_chunks)
    combined_audio_path = "combined_audio.mp3"
    save(combined_audio, combined_audio_path)
    print("Combined audio saved!")