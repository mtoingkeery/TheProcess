import tensorflow as tf
import time
from tensorflow.python.client import device_lib

print(time.strftime('%Y/%m/%d %T')+" - Start")    

matrix1 = tf.constant([[3., 3., 3.]])
matrix2 = tf.constant([[2.], [2.], [2.]])

product = tf.matmul(matrix1, matrix2)
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
result = sess.run(product)
print (result)
sess.close()

print(time.strftime('%Y/%m/%d %T')+" - End")    


two_node = tf.constant(2)
print(two_node)

