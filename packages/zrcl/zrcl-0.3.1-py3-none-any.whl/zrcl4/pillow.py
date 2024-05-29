import base64
from PIL import Image
import io


def load_base64_img(string: str):

    if string.startswith("data:image/png;base64,"):
        string = string[22:]
    return Image.open(io.BytesIO(base64.b64decode(string)))
