import tflite_runtime.interpreter as tflite
import tensorflow as tf
import numpy as np
import time

# Example of running a LeNet compiled in tflite with tflite_runtime

accelerator="CORAL"

if (accelerator == "CORAL"):
        model_path = "lenet_quantized_edgetpu.tflite"
        interpreter = tflite.Interpreter(model_path,
                                 experimental_delegates=[tflite.load_delegate('libedgetpu.so.1')])
elif (accelerator == "CPU"):
        model_path = "lenet_quantized.tflite"
        interpreter = tflite.Interpreter(model_path)


interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]
output_details = interpreter.get_output_details()[0]
input_index = input_details['index']
output_index = output_details['index']

fashion_mnist = tf.keras.datasets.fashion_mnist
n_cls=10
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
y_train = tf.keras.utils.to_categorical(y_train, num_classes=n_cls)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=n_cls)

# iterate through first 255 samples
n_correct = 0
samples = 255

latencies = []
for i in range(samples):
        input_data = np.expand_dims(x_test[i], axis=(0,3))
        expected_cls = y_test[i]
        interpreter.set_tensor(input_index, input_data)

        # benchmark latency too
        start_time = time.perf_counter_ns()
        interpreter.invoke()
        end_time = time.perf_counter_ns()

        latency = ((end_time - start_time) / (1e6))
        latencies.append(latency)

        output_data = interpreter.get_tensor(output_index)
        (pred, labl) = np.argmax(output_data), np.argmax(y_test[i])
        if (pred == labl):
                n_correct += 1
        print(f"Predicted class {np.argmax(output_data)} in {latency}ms, label was {np.argmax(y_test[i])}")

print(f"Average latency: {np.mean(latencies)}ms")
print(f"Accuracy: {n_correct / samples}")
