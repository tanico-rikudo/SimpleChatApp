from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

class Chat:
    def __init__(self, openai_api_key, model_name):
        self.store = {}
        self.chat_model = self.gen_chat_model(openai_api_key, model_name)
        self.runnable_with_history = None
        self.system_prompt = ""
        
    def gen_chat_model(openai_api_key, model_name):
        self.chat_model = ChatOpenAI(
                openai_api_key=openai_api_key,
                model=model_name
        )
        
    def set_system_prompt(self, prompt):
        return self.system_prompt = prompt
    
    def create_prompt_template(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt), 
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def gen_runnable(self, session_id):
        prompt_template = self.create_prompt_template()
        runnable = prompt_template | self.chat_model
        runnable_with_history = RunnableWithMessageHistory(
            runnable,
            lambda _:self.get_session_history(session_id),
            input_messages_key="input",
            history_messages_key="history",
        )
        return runnable_with_history
    
    def run_conversation(self, session_id: str, user_input: str):
        if self.runnable_with_history is None:
            self.runnable_with_history = self.gen_runnable(session_id)
        output = self.runnable_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}},
        )
        return output.content
