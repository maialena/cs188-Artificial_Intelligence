# features.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import numpy as np
import util
import samples

DIGIT_DATUM_WIDTH=28
DIGIT_DATUM_HEIGHT=28

def basicFeatureExtractor(datum):
    """
    Returns a binarized and flattened version of the image datum.

    Args:
        datum: 2-dimensional numpy.array representing a single image.

    Returns:
        A 1-dimensional numpy.array of features indicating whether each pixel
            in the provided datum is white (0) or gray/black (1).
    """
    features = np.zeros_like(datum, dtype=int)
    features[datum > 0] = 1
    return features.flatten()

def enhancedFeatureExtractor(datum):
    """
    Returns a feature vector of the image datum.

    Args:
        datum: 2-dimensional numpy.array representing a single image.

    Returns:
        A 1-dimensional numpy.array of features designed by you. The features
            can have any length.

    ## DESCRIBE YOUR ENHANCED FEATURES HERE...

    ##
    """
    features = basicFeatureExtractor(datum)

    "*** YOUR CODE HERE ***"
    # strikethroughFeature = [0]
    # longStraightLineFeature = [0]
    # longestStraightLine = 0
    # for row in  datum:
    #     seenNumber = 0 #0 means haven't seen any black, 1 menas in continuous black, 2 means transitino from black to white
    #     localStraightLine = 0
    #     for elem in row:
    #         if seenNumber == 2 and elem != 0:
    #             strikethroughFeature[0] = 1
    #             break
    #         if seenNumber == 1 and elem == 0:
    #             seenNumber = 2
    #         if seenNumber == 0 and elem != 0:
    #             seenNumber = 1
    #         if seenNumber == 1 and elem != 0:
    #             localStraightLine += 1
    #     longestStraightLine = max(localStraightLine, longestStraightLine)
    # features = np.append(features, strikethroughFeature)
    # if longestStraightLine > 10:
    #     longStraightLineFeature[0] = 1
    # features = np.append(features, longStraightLineFeature)
    numWhiteSpaces = [0, 0, 0]
    
    def bfsForWhiteSpace(datum, start, closed):
        fringe = []
        closed = set()
        fringe.append(start)
        while fringe != []:
            node = fringe.pop(0)
            closed.add(node)
            children = []
            if node[0] > 0 and datum[node[0]-1][node[1]][0] == 0 and (node[0]-1, node[1]) not in closed and (node[0]-1, node[1]) not in fringe:
                children.append((node[0] - 1, node[1])) #up
            if node[1] > 0 and datum[node[0]][node[1]-1][0] == 0 and (node[0], node[1]-1) not in closed and (node[0], node[1]-1) not in fringe:
                children.append((node[0], node[1]-1)) #left
            if node[0] < len(datum) - 1 and datum[node[0]+1][node[1]][0] == 0 and (node[0]+1, node[1]) not in closed and (node[0]+1, node[1]) not in fringe:
                children.append((node[0]+1, node[1])) #down
            if node[1] < len(datum[0]) - 1 and datum[node[0]][node[1]+1][0] == 0 and (node[0], node[1]+1) not in closed and (node[0], node[1]+1) not in fringe:
                children.append((node[0], node[1]+1)) #right
            fringe.extend(children)
        return closed
    closed = set()
    whiteSpaceSeen = 0
    for row in range(len(datum)):
        for col in range(len(datum[0])):
            if datum[row][col][0] == 0 and (row, col) not in closed:
                closed = bfsForWhiteSpace(datum, (row, col), closed)
                whiteSpaceSeen += 1
    if whiteSpaceSeen == 1:
        numWhiteSpaces[0] = 1
    elif whiteSpaceSeen == 2:
        numWhiteSpaces[1] = 1
    elif whiteSpaceSeen > 2:
        numWhiteSpaces[2] = 1
    features = np.append(features, numWhiteSpaces)

    return features


def analysis(model, trainData, trainLabels, trainPredictions, valData, valLabels, validationPredictions):
    """
    This function is called after learning.
    Include any code that you want here to help you analyze your results.

    Use the print_digit(numpy array representing a training example) function
    to the digit

    An example of use has been given to you.

    - model is the trained model
    - trainData is a numpy array where each row is a training example
    - trainLabel is a list of training labels
    - trainPredictions is a list of training predictions
    - valData is a numpy array where each row is a validation example
    - valLabels is the list of validation labels
    - valPredictions is a list of validation predictions

    This code won't be evaluated. It is for your own optional use
    (and you can modify the signature if you want).
    """

    # Put any code here...
    # Example of use:
    # for i in range(len(trainPredictions)):
    #     prediction = trainPredictions[i]
    #     truth = trainLabels[i]
    #     if (prediction != truth):
    #         print "==================================="
    #         print "Mistake on example %d" % i
    #         print "Predicted %d; truth is %d" % (prediction, truth)
    #         print "Image: "
    #         print_digit(trainData[i,:])


## =====================
## You don't have to modify any code below.
## =====================

def print_features(features):
    str = ''
    width = DIGIT_DATUM_WIDTH
    height = DIGIT_DATUM_HEIGHT
    for i in range(width):
        for j in range(height):
            feature = i*height + j
            if feature in features:
                str += '#'
            else:
                str += ' '
        str += '\n'
    print(str)

def print_digit(pixels):
    width = DIGIT_DATUM_WIDTH
    height = DIGIT_DATUM_HEIGHT
    pixels = pixels[:width*height]
    image = pixels.reshape((width, height))
    datum = samples.Datum(samples.convertToTrinary(image),width,height)
    print(datum)

def _test():
    import datasets
    train_data = datasets.tinyMnistDataset()[0]
    for i, datum in enumerate(train_data):
        print_digit(datum)

if __name__ == "__main__":
    _test()
