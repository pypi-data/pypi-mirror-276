import pyscreeze
import typing

"""
provides easy import
"""


class easyimport:
    from pyscreeze import (  # noqa: E402
        center as center,
        locateAll as locateAll,
        locateAllOnScreen as locateAllOnScreen,
        locateCenterOnScreen as locateCenterOnScreen,
        locateOnScreen as locateOnScreen,
        locateOnWindow as locateOnWindow,
        pixel as pixel,
        pixelMatchesColor as pixelMatchesColor,
        screenshot as screenshot,
    )


def screenshot():
    return pyscreeze._screenshot_win32(allScreens=True)


"""
attempt to import two methods
"""
try:
    pyscreeze._locateAll_pillow

    def locateAllPillow(
        needleImage,
        haystackImage,
        grayscale=None,
        limit=None,
        region=None,
        step=1,
        confidence=None,
    ):
        return pyscreeze._locateAll_pillow(needleImage, haystackImage, grayscale, limit, region, step, confidence)  # type: ignore

except AttributeError:
    locateAllPillow = None  # type: ignore

try:
    pyscreeze._locateAll_opencv

    def locateAllOpenCV(
        needleImage,
        haystackImage,
        grayscale=None,
        limit=None,
        region=None,
        step=1,
        confidence=None,
    ):
        return pyscreeze._locateAll_opencv(needleImage, haystackImage, grayscale, limit, region, step, confidence)  # type: ignore

except AttributeError:
    locateAllOpenCV = None  # type: ignore


def locate(
    needleImage,
    haystackImage,
    _algo: typing.Literal["cv2", "pillow"] = "pillow",
    **kwargs,
):
    locallocateAll = locateAllOpenCV if _algo == "cv2" else locateAllPillow
    if locallocateAll is None:
        locallocateAll = locateAllPillow

    if locallocateAll is locateAllPillow:
        kwargs.pop("confidence", None)

    kwargs["limit"] = 1
    points = tuple(locallocateAll(needleImage, haystackImage, **kwargs))
    if len(points) > 0:
        return points[0]
    else:
        if pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION:
            raise pyscreeze.ImageNotFoundException("Could not locate the image.")
        else:
            return None


def boxcenter(box):
    if isinstance(box, tuple):
        return pyscreeze.center(box)
    return pyscreeze.Point(box.left + box.width / 2, box.top + box.height / 2)
