from tensorflow.python.client import device_lib
import tensorflow as tf

with tf.device('/gpu:0'):
    print(device_lib.list_local_devices())
    print("gpu used \n\n")

with tf.device('/cpu:0'):
    print(device_lib.list_local_devices())

