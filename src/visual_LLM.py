# import os
# import openai
from tempfile import NamedTemporaryFile
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from image_tools import ImageCaptionTool, ObjectDetectionTool

from langchain.output_parsers import CommaSeparatedListOutputParser, NumberedListOutputParser


def image_to_text(image=None) -> str:
    """
    入力として受け取った画像に対し、画像の雰囲気に合った音楽名を返す関数。
    """
    #initialize the agent
    tools = [ImageCaptionTool(), ObjectDetectionTool()]

    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    llm = ChatOpenAI(
        openai_api_key="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",
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
    user_question = """Please suggest some names of music pieces which fit to this image."""
    
    response = agent.run(f'{user_question}, this is the image path: {image_path}')

    print(user_question)
    print(response)

    return response


def parser(response: str) -> list:

    # output_parser = CommaSeparatedListOutputParser()
    output_parser = NumberedListOutputParser()
    result = output_parser.parse(response)
    return result


if __name__ == "__main__":

    # response = image_to_text()
    response = """
Based on the image description, some music pieces that could fit the scene are: 

1. Romantic Dinner by Kevin MacLeod
2. Jazz Restaurant by Music For Video
3. Elegant Dinner Jazz by Background Music For Video
4. Fine Dining by Music For Video
5. Smooth Jazz Dinner Party by Background Music For Video

These are just a few suggestions, and the choice of music ultimately depends on the mood and atmosphere you want to create. Enjoy your music selection!
"""

    result = parser(response)
    print(result)