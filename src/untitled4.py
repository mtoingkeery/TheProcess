import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# OP_HELLO 的类型为 tensorflow.python.framework.ops.Tensor
OP_HELLO = tf.constant('Hello, Tensor Flow!')

# SESSION 的类型为 tensorflow.python.client.session.Session
SESSION = tf.Session()

print(SESSION.run(OP_HELLO))


matrix1 = tf.constant([[3., 3.]])
matrix2 = tf.constant([[2.], [2.]])
product = tf.matmul(matrix1, matrix2)
sess = tf.Session()
result = sess.run(product)
print(result)
sess.close()