#from loader import load_document
from lensegt.my_backend.qna_engine import *
from lensegt.my_backend.SQL_engine import *
from lensegt.my_backend.csv_engine import *
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from enum import Enum
from lensegt.my_backend.qna_engine import embed_and_run_openai, embed_and_run_azureopenai, embed_and_run_mistral, embed_and_run_model
import shutil
import os
from lensegt.my_backend.loader import load_document, load_directory
from fastapi import FastAPI, Request ,APIRouter
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
import uvicorn
import warnings
from typing import List, Optional, Union
from pydantic import BaseModel
warnings.filterwarnings('ignore')
from lensegt import lense
from lensegt.my_backend.chat_history import *
from datetime import datetime
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
 CORSMiddleware,
 allow_origins=["*"],
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)

# Define an Enum for engine selection
class EngineType(str, Enum):
    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"
    HuggingFace = "HuggingFace"
    GOOGLE_GENAI = "Google GenAI"

class MistralModel(str, Enum):
    MIXTRAL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    MISTRAL = "mistralai/Mistral-7B-Instruct-v0.2"
    GEMMA = "google/gemma-7b"
    PHI = "microsoft/Phi-3-mini-4k-instruct"
    TINYLLAMA = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    STABLELM = "stabilityai/stablelm-2-zephyr-1_6b"
    H2O = "h2oai/h2o-danube2-1.8b-chat"

# class EngineType1(str, Enum):
#     OPENAI = "OpenAI"
#     AZURE_OPENAI = "Azure OpenAI"

# class EngineType2(str, Enum):
#     OPENAI = "OpenAI"
#     AZURE_OPENAI = "Azure OpenAI"
#     GOOGLE_GENAI = "Google GenAI"

# List to store engines
engines = []
engine_name = ''

# Temporary directory to store uploaded files
temporary_folder = "temp_uploaded_files"
file_extension = ''
database_url = ''

# Ensure the temporary folder exists
os.makedirs(temporary_folder, exist_ok=True)

@app.post("/upload/")
async def upload_files(
    file: UploadFile = File(None),
    DB_URL: str = Form(None)
):
    global database_url
    global file_extension
    try:
        
        if file and DB_URL:
            return {"error": "Only one input should be provided"}

        elif file:
            file_extension = Path(file.filename).suffix.lower()

            # Check the file extension
            if file_extension not in (".csv", ".pdf", ".docx", ".ppt", ".json"):
                return {"error": "Unsupported file format."}
            # Save the uploaded file to the temporary directory
            save_path = os.path.join(temporary_folder, file.filename)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
    
            return {"result": "Files uploaded to temporary folder successfully", "folder_path": temporary_folder}

        elif DB_URL:
            database_url = DB_URL
            return {"result": "String input received successfully", "string_input": DB_URL}
        
        else :
            return {"error": "No input provided."}
    
    except Exception as e:
        return {"error": str(e)}
    


@app.post("/create_engine/")
async def process_documents(
    engine_type: EngineType,
    selected_model: MistralModel = None,
    api_key: str = Form(None),
    api_version: str = Form(None),
    azure_endpoint: str = Form(None),
    google_api_key: str = Form(None),
    hf_token: str = Form(None)
):
    global temporary_folder
    global file_extension
    global database_url

    if file_extension in (".pdf", ".docx", ".ppt", ".json"):
        try:
            # Check if any file has been uploaded
            if not temporary_folder:
                return {"error": "No files uploaded"}

            # Load documents from the uploaded files
            documents = []
            documents.extend(load_directory(temporary_folder))
            
            # Select and run the appropriate engine based on user input
            if engine_type == EngineType.OPENAI:
                if api_key is None:
                    return {"error": "api_key is required for OpenAI"}
                engine, index = embed_and_run_openai(
                    documents=documents,
                    api_key=api_key
                )
                engine_name = 'OPENAI'
            elif engine_type == EngineType.AZURE_OPENAI:
                if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                    return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
                engine, index = embed_and_run_azureopenai(
                    documents=documents,
                    api_key=api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint
                )
                engine_name = 'AZURE_OPENAI'
            elif engine_type == EngineType.HuggingFace:
                if hf_token is None or selected_model is None:
                    return {"error": "hf_token and selected_model are required for Mistral"}
                engine, index = embed_and_run_model(
                    documents=documents,
                    hf_token=hf_token,
                    model=selected_model
                )
                engine_name = 'HuggingFace'
            else:
                return {"error": "Invalid engine type"}
            
            # Store the engine in the list
            engines.append(engine)
            
            # Clean up: Remove the temporary files
            # if os.path.exists('temp_uploaded_files'):
            #     shutil.rmtree('temp_uploaded_files')
            #     print("Temporary folder removed")

            if os.path.exists('temp_uploaded_files'):
                for filename in os.listdir('temp_uploaded_files'):
                    file_path = os.path.join('temp_uploaded_files', filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")
                print("Temporary files removed")
            
            return {"result": "Engine created and stored successfully"}
        
        except Exception as e:
            return {"error": str(e)}
        
    elif file_extension == '.csv':
        try:

            if os.path.isdir(temporary_folder):
                files = os.listdir(temporary_folder)

                # Check if there is exactly one file in the folder
                if len(files) == 1:
                    file_path = os.path.join(temporary_folder, files[0])
                    documents = load_document(file_path)
                else:
                    return {"error": "Temporary folder should contain exactly one CSV file"}
            else:
                return {"error": "Temporary folder not found"}
            
            # Select and run the appropriate engine based on user input
            if engine_type == EngineType.OPENAI:
                if api_key is None:
                    return {"error": "api_key is required for OpenAI"}
                engine = csv_engine_openai(
                    df=documents,
                    api_key=api_key
                )
            elif engine_type == EngineType.AZURE_OPENAI:
                if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                    return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
                engine = csv_engine_azure(
                    df=documents,
                    api_key=api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint
                )
            else:
                return {"error": "Invalid engine type"}
            
            # Store the engine in the list
            engines.append(engine)
            
            if os.path.exists('temp_uploaded_files'):
                for filename in os.listdir('temp_uploaded_files'):
                    file_path = os.path.join('temp_uploaded_files', filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")
                print("Temporary files removed")
            
            return {"result": "Engine created and stored successfully"}
        
        except Exception as e:
            return {"error": str(e)}
        
    elif database_url != '':
        try:
            # Select and run the appropriate engine based on user input
            if engine_type == EngineType.OPENAI:
                if api_key is None:
                    return {"error": "api_key is required for OpenAI"}
                engine = sql_engine_openai(db_url=database_url, api_key=api_key)
            elif engine_type == EngineType.AZURE_OPENAI:
                if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                    return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
                engine = sql_engine_azure(db_url=database_url, api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
            elif engine_type == EngineType.GOOGLE_GENAI:
                if google_api_key is None:
                    return {"error": "google_api_key is required for Google GenAI"}
                engine = sql_engine_genai(db_url=database_url, api_key=google_api_key)
            else:
                return {"error": "Invalid engine type"}

            # Store the engine in the list
            engines.append(engine)
            
            return {"result": "Engine created and stored successfully"}
        
        except Exception as e:
            return {"error": str(e)}
    

@app.post("/chat")
async def use_engine(
    query: str = Form(...)
):
    print("Inside the chat of the query")
    for ele in engines:
        print("Value of the engine is ",ele)

    if file_extension in (".pdf", ".docx", ".ppt", ".json"):
        print("Inside the correct file extesion")

        try:
            return_response = {
                                "data_points": '',
                                "thoughts": '',
                                "exchange_id": 123,
                                "tokens": 0,
                                "recommended_question": '',
                                "isChartRequired": '',
                                "product_list": [],
                                "question_count": 0,
                                "user_limit": 0,
                                "guest_limit": 0
                            }
            # Check if any engine has been stored
            print("Inside the try of the return_responses")
            if not engines:
                return {"error": "No engine available"}
            
            print("After the if")
            # Use the latest stored engine to run the query
            print("Length of the engines is  ",len(engines))
            for ele in engines:
                print("Value of the engine is ",ele)
            engine = engines[-1]
            result = engine(query)
            response = str(result)
            pattern = r'Answer:\s*(.*)'
            matches = re.findall(pattern, response, re.DOTALL)
            answer = ""
            if matches:
                for match in matches:
                    print(match)
                    answer+=match
            else:
                answer += response

            return_response['answer'] = answer
            
            log_chat(datetime.now(), query, answer, engine_name )  # Log the interaction to the database

            return return_response
        
        except Exception as e:
            print("Insid ethe exception  of chat")
            return {"error": str(e)}
        
    elif file_extension == '.csv':
        try:
            return_response = {
                                "data_points": '',
                                "thoughts": '',
                                "exchange_id": 123,
                                "tokens": 0,
                                "recommended_question": '',
                                "isChartRequired": '',
                                "product_list": [],
                                "question_count": 0,
                                "user_limit": 0,
                                "guest_limit": 0
                            }
            # Check if any engine has been stored
            if not engines:
                return {"error": "No engine available"}
            
            # Use the latest stored engine to run the query
            engine = engines[-1]
            result = engine(query_str=query)
            result = result.message.content
            return_response['answer'] = str(result)

            return return_response
    
        except Exception as e:
            return {"error": str(e)}
        
    elif database_url != '':
        try:
            return_response = {
                                "data_points": '',
                                "thoughts": '',
                                "exchange_id": 123,
                                "tokens": 0,
                                "recommended_question": '',
                                "isChartRequired": '',
                                "product_list": [],
                                "question_count": 0,
                                "user_limit": 0,
                                "guest_limit": 0
                            }
            # Check if any engine has been stored
            if not engines:
                return {"error": "No engine available"}
            
            # Use the latest stored engine to run the query
            engine = engines[-1]
            result = engine(query)
            return_response['answer'] = str(result)
            return return_response
        
        except Exception as e:
            return {"error": str(e)}
    
@app.post("/View-History/")
async def view_history():
    try:
        history = view_chat_logs()
        return {"Hostory":history}
    except Exception as e:
        return {"error": str(e)}
    

def load_file(
    file: UploadFile = File(None),
    DB_URL: str = Form(None)
    ):
    global database_url
    global file_extension
    try:
        
        file_extension = Path(file.filename).suffix.lower()

        # Check the file extension
        if file_extension not in (".csv", ".pdf", ".docx", ".ppt", ".json"):
            return {"error": "Unsupported file format."}
        # Save the uploaded file to the temporary directory
        save_path = os.path.join(temporary_folder, file.filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"result": "Files uploaded to temporary folder successfully", "folder_path": temporary_folder}

        
    
    except Exception as e:
        return {"error": str(e)}
    
def engine(
    engine_type: EngineType,
    selected_model: MistralModel = None,
    api_key: str = Form(None),
    api_version: str = Form(None),
    azure_endpoint: str = Form(None),
    google_api_key: str = Form(None),
    hf_token: str = Form(None)
):
    global temporary_folder
    global file_extension
    global database_url

    if file_extension in (".pdf", ".docx", ".ppt", ".json"):
        try:
            # Check if any file has been uploaded
            if not temporary_folder:
                return {"error": "No files uploaded"}

            # Load documents from the uploaded files
            documents = []
            documents.extend(load_directory(temporary_folder))
            
            # Select and run the appropriate engine based on user input
            if engine_type == EngineType.OPENAI:
                if api_key is None:
                    return {"error": "api_key is required for OpenAI"}
                engine, index = embed_and_run_openai(
                    documents=documents,
                    api_key=api_key
                )
                engine_name = 'OPENAI'
            elif engine_type == EngineType.AZURE_OPENAI:
                if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                    return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
                engine, index = embed_and_run_azureopenai(
                    documents=documents,
                    api_key=api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint
                )
                engine_name = 'AZURE_OPENAI'
            elif engine_type == EngineType.HuggingFace:
                if hf_token is None or selected_model is None:
                    return {"error": "hf_token and selected_model are required for Mistral"}
                engine, index = embed_and_run_model(
                    documents=documents,
                    hf_token=hf_token,
                    model=selected_model
                )
                engine_name = 'HuggingFace'
            else:
                return {"error": "Invalid engine type"}
            
            # Store the engine in the list
            engines.append(engine)
            
            # Clean up: Remove the temporary files
            # if os.path.exists('temp_uploaded_files'):
            #     shutil.rmtree('temp_uploaded_files')
            #     print("Temporary folder removed")

            if os.path.exists('temp_uploaded_files'):
                for filename in os.listdir('temp_uploaded_files'):
                    file_path = os.path.join('temp_uploaded_files', filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")
                print("Temporary files removed")
            
            return {"result": "Engine created and stored successfully"}
        
        except Exception as e:
            return {"error": str(e)}
        
    elif file_extension == '.csv':
        try:

            if os.path.isdir(temporary_folder):
                files = os.listdir(temporary_folder)

                # Check if there is exactly one file in the folder
                if len(files) == 1:
                    file_path = os.path.join(temporary_folder, files[0])
                    documents = load_document(file_path)
                else:
                    return {"error": "Temporary folder should contain exactly one CSV file"}
            else:
                return {"error": "Temporary folder not found"}
            
            # Select and run the appropriate engine based on user input
            if engine_type == EngineType.OPENAI:
                if api_key is None:
                    return {"error": "api_key is required for OpenAI"}
                engine = csv_engine_openai(
                    df=documents,
                    api_key=api_key
                )
            elif engine_type == EngineType.AZURE_OPENAI:
                if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                    return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
                engine = csv_engine_azure(
                    df=documents,
                    api_key=api_key,
                    api_version=api_version,
                    azure_endpoint=azure_endpoint
                )
            else:
                return {"error": "Invalid engine type"}
            
            # Store the engine in the list
            engines.append(engine)
            
            if os.path.exists('temp_uploaded_files'):
                for filename in os.listdir('temp_uploaded_files'):
                    file_path = os.path.join('temp_uploaded_files', filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")
                print("Temporary files removed")
            
            return {"result": "Engine created and stored successfully"}
        
        except Exception as e:
            return {"error": str(e)}
        
    elif database_url != '':
        try:
            # Select and run the appropriate engine based on user input
            if engine_type == EngineType.OPENAI:
                if api_key is None:
                    return {"error": "api_key is required for OpenAI"}
                engine = sql_engine_openai(db_url=database_url, api_key=api_key)
            elif engine_type == EngineType.AZURE_OPENAI:
                if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                    return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
                engine = sql_engine_azure(db_url=database_url, api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
            elif engine_type == EngineType.GOOGLE_GENAI:
                if google_api_key is None:
                    return {"error": "google_api_key is required for Google GenAI"}
                engine = sql_engine_genai(db_url=database_url, api_key=google_api_key)
            else:
                return {"error": "Invalid engine type"}

            # Store the engine in the list
            engines.append(engine)
            
            return {"result": "Engine created and stored successfully"}
        
        except Exception as e:
            return {"error": str(e)}
        
def chat_query(
    query: str = Form(...)
    ):
    print("Inside the chat of the query")
    for ele in engines:
        print("Value of the engine is ",ele)

    if file_extension in (".pdf", ".docx", ".ppt", ".json"):
        print("Inside the correct file extesion")

        try:
            return_response = {
                                "data_points": '',
                                "thoughts": '',
                                "exchange_id": 123,
                                "tokens": 0,
                                "recommended_question": '',
                                "isChartRequired": '',
                                "product_list": [],
                                "question_count": 0,
                                "user_limit": 0,
                                "guest_limit": 0
                            }
            # Check if any engine has been stored
            print("Inside the try of the return_responses")
            if not engines:
                return {"error": "No engine available"}
            
            print("After the if")
            # Use the latest stored engine to run the query
            print("Length of the engines is  ",len(engines))
            for ele in engines:
                print("Value of the engine is ",ele)
            engine = engines[-1]
            result = engine(query)
            response = str(result)
            pattern = r'Answer:\s*(.*)'
            matches = re.findall(pattern, response, re.DOTALL)
            answer = ""
            if matches:
                for match in matches:
                    print(match)
                    answer+=match
            else:
                answer += response

            return_response['answer'] = answer
            
            log_chat(datetime.now(), query, answer, engine_name )  # Log the interaction to the database

            return return_response
        
        except Exception as e:
            print("Insid ethe exception  of chat")
            return {"error": str(e)}
        
    elif file_extension == '.csv':
        try:
            return_response = {
                                "data_points": '',
                                "thoughts": '',
                                "exchange_id": 123,
                                "tokens": 0,
                                "recommended_question": '',
                                "isChartRequired": '',
                                "product_list": [],
                                "question_count": 0,
                                "user_limit": 0,
                                "guest_limit": 0
                            }
            # Check if any engine has been stored
            if not engines:
                return {"error": "No engine available"}
            
            # Use the latest stored engine to run the query
            engine = engines[-1]
            result = engine(query_str=query)
            result = result.message.content
            return_response['answer'] = str(result)

            return return_response
    
        except Exception as e:
            return {"error": str(e)}
        
    elif database_url != '':
        try:
            return_response = {
                                "data_points": '',
                                "thoughts": '',
                                "exchange_id": 123,
                                "tokens": 0,
                                "recommended_question": '',
                                "isChartRequired": '',
                                "product_list": [],
                                "question_count": 0,
                                "user_limit": 0,
                                "guest_limit": 0
                            }
            # Check if any engine has been stored
            if not engines:
                return {"error": "No engine available"}
            
            # Use the latest stored engine to run the query
            engine = engines[-1]
            result = engine(query)
            return_response['answer'] = str(result)
            return return_response
        
        except Exception as e:
            return {"error": str(e)}
    
def start():
    print("-"*100)
    print("Inside the the start function")
    print("current path of directory",os.getcwd())
    file_path =  lense.__file__
    path = os.path.join(os.path.dirname(os.path.dirname(file_path)),"my_frontend")

    app.mount("/", StaticFiles(directory=path, html=True), name="my_frontend")

    # running in pip installer
    # uvicorn.run("lense.app:app", reload=False, host="127.0.0.1", port=9017,workers=1)

    # running in local through demo.py
    uvicorn.run("lensegt.lense.app:app", reload=False, host="127.0.0.1", port=9017,workers=1)