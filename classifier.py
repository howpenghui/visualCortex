'''
File: Classifier
----------------
This is your file to modify! You should fill in both
the train and test functions.
'''
import math
import random
import util
import numpy as np
from featureLearner import FeatureLearner

class Classifier(object):

    # Constructor
    # -----------
    # Called when the classifier is first created.
    def __init__(self):
        # DONT CHANGE THIS USED FOR GRADING
        self.trained = False
        self.alpha = 1e-5 # learning rate
        self.maxIter = 5000 # max num iterations
        self.featureLearner = None
        self.theta = None # parameter vector for logistic regression

    # Function: Train
    # -------------
    # Given a set of training images, and a number of centroids
    # to learn k,
    # calculate any information you will need in order to make 
    # predictions in the testing phase. This function will be
    # called only once. Your training must feature select!
    def train(self, trainImages, k):
        assert not self.trained

        # We are going to use the Feature Learner you programmed 
        # in the first two parts of the assignment.
        self.featureLearner = FeatureLearner(k)

        # First run your k-means function. After, you will be
        # able to use the extractFeatures method that you wrote.
        self.featureLearner.runKmeans(trainImages)  

        ### YOUR CODE HERE ###
        # Initialize the weight vector from a zero-mean gaussian with 0.01 standard deviation.
        numPatches = len(trainImages[0].getPatches())
        numParams = k * numPatches
        self.theta = np.random.randn(numParams) * 0.01
        # Initialize bookkeeping variables
        numImages = len(trainImages)
        iterations = 0
        oldTheta = None

        imageFeatures = [self.featureLearner.extractFeatures(trainImages[i]) for i in range(numImages)]
        while not self.shouldStop(oldTheta, self.theta, iterations):
            oldTheta = self.theta
            iterations += 1            
            self.theta -= self.alpha * sum([(self.logisticFn(imageFeatures[i]) - trainImages[i].getLabel()) * imageFeatures[i] for i in range(numImages)])

        self.trained = True

    def shouldStop(self, oldTheta, theta, iterations):
        return iterations >= self.maxIter

    def logisticFn(self, features):
        return 1.0/(1.0 + math.exp(-np.inner(self.theta, features)))

    # Function: Test
    # -------------
    # Given a set of testing images
    # calculate a list of predictions for those images. You
    # may assume that the train function has already been called. 
    # This function will be called multiple times.
    def test(self, testImages):
        assert self.trained

        # populate this list with best guess for each image
        predictions = []
        for i in range(len(testImages)):
            prediction = np.inner(self.featureLearner.extractFeatures(testImages[i]), self.theta)
            if prediction > 0.0:
                predictions.append(1)
            else:
                if prediction < 0.0:
                    predictions.append(0)
                else:
                    predictions.append(random.randrange(0, 2, 1))

        ### YOUR CODE HERE ###

        return predictions
