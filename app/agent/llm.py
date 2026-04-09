import os

from langchain.chat_models import init_chat_model

from app.conf.app_config import app_config

from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)


llm = init_chat_model(model=app_config.llm.model_name,
                      model_provider="openai",
                      base_url=app_config.llm.base_url,
                      api_key=os.getenv("OPENAI_API_KEY"),
                      temperature=0)

if __name__ == '__main__':
    print(llm.invoke("你好").content)
