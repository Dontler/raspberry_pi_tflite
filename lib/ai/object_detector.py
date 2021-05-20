import tflite_runtime.interpreter as tflite

from lib.ai.input_details import InputDetails
from lib.ai.output_details import OutputDetails
from lib.capture.image import Image


class ObjectDetectorConfig:

    def __init__(self, model_path: str, width: int, height: int):
        self.__model_path = model_path
        self.__width = width
        self.__height = height

    @property
    def model_path(self):
        return self.__model_path

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height


class ObjectDetector:

    def __init__(self, config: ObjectDetectorConfig):
        self.__interpreter = tflite.Interpreter(model_path=config.model_path, num_threads=4)
        self.__config = config
        self.__interpreter.allocate_tensors()

        input_details = self.__interpreter.get_input_details()
        shape = input_details[0]['shape']
        index = input_details[0]['index']

        self.__input_details = InputDetails(shape, index)

    @property
    def input_details(self) -> InputDetails:
        return self.__input_details

    def detect(self, img: Image) -> OutputDetails:
        img_rgb = Image.to_rgb(img, self.__config.width, self.__config.height)
        img_rgb = img_rgb.source.reshape(self.input_details.shape)

        self.__interpreter.set_tensor(self.input_details.index, img_rgb)
        self.__interpreter.invoke()

        output = self.__interpreter.get_output_details()
        return OutputDetails(
            boxes=self.__interpreter.get_tensor(output[0]["index"])[0],
            classes=self.__interpreter.get_tensor(output[1]["index"])[0],
            scores=self.__interpreter.get_tensor(output[2]["index"])[0],
            num=self.__interpreter.get_tensor(output[3]["index"])[0],
        )
