from fastapi import FastAPI, WebSocket, Request, File, UploadFile, Form, Request, HTTPException, Header,WebSocketDisconnect
from flask import request, jsonify
from pydantic import BaseModel, EmailStr
from llama_index.llms.llama_cpp import LlamaCPP
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import asyncio
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import vertexai
from vertexai.generative_models import GenerativeModel
from openai import AzureOpenAI
from fastapi.responses import JSONResponse
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
import jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SECRET="!az$y#5%"

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


max_new_tokens = 512
prompt_template = "<s>[INST] {prompt} [/INST]"
config_path = "model/config.json"
vertex_config_path = "model/vertex_config.json"
azure_config_path = "model/azure_config.json"
email_config_path = "model/email_config.json"

class Message(BaseModel):
    userInput: str
    model: str
    temperature: float

class Response(BaseModel):
    response: str

class ModelConfig(BaseModel):
    temp: float
    model: str
    gpu: bool
    agent: str

def load_config():
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "temperature": 0.5,
            "model": "",
            "model_path": "",
            "gpu": False
        }
    
def load_vertex_config():
    if os.path.exists(vertex_config_path):
        with open(vertex_config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "projectId": "",
            "modelInput": "gemini-1.0-pro-002",
            "region": "",
        }
    
def load_azure_config():
    if os.path.exists(azure_config_path):
        with open(azure_config_path, "r") as f:
            return json.load(f)
    else:
        return {
            "apikey": "",
            "modelInput": "gemini-1.0-pro-002",
            "version": "",
            "endpoint": ""
        }
def load_email_config():
    if os.path.exists(email_config_path):
        with open(email_config_path, "r") as f:
            return json.load(f)
    else:
        return{
            "smtp_server": "",
            "smtp_port": "",
            "smtp_username": "",
            "smtp_password": "",
            "sender_email": "",
            "recipient_emails": "",
            "user_creation" : "",
            "user_deletion" : "",
            "feedback" : "",
            "password_change" : "",
            "model_change" : "",
            "feedback_email_subject": "Feedback received",
            "password_change_email_subject": "Password changed",
            "model_change_email_subject": "Model changed",
            "user_creation_email_subject": "New user added to Database",
            "user_deletion_email_subject": "User deleted from Database",
            "user_creation_email_body": "Dear admin, \n A new user has been added to the database, kindly take a note of the same.",
            "user_deletion_email_body": "Dear admin, \n A user has been deleted from the database, kindly take a note of the same.",
            "feedback_email_body": "Dear admin, \n Feedback received for a response",
            "password_change_email_body": "Your password has been changed",
            "model_change_email_body": "The global model configuration has changed, kindly take a note of the same.",
        }
def save_config(config):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
def save_azure_config(config):
    with open(azure_config_path, "w") as f:
        json.dump(config, f, indent=4)
def save_vertex_config(config):
    with open(vertex_config_path, "w") as f:
        json.dump(config, f, indent=4)
def save_emails_config(config):
    with open(email_config_path, "w") as f:
        json.dump(config, f, indent=4)

# Database setup function
def setup_database():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        fullname TEXT NOT NULL,
        role TEXT, 
        profilepic TEXT,
        designation TEXT,
        notifications TEXT,
        JWT TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS monitoring (
        logs TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS organization (
        name TEXT,
        mainlogo TEXT,
        chatlogo TEXT,
        about TEXT,
        chatdisclaimer TEXT
    )''')

    conn.commit()
    conn.close()


config = load_config()

def sanitize_email(email):
    # Replace invalid characters with underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', email)

@app.websocket("/model_config")
async def websocket_model_config(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print("Received model config:", data)
            is_vertex_model = "projectId" in data or "region" in data
            is_azure_model = "key" in data  or "version" in data or "endpoint" in data
            if is_vertex_model:
                vertex_config = {
                    "project_id" : data["projectId"],
                    "model" : data["modelInput"],
                    "region" : data["region"]
                }
                save_vertex_config(vertex_config)
            if is_azure_model:
                azure_config = {
                    "apikey" : data["key"],
                    "version" : data["version"],
                    "endpoint" : data["endpoint"],
                    "modelInput" : data["modelInput"]
                }
                save_azure_config(azure_config)
            else:

                model_config = load_config()
                temp = model_config["temperature"]
                model = model_config["model"]
                gpu = model_config["gpu"]
                
                if model != data["model"] or temp != data["temperature"]:
                    model_config["model"] = data["model"]
                    model_config["temperature"] = data["temperature"]

                    model_directory = "model"
                    for file in os.listdir(model_directory):
                        if file.endswith('.gguf') and config["model"].lower() in file:
                            config["model_path"] = os.path.join(model_directory, file)
                            break

                    save_config(config)

                model_kwargs = {"n_gpu_layers": -1 if gpu else 0}
                # llm = LlamaCPP(
                #     model_path=config["model_path"],
                #     temperature=config["temperature"],
                #     max_new_tokens=max_new_tokens,
                #     context_window=3900,
                #     model_kwargs=model_kwargs,
                #     verbose=False,
                # )
            await websocket.send_json({"status": "success", "message": "Model configuration updated."})

    except Exception as e:
        print(e)
    # finally:
    #     await websocket.close()


    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            print("ws route")
            user_input = data["userInput"]
            print(user_input)
            if user_input.lower() == "exit":
                print("Exiting chat.")
                break

            prompt = prompt_template.format(prompt=user_input)
            model_kwargs = {"n_gpu_layers": -1 if config["gpu"] else 0}
            llm = LlamaCPP(
                model_path=config["model_path"],
                temperature=config["temperature"],
                max_new_tokens=max_new_tokens,
                context_window=3900,
                model_kwargs=model_kwargs,
                verbose=False,
            )
            response_iter = llm.stream_complete(prompt)

            for response in response_iter:
                await websocket.send_text(response.delta)
                await asyncio.sleep(0)
                if websocket.client_state.name != 'CONNECTED':
                    break

            await websocket.close()
            

    except Exception as e:
        print(e)
    # finally:
    #     await websocket.close()


@app.websocket("/available_agents")
async def agentinfo(websocket: WebSocket):
    await websocket.accept()
    agents = os.listdir('db')
    dict = {
        'agentinfo': agents
    }
    await websocket.send_json(dict)

@app.websocket("/agent")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_config()
        model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
        llm = LlamaCPP(
            model_path=config["model_path"],
            temperature=config["temperature"],
            max_new_tokens=max_new_tokens,
            context_window=3900,
            model_kwargs=model_kwargs,
            verbose=False,
        )
        while True:
            data = await websocket.receive_json()
            print(data)
            print("agent route")
            user_input = data["userInput"]
            
            if user_input.lower() == "exit":
                print("Exiting chat.")
                break

            agent = data['agent']
            persist_directory = os.path.join('db', agent)
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

            docs = db.similarity_search(user_input, k=3)
            context = docs[0].page_content
            prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
            prompt = prompt_template.format(context=context, prompt=user_input)

            # model_kwargs = {"n_gpu_layers" : -1 if config["gpu"] else 0}
            # llm = LlamaCPP(
            #     model_path=config["model_path"],
            #     temperature=config["temperature"],
            #     max_new_tokens=max_new_tokens,
            #     context_window=3900,
            #     model_kwargs=model_kwargs,
            #     verbose=False,
            # )

            response_iter = llm.stream_complete(prompt)

            for response in response_iter:
                await websocket.send_text(response.delta)
                await asyncio.sleep(0)


                save_config(config)
            await websocket.close()

        
    except Exception as e:
        print(e)
    # finally:
    #     await websocket.close()

@app.websocket("/vertex")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_vertex_config()
        while True:
            data = await websocket.receive_json()
            print(data)
            print("vertex route")
            prompt = data["userInput"]
            
            if prompt.lower() == "exit":
                print("Exiting chat.")
                break

            agent = data['agent']
            projectid=config["project_id"]
            region=config["region"]
            model=config["model"]
            vertexai.init(project=projectid, location=region)
            multimodal_model = GenerativeModel(model_name=model)
            if agent == "None":
                response = multimodal_model.generate_content(prompt)
                await websocket.send_text(response.text)
                await websocket.close()
            else:

                persist_directory = os.path.join('db', agent)
                embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

                docs = db.similarity_search(prompt, k=3)
                context = docs[0].page_content
                prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
                prompt = prompt_template.format(context=context, prompt=prompt)
                response = multimodal_model.generate_content(prompt)
                await websocket.send_text(response.text)
                await websocket.close()
           

    except Exception as e:
        print(e)
    # finally:
    #     await websocket.close()

@app.websocket("/azure")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        config=load_azure_config()

        while True:
            data = await websocket.receive_json()
            print(data)
            print("azure route")
            prompt = data["userInput"]
            
            if prompt.lower() == "exit":
                print("Exiting chat.")
                break

            agent = data['agent']
            key=config['apikey']
            version=config['version']
            model=config['modelInput']
            endpoint=config['endpoint']


            client = AzureOpenAI(
                api_key = (key),
                api_version = version,
                azure_endpoint = (endpoint)
            )

            if agent == "None":
                response = client.chat.completions.create(
                    model=model, # model = "deployment_name".
                    messages=[
                        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                        {"role": "user", "content": prompt}
                        
                    ]
                )
                for choice in response.choices:
                    await websocket.send_text(choice.message.content)
                    await websocket.close()
            else:
                persist_directory = os.path.join('db', agent)
                if os.path.exists(persist_directory):
                    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
                    db = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
                    docs = db.similarity_search(prompt, k=3)
                    context = docs[0].page_content
                    prompt_template = "You are a friendly assistant, who gives context aware responses on user query. Kindly analyse the provided context and give proper response\n   Context: {context}\n query:<s>[INST] {prompt} [/INST]"
                    prompt = prompt_template.format(context=context, prompt=prompt)
                    response = client.chat.completions.create(
                            model=model, # model = "deployment_name".
                            messages=[
                                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                                {"role": "user", "content": prompt}
                                
                            ]
                        )
                    for choice in response.choices:
                        await websocket.send_text(choice.message.content)
                    await websocket.close()
                        


           

    except Exception as e:
        print(e)
    # finally:
    #     await websocket.close()


# class RequestData(BaseModel):
#     agent: str
#     file: UploadFile
@app.post("/create_agent")
async def upload_file(name: str = Form(...),file: UploadFile = File(...)):
        try:
            agentname = name
            uploaded_file = file
            # Process the uploaded file
            # Example: Save the file locally
            if not os.path.exists("uploads"):
                os.mkdir("uploads")
            file_path = f"uploads/{uploaded_file.filename}"
            with open(file_path, "wb") as file_object:
                file_object.write(await uploaded_file.read())
            persist_directory = 'db'
            doc_path = os.path.normpath(file_path)
            agent_directory = os.path.join(persist_directory, agentname)
            if not os.path.exists(agent_directory):
                os.makedirs(agent_directory)

            # Load the document
            if doc_path.endswith(".csv"):
                loader = CSVLoader(doc_path)
            elif doc_path.endswith(".pdf"):
                loader = PDFMinerLoader(doc_path)
            elif doc_path.endswith(".docx"):
                loader = TextLoader(doc_path)
            else:
                raise ValueError("Unsupported file format. Supported formats are CSV, PDF, and DOCX.")

            documents = loader.load()

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=500)
            texts = text_splitter.split_documents(documents)

            # Create embeddings
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            # Create ChromaDB and store document IDs
            db = Chroma.from_documents(texts, embeddings, persist_directory=agent_directory)
            db.persist()

            doc_ids_path = os.path.join(agent_directory, f"{agentname}_docids.txt")

            # Store document IDs in a file
            with open(doc_ids_path, "a") as f:
                for text_id, _ in enumerate(texts):
                    document_id = f"doc_{text_id}"
                    f.write(f"{document_id}\n")
            return JSONResponse(content={"agentname": name, "message": "agent created successfully"}) 
        



        except Exception as e:
            print(e)

@app.websocket("/configdata")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        print(data)
        if data == "Azure":
            azure_config=load_azure_config()
            await websocket.send_json(azure_config)
        elif data == "Vertex":
            vertex_config=load_vertex_config()
            await websocket.send_json(vertex_config)
        else:
            config=load_config()
            await websocket.send_json(config)

    except Exception as e:
        print(e)
    finally:
        await websocket.close()


@app.post("/signup")
async def signup(request: Request):
    data = await request.json()
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    profilepic = data.get('profilepic')
    designation = data.get('designation')
    notifications = data.get('notifications')

    if not email or not password or not fullname:
        raise HTTPException(status_code=400, detail="Required fields are missing")

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Check if '@' is in the email to distinguish signup from user creation
    if '@' in email:
        try:
            cursor.execute('''
                INSERT INTO users (email, password, fullname, role, profilepic, designation, notifications)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (email, hashlib.sha256(password.encode()).hexdigest(), fullname, role, profilepic, designation, notifications))

            token = jwt.encode({'email': email}, SECRET, algorithm='HS256')

            # Store JWT token in the database
            cursor.execute('''
                UPDATE users SET jwt = ? WHERE email = ?
            ''', (token, email))

            sanitized_table_name = sanitize_email(email)
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {sanitized_table_name} (
                    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    messageheader TEXT,
                    chats TEXT                   
                )
            ''')
            conn.commit()
        
            response = {'message': 'User signed up successfully!'}
        except sqlite3.IntegrityError:
            response = {'message': 'Username already exists!'}
        except Exception as e:
            response = {'message': 'Error occurred while signing up'}
            print(e)
    else:
        response = {'message': 'Email format is not correct'}
        raise HTTPException(status_code=400, detail=response)

    conn.close()
    return response

# Route for user login
@app.route('/login', methods=['POST'])
async def login(request: Request):
    data = await request.json()
    email = data['email']
    password = data['password']

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, fullname, role FROM users WHERE email = ? AND password = ?
    ''', (email, hashed_password))

    user = cursor.fetchone()

    if user:
        print(user)
        user_id = user[0]
        fullname = user[1]
        role = user[2]
        token = jwt.encode({'email': email, 'role': user[2]}, SECRET, algorithm='HS256')
        print(fullname, user_id)
        response = {'message': f"Welcome, {fullname}!","status": True, "token": token, "role": role }
    else:
        response = {'message': 'Invalid username or password.'}

    conn.close()
    return JSONResponse(content=response)

def is_user(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_role = payload.get("role")
        if user_role and user_role.lower() == 'admin':
            return True
        else:
            return False
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/check_user")
def check_user(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = authorization.split(" ")[1]  # Assuming the header is "Bearer <token>"
    
    if is_user(token):
        return {"status": "true"}
    else:
        raise HTTPException(status_code=403, detail="You are not authorized to access this page")

@app.post('/newchat')
async def update_chat_history(request: Request):
    data = await request.json()
    print(data)
    user_email = data['userEmail']
    message_header = data['messageheader']
    chats = data['chats']
    
    # Convert the chats array to a JSON string
    chats_json = json.dumps(chats)

    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Execute query to insert data into the specified user's table
        cursor.execute(f'''
            INSERT INTO {user_email} (messageheader, chats)
            VALUES (?, ?)
        ''', (message_header, chats_json))

        cursor.execute(f'''
            SELECT chat_id FROM {user_email}
            WHERE messageheader = ?
        ''', (message_header,))
        
        # Fetch the chat_id
        chat_id = cursor.fetchone()[0]

        # Commit the transaction
        conn.commit()

        # Close the database connection
        conn.close()

        return JSONResponse(content={'message': 'Chat history updated successfully.', 'chat_id': chat_id})
    except Exception as e:
        # Rollback changes if an error occurs
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=f'Error updating chat history: {str(e)}')
    

@app.post('/fetchchat')
async def fetch_chat_history(request: Request):
    data = await request.json()
    print(data)
    user_email = data['userEmail']
    chat_id = data['chat_id']

    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Execute query to fetch chat history based on userEmail and chat_id
        cursor.execute(f'''
            SELECT chats FROM {user_email}
            WHERE chat_id = ?
        ''', (chat_id,))
        
        # Fetch the chat history
        chat_history = cursor.fetchone()

        if chat_history:
            # Parse the chat history from JSON
            chat_history_json = json.loads(chat_history[0])
            return JSONResponse(content={'chat': chat_history_json})
        else:
            raise HTTPException(status_code=404, detail='Chat history not found.')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f'Error fetching chat history: {str(e)}')
    finally:
        # Close the database connection
        conn.close()

@app.post('/updatechat')
async def update_chat_history(request: Request):
    data = await request.json()
    user_email = data['userEmail']
    chat_id = data['chat_id']
    updated_chats = data['chats']
    
    # Convert the updated chats array to a JSON string
    updated_chats_json = json.dumps(updated_chats)

    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        # Execute query to update the chat data for the specified chat_id
        cursor.execute(f'''
            UPDATE {user_email}
            SET chats = ?
            WHERE chat_id = ?
        ''', (updated_chats_json, chat_id))

        # Check if any rows were affected
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Chat not found.")
        
        # Commit the transaction
        conn.commit()

        return JSONResponse(content={'message': 'Chat history updated successfully.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error updating chat history: {str(e)}')
    finally:
        # Close the database connection
        conn.close()

def get_start_of_day(date):
    return date.replace(hour=0, minute=0, second=0, microsecond=0)

def get_date_x_days_ago(days):
    return get_start_of_day(datetime.now() - timedelta(days=days))

@app.post('/fetchchatsidebar')
async def fetch_chat_sidebar(request: Request):
    data = await request.json()
    print(data)
    user_email = data.get('userEmail')

    if not user_email:
        raise HTTPException(status_code=400, detail='userEmail is required')

    email_safe = user_email.replace('.', '_').replace('@', '_')
    today_start = get_start_of_day(datetime.now())
    yesterday_start = get_date_x_days_ago(1)

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f'''
            SELECT chat_id, messageheader, timestamp
            FROM {email_safe}
        ''')

        chats = cursor.fetchall()

        today_chats = []
        yesterday_chats = []
        previous_chats = []


        for chat in chats:
            chat_id, message_header, timestamp = chat
            chat_date = datetime.fromisoformat(timestamp)

            if chat_date >= today_start:
                today_chats.append({
                    'chat_id': chat_id,
                    'message_header': message_header,
                    'timestamp': timestamp
                })
            elif chat_date >= yesterday_start and chat_date < today_start:
                yesterday_chats.append({
                    'chat_id': chat_id,
                    'message_header': message_header,
                    'timestamp': timestamp
                })
            else:
                previous_chats.append({
                    'chat_id': chat_id,
                    'message_header': message_header,
                    'timestamp': timestamp
                })

        return JSONResponse(content={
            'today': today_chats,
            'yesterday': yesterday_chats,
            'previous': previous_chats
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error fetching chat sidebar: {str(e)}')
    finally:
        conn.close()

@app.route('/fetch_user_details', methods=['POST'])
async def fetch_user_details(request: Request):
    data = await request.json()
    email = data['email']

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT email, fullname, role, profilepic, designation, notifications, JWT FROM users WHERE email = ?
    ''', (email,))

    user = cursor.fetchone()

    if user:
        email, fullname, role, profilepic, designation, notifications, JWT = user
        response = {
            'status': True,
            'email': email,
            'fullname': fullname,
            'role': role,
            'profilepic': profilepic,
            'designation': designation,
            'notifications': notifications,
            "JWT":JWT
        }
    else:
        response = {'status': False, 'message': 'User not found'}

    conn.close()
    return JSONResponse(content=response)


@app.get("/fetch_users")
async def fetch_non_admin_users():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT email, fullname, role, profilepic, designation, notifications 
    FROM users 
    WHERE role != "admin" AND role != "Admin"
    ''')

    users = cursor.fetchall()

    user_list = [
        {
            "email": user[0],
            "fullname": user[1],
            "role": user[2],
            "profilepic": user[3],
            "designation": user[4],
            "notifications": user[5]
        }
        for user in users
    ]

    conn.close()
    return JSONResponse(content={"status": True, "users": user_list})


class UpdateUserRequest(BaseModel):
    email: str
    password: str
    fullname: str
    role: str
    profilepic: str
    designation: str
    notifications: str

@app.post('/update_user')
async def update_user(request: Request):
    data = await request.json()
    print(data)
    email = data.get('email')

    # Validate that email is provided
    if not email:
        raise HTTPException(status_code=400, detail="Email is required to update user information.")
    
    update_fields = {
        'password': data.get('password'),
        'fullname': data.get('fullname'),
        'role': data.get('role'),
        'profilepic': data.get('profilepic'),
        'designation': data.get('designation'),
        'notifications': data.get('notifications')
    }
    
    # Filter out None values from the update_fields dictionary
    update_fields = {k: v for k, v in update_fields.items() if v is not None}
    
    # Validate that at least one field to update is provided
    if not update_fields:
        raise HTTPException(status_code=400, detail="At least one field is required to update user information.")
    
    set_clause = ', '.join([f"{k} = ?" for k in update_fields.keys()])
    values = list(update_fields.values())
    values.append(email)  # Add email to the end of the values list for the WHERE clause
    
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"UPDATE users SET {set_clause} WHERE email = ?", values)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found.")
        
        response = {'message': 'User information updated successfully.', 'status': True}
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()
    
    return JSONResponse(content=response)

@app.post("/delete_user")
async def delete_user(request: Request):
    data = await request.json()
    email = data.get('email')

    if not email:
        raise HTTPException(status_code=400, detail="Email not provided")

    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    user_exists = cursor.fetchone()

    if not user_exists:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user
    cursor.execute('DELETE FROM users WHERE email = ?', (email,))
    sanitized_table_name = sanitize_email(email)
    cursor.execute(f'DROP TABLE IF EXISTS {sanitized_table_name}')
    conn.commit()
    conn.close()

    return {"message": "User deleted successfully"}


@app.post('/update_org_details')
async def add_orgData(request: Request):
    data = await request.json()
    
    # Extract values from the JSON data
    name = data.get('name')
    mainlogo = data.get('mainlogo')
    chatlogo = data.get('chatlogo')
    about = data.get('about')
    chatdisclaimer = data.get('chatdisclaimer')
    
    # Validate that all required fields are present
    if not all([name, mainlogo, chatlogo, about, chatdisclaimer]):
        raise HTTPException(status_code=400, detail="All fields are required: name, mainlogo, chatlogo, about, chatdisclaimer")
    
    # Connect to the SQLite database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    
    try:
        # Check if any data exists in the organization table
        cursor.execute("SELECT COUNT(*) FROM organization")
        row_count = cursor.fetchone()[0]
        
        if row_count == 0:
            # If no data exists, insert new row
            cursor.execute("""
                INSERT INTO organization (name, mainlogo, chatlogo, about, chatdisclaimer)
                VALUES (?, ?, ?, ?, ?)
            """, (name, mainlogo, chatlogo, about, chatdisclaimer))
        else:
            # If data exists, update the existing row
            cursor.execute("""
                UPDATE organization
                SET name = ?, mainlogo = ?, chatlogo = ?, about = ?, chatdisclaimer = ?
            """, (name, mainlogo, chatlogo, about, chatdisclaimer))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed: " + str(e))
    finally:
        conn.close()
    
    return {"message": "Organization details updated successfully"}


@app.get("/get_org_details")
async def get_org_details():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()

    # try:
    cursor.execute("SELECT name, mainlogo, chatlogo, about, chatdisclaimer FROM organization LIMIT 1")
    result = cursor.fetchone()

    if result:
        org_details = {
            "name": result[0],
            "mainlogo": result[1],
            "chatlogo": result[2],
            "about": result[3],
            "chatdisclaimer": result[4]
        }
        return org_details
        conn.close()
    else:
        raise HTTPException(status_code=404, detail="Organization details not found")
    # except Exception as e:
        # raise HTTPException(status_code=500, detail="Database query failed: " + str(e))
    # finally:

class SMTPParams(BaseModel):
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender_email: EmailStr
    recipient_emails: list[EmailStr]
    user_creation : bool
    user_deletion : bool
    feedback : bool
    password_change : bool
    model_change : bool

@app.websocket("/send-email")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            smtp_params = SMTPParams(**json.loads(data))
            save_emails_config(smtp_params)

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = smtp_params.sender_email
            msg['To'] = ", ".join(smtp_params.recipient_emails)
            msg['Subject'] = smtp_params.subject

            # Attach the body with the msg instance
            msg.attach(MIMEText(smtp_params.body, 'plain'))

            try:
                # Connect to the server
                server = smtplib.SMTP(smtp_params.smtp_server, smtp_params.smtp_port)
                server.starttls()  # Secure the connection
                server.login(smtp_params.smtp_username, smtp_params.smtp_password)

                # Send the email
                server.sendmail(smtp_params.sender_email, smtp_params.recipient_emails, msg.as_string())
                server.quit()

                await websocket.send_text("Email sent successfully")
            except Exception as e:
                await websocket.send_text(f"Failed to send email: {str(e)}")
    except WebSocketDisconnect:
        print("Client disconnected")


def main():
    import uvicorn
    setup_database()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()