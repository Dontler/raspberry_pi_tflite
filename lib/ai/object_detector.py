import tflite_runtime.interpreter as tflite

from lib.ai.input_details import InputDetails
from lib.ai.output_details import OutputDetails


class ObjectDetector:

    def __init__(self, model_path: str):
        self.__interpreter = tflite.Interpreter(model_path=model_path)
        self.__interpreter.allocate_tensors()

        input_details = self.__interpreter.get_input_details()
        shape = input_details[0]['shape']
        index = input_details[0]['index']

        self.__input_details = InputDetails(shape, index)

    @property
    def input_details(self) -> InputDetails:
        return self.__input_details

    def detect(self, img) -> OutputDetails:
        self.__interpreter.set_tensor(self.input_details.index, img)
        self.__interpreter.invoke()

        output = self.__interpreter.get_output_details()
        return OutputDetails(
            boxes=self.__interpreter.get_tensor(output[0]["index"])[0],
            classes=self.__interpreter.get_tensor(output[1]["index"])[0],
            scores=self.__interpreter.get_tensor(output[2]["index"])[0],
            num=self.__interpreter.get_tensor(output[3]["index"])[0],
        )

