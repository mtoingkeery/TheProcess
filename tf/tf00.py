import os
#Warning:Your CPU supports instructions that this TensorFlow binary was not compiled
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import time
import tf_input_data as input_data

print(time.strftime('%Y/%m/%d %T')+" - Start")
matrix1 = tf.constant([[3., 3., 3.]])
matrix2 = tf.constant([[2.], [2.], [2.]])
product = tf.matmul(matrix1, matrix2)
sess = tf.Session()

result = sess.run(product)
print(result)
sess.close()

print(time.strftime('%Y/%m/%d %T')+" - End")


mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
print(type(mnist))