from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from polls.models import Image
from polls.FileUploadForm import FileUploadForm
import os
from django.contrib.staticfiles.templatetags.staticfiles import static
import cv2
import tensorflow as tf
import polls.preprocessor as preprocessor
import polls.network as network
import numpy as np

# Create your views here.
def index(request):
    form = FileUploadForm
    return render(request, 'index.html',{'form':form})

def upload_file(request):
    form = FileUploadForm(request.POST, request.FILES)
    if request.method == 'POST':
        test = Image(test_img = request.FILES['test'])
        test.save()
        main()
        print('OpenCV version {} '.format(cv2.__version__))

        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        author = '021'
        training_folder = os.path.join(current_dir, 'media/data/training/', author)
        test_folder = os.path.join(current_dir, 'media/data/test/', author)

        training_data = []
        training_labels = []
        for filename in os.listdir(training_folder):
            img = cv2.imread(os.path.join(training_folder, filename), 0)
            if img is not None:
                data = preprocessor.prepare(img)
                training_data.append(data)
                training_labels.append([0, 1] if "genuine" in filename else [1, 0])

        test_data = []
        test_labels = []
        for filename in os.listdir(test_folder):
            img = cv2.imread(os.path.join(test_folder, filename), 0)
            if img is not None:
                data = preprocessor.prepare(img)
                test_data.append(data)
                test_labels.append([0, 1] if "genuine" in filename else [1, 0])

        message = sgd(training_data, training_labels, test_data, test_labels)
        print(message)
    return render(request, 'result.html',{'message':message})

# Softmax Regression Model
def regression(x):
    W = tf.Variable(tf.zeros([901, 2]), name="W")
    b = tf.Variable(tf.zeros([2]), name="b")
    y = tf.nn.softmax(tf.matmul(x, W) + b)
    return y, [W, b]


def sgd(training_data, training_labels, test_data, test_labels):
    # model
    with tf.variable_scope("regression"):
        x = tf.placeholder(tf.float32, [None, 901])
        y, variables = regression(x)

    # train
    y_ = tf.placeholder("float", [None, 2])
    cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(train_step, feed_dict={x: training_data, y_: training_labels})
        return (sess.run(accuracy, feed_dict={x: test_data, y_: test_labels}))

def main():
    print('OpenCV version {} '.format(cv2.__version__))

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    author = '021'
    training_folder = os.path.join(current_dir, 'media/data/training/', author)
    test_folder = os.path.join(current_dir, 'media/data/test/', author)

    training_data = []
    for filename in os.listdir(training_folder):
        img = cv2.imread(os.path.join(training_folder, filename), 0)
        if img is not None:
            data = np.array(preprocessor.prepare(img))
            data = np.reshape(data, (901, 1))
            result = [[0], [1]] if "genuine" in filename else [[1], [0]]
            result = np.array(result)
            result = np.reshape(result, (2, 1))
            training_data.append((data, result))

    test_data = []
    for filename in os.listdir(test_folder):
        img = cv2.imread(os.path.join(test_folder, filename), 0)
        if img is not None:
            data = np.array(preprocessor.prepare(img))
            data = np.reshape(data, (901, 1))
            result = 1 if "genuine" in filename else 0
            test_data.append((data, result))

    net = network.NeuralNetwork([901, 500, 500, 2])
    net.sgd(training_data, 10, 50, 0.01, test_data)
