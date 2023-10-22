import os
import openai
from tempfile import NamedTemporaryFile
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from image_tools import ImageCaptionTool, ObjectDetectionTool

openai_api_key = "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"


def image_to_text(image=None) -> str:
    """
    入力として受け取った画像に対し、画像の雰囲気に合った音楽名を返す関数。
    """
    #initialize the gent
    tools = [ImageCaptionTool(), ObjectDetectionTool()]

    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    llm = ChatOpenAI(
        openai_api_key= openai_api_key,
        temperature=0,
        model_name="gpt-3.5-turbo"
    )

    agent = initialize_agent(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=llm,
        max_iterations=5,
        verbose=True,
        memory=conversational_memory,
        early_stopping_method='generate'
    )

    # Prompt
    image_path = "/Users/naoki/github/Rutilea/img/suits_dining_scene.jpg"
    # user_question = "generate a caption for this iamge?"
    user_question = "Tell me the atmosphere of this image."
    response = agent.run(f'{user_question}, this is the image path: {image_path}')
    print(response)

    return response


if __name__ == "__main__":

    image_to_text()