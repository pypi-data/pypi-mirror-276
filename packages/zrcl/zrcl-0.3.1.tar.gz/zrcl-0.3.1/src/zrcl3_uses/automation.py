from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from functools import cached_property
import logging
import time
import typing
import numpy
import pygetwindow as gw
from PIL import Image
import screeninfo
from zrcl4.pillow import load_base64_img
from zrcl4.pygetwindow import activate_wnd, get_window_pos, refetch_wnd
from zrcl4.pyscreeze import boxcenter
from zrcl4.screeninfo import get_primary_monitor, wnd_on_monitor
from pyscreeze import Box


def img_reg(token: "AutoToken"):
    from zrcl4.pyscreeze import locate

    res = locate(
        token.sourceImg,
        token.targetImg,
        _algo=token.cfg_imgAlgo,
        confidence=token.confidence,
    )

    if isinstance(res, Box) or (isinstance(res, tuple) and len(res) == 4):
        return tuple(boxcenter(res))

    return res


def ocr(token: "AutoToken"):
    from zrcl4.easyocr import get_text_coordinates, EasyOCRMeta

    imagearr = numpy.array(token.targetImg)
    res: list[EasyOCRMeta] = get_text_coordinates(imagearr, token.cfg_ocrLang)
    token.ocrMatchResult = res
    if token.cfg_ocrMatchMethod == "fuzz":
        from thefuzz import process

        what = process.extract(token.text, res, scorer=process.fuzz.token_set_ratio)
        token.ocrMatchResult = what
        rect = what[0][0]

    else:
        records = []
        maxed = None
        for item in res:
            if token.cfg_ocrMatchMethod == "exact" and item["text"] != token.text:
                continue
            elif (
                token.cfg_ocrMatchMethod == "contains"
                and token.text not in item["text"]
            ):
                continue
            elif token.cfg_ocrMatchMethod == "startswith" and not item[
                "text"
            ].startswith(token.text):
                continue
            if maxed is None or item["confidence"] > maxed["confidence"]:
                maxed = item
            records.append((item, item["confidence"]))

        token.ocrMatchResult = records

        if not maxed:
            return None
        rect = maxed

    if rect["confidence"] < token.confidence:
        return None

    top_left = rect["top_left"]
    bottom_rght = rect["bottom_right"]
    # return as center point
    return (top_left[0] + bottom_rght[0]) / 2, (top_left[1] + bottom_rght[1]) / 2


@dataclass
class AutoToken:
    text: str = None
    image: typing.Union[Image.Image, str, numpy.ndarray] = None

    wnd: typing.Union[str, gw.Window] = None
    monitor: typing.Union[screeninfo.Monitor, int] = None
    region: typing.Tuple[typing.Union[int, float], ...] = None
    image2: typing.Union[Image.Image, str, numpy.ndarray] = None

    confidence: float = 0.8

    cfg_imgAlgo: typing.Literal["cv2", "pillow"] = "pillow"
    cfg_ocrLang: typing.List[str] = field(default_factory=lambda: ["en"])
    cfg_ocrMatchMethod: typing.Literal["startswith", "contains", "fuzz", "exact"] = (
        "fuzz"
    )

    onImgProcess: typing.Callable = None
    preProcessCallback: typing.Callable = None
    postProcessCallback: typing.Callable = None
    ocrMethod: typing.Callable = ocr
    imgMethod: typing.Callable = img_reg

    ocrMatchResult: typing.List[dict] = None
    result: typing.Tuple[float, float] = None

    def __getattribute__(self, name):
        if name == "wnd":
            wnd = super().__getattribute__(name)
            object.__setattr__(self, "wnd", refetch_wnd(wnd) if wnd else None)

        return super().__getattribute__(name)

    def __post_init__(self):
        if not self.text and not self.image:
            raise ValueError("Either 'text' or 'image' must be set")

        if self.monitor and isinstance(self.monitor, int):
            self.monitor = screeninfo.get_monitors()[self.monitor]

        if self.wnd and isinstance(self.wnd, str):
            self.wnd = gw.getWindowsWithTitle(self.wnd)[0]

    def screenshot(self):
        import pyscreeze

        if self.wnd:
            activate_wnd(self.wnd)
        return pyscreeze.screenshot(
            region=self.interestedRegion,
            allScreens=True if not self.wnd or self.wndInNonPrimaryMonitor else False,
        )

    @staticmethod
    def __prep_img(img):
        if isinstance(img, Image.Image):
            return img
        elif isinstance(numpy, numpy.ndarray):
            return Image.fromarray(img)
        elif isinstance(img, str) and img.startswith("data:image/png;base64,"):
            return load_base64_img(img)
        elif isinstance(img, str):
            return Image.open(img)
        else:
            raise ValueError("Invalid image type")

    @cached_property
    def sourceImg(self):
        if self.text:
            return None

        return self.__prep_img(self.image)

    @property
    def targetImg(self):
        if self.image2:
            return self.__prep_img(self.image2)

        # screenshot
        import pyscreeze

        if self.wnd:
            activate_wnd(self.wnd)
        ss = pyscreeze.screenshot(
            region=self.interestedRegion,
            allScreens=True if not self.wnd or self.wndInNonPrimaryMonitor else False,
        )
        if self.onImgProcess:
            self.onImgProcess(ss)
        return ss

    @property
    def regionIsRect(self):
        return len(self.region) == 4

    @property
    def regionAsInts(self):
        return tuple(map(int, self.region))

    @property
    def wndInNonPrimaryMonitor(self):
        if not self.wnd:
            return None

        return wnd_on_monitor(self.wnd) != get_primary_monitor()

    @property
    def monitorCenterPoint(self):
        if not self.monitor:
            return None
        assert isinstance(self.monitor, screeninfo.Monitor)
        return (
            self.monitor.x + self.monitor.width / 2,
            self.monitor.y + self.monitor.height / 2,
        )

    @property
    def interestedRegion(self):
        if self.wnd and not self.monitor:
            self.monitor = wnd_on_monitor(self.wnd)

        match (self.wnd, self.monitor, self.region):
            case (None, None, None):
                primary = get_primary_monitor()
                return (primary.x, primary.y, primary.width, primary.height)
            case (wnd, _, None):
                return get_window_pos(wnd)
            case (wnd, _, region) if self.regionIsRect:
                base = get_window_pos(wnd)
                return (base[0] + region[0], base[1] + region[1], region[2], region[3])
            case (wnd, _, region) if not self.regionIsRect:
                # treat as width and height in center
                base = get_window_pos(wnd)
                return (
                    base[0] + base[2] / 2 - region[0] / 2,
                    base[1] + base[3] / 2 - region[1] / 2,
                    region[0],
                    region[1],
                )
            case (None, None, region) if not self.regionIsRect:
                self.monitor = get_primary_monitor()
                return (
                    self.monitorCenterPoint[0] - region[0] / 2,
                    self.monitorCenterPoint[1] - region[1] / 2,
                    region[0],
                    region[1],
                )
            case (None, None, region):
                return region
            case (None, screeninfo.Monitor(_), region) if not self.regionIsRect:
                return (
                    self.monitorCenterPoint[0] - region[0] / 2,
                    self.monitorCenterPoint[1] - region[1] / 2,
                    region[0],
                    region[1],
                )
            case (None, screeninfo.Monitor(_), region) if self.regionIsRect:
                return (
                    self.monitorCenterPoint[0] - region[0] / 2,
                    self.monitorCenterPoint[1] - region[1] / 2,
                    region[2],
                    region[3],
                )
            case (None, monitor, None):
                return (monitor.x, monitor.y, monitor.width, monitor.height)

            case _:
                raise ValueError("Invalid combination of parameters")

    def _execute(self):
        if self.preProcessCallback:
            self.preProcessCallback(self)
        if self.wnd:
            activate_wnd(self.wnd)

        if self.text:
            res = self.ocrMethod(self)
        else:
            res = self.imgMethod(self)

        if not res:
            return None

        # relative to interested region
        iregion = self.interestedRegion
        self.result = res
        curr_normalized = (res[0] + iregion[0], res[1] + iregion[1])
        if self.postProcessCallback:
            self.postProcessCallback(self, curr_normalized)

        return curr_normalized

    def __call__(self, **kwds):
        return self._execute()

    @property
    def normalizedResult(self):
        iregion = self.interestedRegion
        return (
            self.result[0] + iregion[0],
            self.result[1] + iregion[1],
        )


@dataclass(init=False)
class FrozenToken(AutoToken):
    def __init__(self, autoToken: AutoToken):
        if not autoToken.result:
            raise ValueError("result must be set")
        d = asdict(autoToken)
        super().__init__(
            **d,
        )
        self.__inited__ = True

    def __setattr__(self, name: str, value) -> None:
        if not hasattr(self, "__inited__"):
            return super().__setattr__(name, value)

        if not hasattr(self, name):
            return super().__setattr__(name, value)

        raise AttributeError(f"{self.__class__.__name__} is frozen")

    def __hash__(self):
        return hash(self.result)


def waitFor(token: AutoToken, timeout: float = 10.0, interval: float = 1.1):
    currentTime = time.time()
    while time.time() - currentTime < timeout:
        try:
            if token():
                break
        except Exception as e:
            logging.error(e)

        time.sleep(interval)

    if not token.result:
        raise TimeoutError("Timed out")
    return token.normalizedResult


@contextmanager
def repeatWith(token: AutoToken, times: int = 1):
    for _ in range(times):
        yield token()
    return token.normalizedResult
