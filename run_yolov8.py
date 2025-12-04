import tflite_runtime.interpreter as tflite
import tensorflow as tf
import numpy as np
import time
from video_frame_iter import video_frame_generator
import sys

"""
Runs a full integer quantized yolov8n model from UltraVision using tflite runtime

Requires video_frame_iter.py, which should be provided in whereever you obtained this module
"""

accelerator="CORAL"
IMG_SZ=640

if (accelerator == "CORAL"):
        #model_path = "yolov8n_no_nms_full_integer_quant.tflite"
        #model_path = "yolov8n_full_integer_quant_edgetpu_imgsz_160_edgetpu.tflite"
        #model_path = "yolov8n_full_integer_quant_edgetpu_imgsz_320.tflite"
        model_path = f"yolov8n_full_integer_quant_edgetpu_imgsz_{IMG_SZ}.tflite"
        interpreter = tflite.Interpreter(model_path,
                                 experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
elif (accelerator == "CPU"):
        #model_path = "yolov8n_full_integer_quant_imgsz_160.tflite"
        #model_path = "yolov8n_full_integer_quant_imgsz_320.tflite"
        model_path = f"yolov8n_full_integer_quant_edgetpu_imgsz_{IMG_SZ}.tflite"
        interpreter = tflite.Interpreter(model_path)
else:
        sys.exit("define your accelerator correctly!")


interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]
output_details = interpreter.get_output_details()[0]
input_index = input_details['index']
output_index = output_details['index']

video_path="test.mp4"
# skip some frames we aren't forwarding effectively duplicate frames
step=5
video_dataset = video_frame_generator(video_path, step=5, resize=(IMG_SZ,IMG_SZ))
 
latencies = []
for idx, frame in video_dataset:
        input_data = np.expand_dims(frame, axis=(0)).astype(np.int8)
        #expected_cls = y_test[i]
        interpreter.set_tensor(input_index, input_data)
# 
        # benchmark latency
        start_time = time.perf_counter_ns()
        interpreter.invoke()
        end_time = time.perf_counter_ns()
 
        latency = ((end_time - start_time) / (1e6))
        latencies.append(latency)
 
        output_data = interpreter.get_tensor(output_index)
        pred = np.argmax(output_data)

        print(f"Predicted class {np.argmax(output_data)} in {latency}ms)")
        # Note: No bounding box prediction and non-maximum suppression is performed on the accelerator side. These are performed on the CPU side

print(f"Average latency: {np.mean(latencies)}ms")
#print(f"Accuracy: {n_correct / samples}")
