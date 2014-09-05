'''
File: Classifier
----------------
This is your file to modify! You should fill in both
the learn and extractFeatures functions. 
'''

import util
import numpy as np

PATCH_LENGTH = 64

class FeatureLearner(object):

    # Constructor
    # -----------
    # Called when the classifier is first created.
    def __init__(self, k):
        #DON"T CHANGE THIS. USED FOR GRADING
        self.maxIter = 50
        self.trained = False
        self.k = k
        self.centroids = None

    # Function: Run K Means
    # -------------
    # Given a set of training images, and a number of features
    # to learn self.k number of centroids. This 
    # function will be called only once. It does not return
    # a value. Instead this function fills in self.centroids.
    def runKmeans(self, trainImages):
        assert not self.trained

        # This line starts you out with random patches which 
        # are stored in a matrix with 64 rows and k columsn. 
        # Each col is a patch.
        # Each patch has 64 values.
        self.centroids = np.random.randn(PATCH_LENGTH, self.k) #there are 64 rows, each with k columns
        imagePatches = self.getImagePatches(trainImages) #1600 patches, each patch has 64 pixels 
        print "imagePatches.shape: " + str(imagePatches.shape) #(1600, 64)

        #Initialize book keeping variables
        iterations = 0
        oldCentroids = None

        while not self.shouldStop(oldCentroids, self.centroids, iterations):
            oldCentroids = self.centroids 
            iterations += 1
            labels = [self.getLabel(patch, self.centroids) for patch in imagePatches] #assign labels to each datapoints based on centroids
            self.centroids = self.getCentroids(imagePatches, labels, self.k) #assign centroids based on datapoint labels
            
        self.trained = True

    # Function: Get Image Patches
    # ------------
    # Returns the image patches with 64 columns, each row represent a patch,
    # each patch has 64 pixels.
    def getImagePatches(self, trainImages):
        numImages = len(trainImages)
        imagePatches = trainImages[0].getPatches() #16 patches, each patch has 64 pixels
        for i in range(1, numImages):
            imagePatches = np.vstack((imagePatches, trainImages[i].getPatches()))
        return imagePatches


    # Function: Should Stop
    # -----------
    # Returns True or False if k-means is done. K-means terminates either
    # because it has run a maximum number of iterations or the centroids 
    # stop changing.
    def shouldStop(self, oldCentroids, centroids, iterations):
        if iterations >= self.maxIter: 
            return True
        else:
            if oldCentroids == None:
                return False
            tOldCentroids = np.transpose(oldCentroids) #transpose
            tCentroids = np.transpose(centroids) #transpose
            trueArray = [True for i in range(self.k)]
            boolArray = [np.array_equal(tOldCentroids[i], tCentroids[i]) for i in range(self.k)]
            return np.array_equal(trueArray, boolArray)

    def getLabel(self, patch, centroids): #returns a value from 0 to k-1
        distances = [np.linalg.norm(patch - centroid) for centroid in np.transpose(centroids)]
        return np.argmin(distances)
    
    def getCentroids(self, imagePatches, labels, k):
        centroids = [self.newCentroid(i, imagePatches, labels) for i in range(k)] #5 rows
        return np.transpose(centroids)
        
    def newCentroid(self, i, imagePatches, labels):
        nearPatches = [imagePatches[index] for index in range(len(imagePatches)) if labels[index] == i]
        if(len(nearPatches) != 0): 
            return np.mean(nearPatches, axis=0)
        else:
            return imagePatches[i]

    # Function: Extract Features
    # -------------
    # Given an image, extract and return its features. This
    # function will be called many times. Should return a 1-d
    # feature array that is number of patches by number of
    # centroids long. Assume that k-means has already been 
    # run.
    def extractFeatures(self, image):
        assert self.trained

        # populate features with features for each patch
        # of the image. 
        numPatches = len(image.getPatches())
        features = np.zeros((numPatches*self.k)) #a00,...,a0k-1,a10,...,a1k-1,...,a150,...,a15k-1
        centroids = np.transpose(self.centroids)
        for i in range(numPatches):
            patch = image.getPatches()[i]
            for j in range(self.k):
                distances = [np.linalg.norm(patch - centroid) for centroid in centroids]
                aij = sum(distances)/self.k - np.linalg.norm(patch - centroids[j])
                features[i * self.k + j] = max(0, aij)

        return features