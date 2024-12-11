from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


from langserve import add_routes

#LANGCHAIN--------------------------------------------------------------------------
from langchain.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_groq import ChatGroq
#------------------------------------------------------------------------------------

import json

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

#Load configuration
with open('api_key.json') as config_file:
    config = json.load(config_file)

#GROQ SETUP---------------------------------------------------------------------------------------------
groq_api_key=config['groq_api_key']
llm = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name="llama3-70b-8192"
    )
#-------------------------------------------------------------------------------------------------------

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

#CHAIN TO ANSWER QUESTION RELATED ARTEFACT IDENTIFICATION-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
template_artefact_identification =  """
You are a digital forensics expert specializing in artifact identification. 
Your task is to analyze and explain digital forensic artifacts such as system logs, metadata, 
timestamps, deleted files, browser histories, and registry entries. 
When you're asked about an artefact, you will:

- Provide the steps or methods to extract and analyze this artifact using tools like Autopsy, EnCase, FTK, or other relevant and correct software.


You should also be able to define or explain any concept in Digital Forensics clearly and simply without being long and while avoiding repetitions.
Ensure your response is precise, and formatted clearly to be easily understood by professionals in the field.
Question: {question}
Answer:
"""    
prompt_artefact_identification = ChatPromptTemplate.from_messages(
    
        [
            ("system", "Given an input question, respond concisely and directly without any preamble."),
            ("human", template_artefact_identification),
        ]    
)
artefact_identification = (
    prompt_artefact_identification
    | llm
    | StrOutputParser()
)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Edit this to add the chain you want to add
add_routes(app, 
        artefact_identification,
        path="/artefact_identification",)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
