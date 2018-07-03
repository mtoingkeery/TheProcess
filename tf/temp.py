import os
#Warning:Your CPU supports instructions that this TensorFlow binary was not compiled
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import time
import tf_input_data as input_data

print(time.strftime('%Y/%m/%d %T')+" - Start "+'-'*40 )
"""
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
print(type(mnist))

x = tf.placeholder("float", [None, 784])
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x,W) + b)

y_ = tf.placeholder("float", [None,10])

cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.global_variables_initializer()

sess = tf.Session()
sess.run(init)

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

print(batch_xs,type(batch_xs))

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
"""


def softmax(x):
    """Compute the softmax of vector x."""
    shiftx = x - np.max(x)
    exps = np.exp(shiftx)
    return exps / np.sum(exps)

x=[10,20,30]

print(softmax(x))

print(time.strftime('%Y/%m/%d %T')+" - End "+'-'*42 )
