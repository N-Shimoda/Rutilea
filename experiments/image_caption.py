from langchain.document_loaders import ImageCaptionLoader
from langchain.indexes import VectorstoreIndexCreator
from PIL import Image
import requests

# images
list_image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hyla_japonica_sep01.jpg/260px-Hyla_japonica_sep01.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Tibur%C3%B3n_azul_%28Prionace_glauca%29%2C_canal_Fayal-Pico%2C_islas_Azores%2C_Portugal%2C_2020-07-27%2C_DD_14.jpg/270px-Tibur%C3%B3n_azul_%28Prionace_glauca%29%2C_canal_Fayal-Pico%2C_islas_Azores%2C_Portugal%2C_2020-07-27%2C_DD_14.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Thure_de_Thulstrup_-_Battle_of_Shiloh.jpg/251px-Thure_de_Thulstrup_-_Battle_of_Shiloh.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Passion_fruits_-_whole_and_halved.jpg/270px-Passion_fruits_-_whole_and_halved.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Messier83_-_Heic1403a.jpg/277px-Messier83_-_Heic1403a.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/2022-01-22_Men%27s_World_Cup_at_2021-22_St._Moritz%E2%80%93Celerina_Luge_World_Cup_and_European_Championships_by_Sandro_Halank%E2%80%93257.jpg/288px-2022-01-22_Men%27s_World_Cup_at_2021-22_St._Moritz%E2%80%93Celerina_Luge_World_Cup_and_European_Championships_by_Sandro_Halank%E2%80%93257.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Wiesen_Pippau_%28Crepis_biennis%29-20220624-RM-123950.jpg/224px-Wiesen_Pippau_%28Crepis_biennis%29-20220624-RM-123950.jpg",
]

# loader
loader = ImageCaptionLoader(path_images=list_image_urls)
list_docs = loader.load()
list_docs

Image.open(requests.get(list_image_urls[0], stream=True).raw).convert("RGB")

# index
index = VectorstoreIndexCreator().from_loaders([loader])

query = "What's the painting about?"
index.query(query)