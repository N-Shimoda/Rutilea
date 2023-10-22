# import os
# import openai
from tempfile import NamedTemporaryFile
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from image_tools import ImageCaptionTool, ObjectDetectionTool

from langchain.output_parsers import NumberedListOutputParser


def image_to_text(image_path: str) -> list:
    """
    入力として受け取った画像に対し、画像の雰囲気に合った音楽名を返す関数。

    Returns
    ----
    List of music. Each music is given as str.
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
    user_question = "Explain the atmosphere of this image " \
                    "and suggest me some music pieces which fit to the scene " \
                    "in a list format."
    
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
    """
    Spec-examination for `image_to_music`.
    See how many music pieces it can return for each picture.
    """

    spec_report = []

    image_list = [
        "/Users/naoki/Desktop/img/jujutsu.jpg", # 0
        "/Users/naoki/Desktop/img/kix_terminal.jpg",
        "/Users/naoki/Desktop/img/lab_gathering.jpg",
        "/Users/naoki/Desktop/img/mohammad-ali-niksejel-KR9ScsVrZVQ-unsplash.jpg",  # 3
        "/Users/naoki/Desktop/img/rugby_boys.jpg",
        "/Users/naoki/Desktop/img/seongho-jang-WIWsRmsHN1s-unsplash.jpg",
        "/Users/naoki/Desktop/img/singer_youtube.png",  # 6
        "/Users/naoki/Desktop/img/star_wars.jpg",
        "/Users/naoki/Desktop/img/suits_dining_scene.jpg",
        "/Users/naoki/Desktop/img/wedding_party.jpg"
    ]

    for filename in image_list:

        response = image_to_text(filename)
        result = parser(response)
        print(result)

        spec_report.append(len(result))

    print(spec_report)