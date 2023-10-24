# Following codes are BASED on a Medium blog.
# See https://nayakpplaban.medium.com/ask-questions-to-your-images-using-langchain-and-python-1aeb30f38751 for details.
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.output_parsers import NumberedListOutputParser, MarkdownListOutputParser
from src.image_tools import ImageCaptionTool, ObjectDetectionTool


def image_to_music(image_path: str) -> tuple:
    """
    入力として受け取った画像に対し、画像の雰囲気に合った音楽名を返す関数。\n
    BLIPを利用した画像キャプションツールを使える LLM にプロンプトを入力し、返答させることで実装されている。
    この際の LLM の回答の全文が第2返数 `response` である。

    Parameter
    ---------
    image_path: str
        入力画像ファイルのパス。

    Returns
    ----
    music_list: list
        List of music keywords. Each music keywords is given as str.
    response: str
        Final response from LLM agent.
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
        temperature=0.5,
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

    music_list = response_to_list(response)

    return music_list, response


def response_to_list(response: str) -> list:
    """
    LLMの回答文章を受け取り、そこに記述された数字付き箇条書きの部分のみをリスト化して返す関数。

    Parameter
    ---------
    response: str

    Return
    ------
    list of music. Each music is represented by str, may contain artist name.
    """

    # See if any numbered list exists in response
    output_parser = NumberedListOutputParser()
    result = output_parser.parse(response)

    if not result:
        output_parser = MarkdownListOutputParser()
        result = output_parser.parse(response)

    print(result)
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

        result = image_to_music(filename)
        print(result)

        spec_report.append(len(result))

    print(spec_report)