import io
from typing import TypedDict, overload
import easyocr
import numpy


@overload
def get_text_coordinates(image: str, lang=["en"]) -> list["EasyOCRMeta"]: ...


@overload
def get_text_coordinates(image: bytes, lang=["en"]) -> list["EasyOCRMeta"]: ...


@overload
def get_text_coordinates(image: numpy.ndarray, lang=["en"]) -> list["EasyOCRMeta"]: ...


@overload
def get_text_coordinates(image: io.BytesIO, lang=["en"]) -> list["EasyOCRMeta"]: ...


class EasyOCRMeta(TypedDict):
    text: str
    confidence: float
    top_left: tuple
    bottom_right: tuple


def get_text_coordinates(
    image: str | bytes | numpy.ndarray | io.BytesIO, lang=["en"]
) -> list[EasyOCRMeta]:

    reader = easyocr.Reader(lang)  # Initialize the EasyOCR reader for English
    if isinstance(image, bytes):
        image = io.BytesIO(image)

    result = reader.readtext(image)

    coordinates = []
    for detection in result:
        top_left = tuple(detection[0][0])
        bottom_right = tuple(detection[0][2])
        text = detection[1]
        confidence = detection[2]
        coordinates.append(
            {
                "text": text,
                "confidence": confidence,
                "top_left": top_left,
                "bottom_right": bottom_right,
            }
        )

    return coordinates
