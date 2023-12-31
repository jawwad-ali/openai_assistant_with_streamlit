from openai import OpenAI
from openai.types.beta import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads.thread_message import ThreadMessage
from openai.types.beta.threads.run import Run

from dotenv import load_dotenv,find_dotenv
import time
from typing import Any

# Single Message
class MessageItem:
    def __init__(self ,role:str ,content:str | Any):
        self.role:str = role
        self.content:str = content

class OpenAIBot:
    def __init__(self , name:str , instructions:str , fileFromUI:str, model:str = "gpt-3.5-turbo-1106" ) -> None:
        # loading openai secret keys from os
        load_dotenv(find_dotenv()) 

        # Initializing Openai Client
        self.client:OpenAI = OpenAI()

        # class constructor variables 
        self.name:str = name
        self.instructions:str = instructions
        self.model:str = model 
        self.file = fileFromUI 

        self.file = self.client.files.create(
            file = open(f"temp/{self.file}" , "rb"),
            purpose="assistants" 
        ) 
        print("Assistant File",self.file)

        # Creating Assistant
        self.assistant = self.client.beta.assistants.create(
            name = self.name,
            model = self.model,
            instructions = self.instructions,
            tools = [{"type": "retrieval"}],
            file_ids = [self.file.id]
        )

        # Creating Thread
        self.thread:Thread = self.client.beta.threads.create()
        
        # Message generated by the model
        self.messages:list[MessageItem] = [] 
    
    def get_name(self):
        return self.name

    def get_instructions(self):
        return self.instructions

    def get_model(self):
        return self.model
    
    def get_File(self):
        print("fileFROMUI",self.file)
        return self.file

    def send_message(self , message:str):
        latest_message: ThreadMessage = self.client.beta.threads.messages.create(
            thread_id= self.thread.id,
            role= "user", 
            content= message
        )

        self.latest_run:Run = self.client.beta.threads.runs.create(
            thread_id = self.thread.id,
            assistant_id = self.assistant.id,
            instructions = self.instructions
        )

        self.addMessage(MessageItem(role="user", content=message))

    def isCompleted(self) -> bool:
        while self.latest_run.status != "completed":
            print("Going to sleep")
            time.sleep(1)

            self.latest_run: Run = self.client.beta.threads.runs.retrieve(
                thread_id = self.thread.id,
                run_id = self.latest_run.id
            )

        return True

    # Getting the message(response) from the model
    def get_latest_response(self)->MessageItem:
        messages = self.client.beta.threads.messages.list(
            thread_id = self.thread.id
        )
        m = MessageItem(messages.data[0].role , messages.data[0].content[0].text.value)
        self.addMessage(m)
        return m 
    
    def getMessages(self)->list[MessageItem]:
        return self.messages
    
    def addMessage(self, message: MessageItem)->None: 
        self.messages.append(message)

    # Delete Chat
    def delete_chat_history(self):
        self.messages:list[MessageItem] = []