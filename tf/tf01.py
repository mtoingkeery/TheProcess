import os
#Warning:Your CPU supports instructions that this TensorFlow binary was not compiled
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import time

print(time.strftime('%Y/%m/%d %T')+" - Start")
matrix1 = tf.constant([[3., 3., 3.]])
matrix2 = tf.constant([[2.], [2.], [2.]])
product = tf.matmul(matrix1, matrix2)
###device info
#sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
sess = tf.Session()

result = sess.run(product)
print (result)
sess.close()

print(time.strftime('%Y/%m/%d %T')+" - End")


from tensorflow.python.client import device_lib
###device info
print(device_lib.list_local_devices())
