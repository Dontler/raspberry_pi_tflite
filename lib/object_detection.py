import tflite_runtime.interpreter as tflite


def prepare_interpreter(model_path: str):
    interpreter = tflite.Interpreter(model_path)
    interpreter.allocate_tensors()

    return interpreter


def prepare_output_data(interpreter, output_details):
    return {
        'boxes': interpreter.get_tensor(output_details[0]['index'])[0],
        'classes': interpreter.get_tensor(output_details[1]['index'])[0],
        'scores': interpreter.get_tensor(output_details[2]['index'])[0],
        'num': interpreter.get_tensor(output_details[3]['index'])[0]
    }
