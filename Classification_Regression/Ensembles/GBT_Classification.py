"""

Created by: Jing Rong

Gradient-Boosted Trees (GBTs) are ensembles of decision trees. 
GBTs iteratively train decision trees in order to minimize a loss function. 
Similar to decision trees, GBTs handle categorical features, extend to the multiclass classification setting, 
	do not require feature scaling, and are able to capture non-linearities and feature interactions.
More sensetive to overfitting if data is noisy. Exhibits higher variance as well.

tl;dr -> Gradient boosting combines weak learners into a single strong learner, in an iterative fashion

Note: MLlib supports GBTs for binary classification and for regression, using both continuous and categorical features.
	  MLlib implements GBTs using the existing decision tree implementation.
	  GBTs do not yet support multiclass classification. For multiclass problems, please use decision trees or Random Forests.


Classification - Predict the class in which the data belongs
	-> Works by majority vote. Each tree prediction is counted as 1 vote for a class.
	-> Label is predicted to by the class which receive the highest number of votes.

The example below demonstrates how to load a LIBSVM data file, 
parse it as an RDD of LabeledPoint and then perform classification using a Random Forest. 
The test error is calculated to measure the algorithm accuracy.
"""


# Imports
# Import DecisionTree / DecisionTreeModel
from pyspark.mllib.tree import GradientBoostedTrees, GradientBoostedTreesModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils
from pyspark import SparkContext

sc = SparkContext("local", "Ensemble")

# Loading and parsing data into RDD of LabeledPoint
# Sample data provided by Spark 1.3.1 folder

# To run locally
# data = MLUtils.loadLibSVMFile(sc, 'sample_libsvm_data.txt')

# To run on hadoop server
data = MLUtils.loadLibSVMFile(sc, 'jingrong/sample_libsvm_data.txt')

# Splits data - Approximately 70% training , 30% testing
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train the Gradient Boosted Forest model
# Empty categoricalFeaturesInfo indicates that all features are continuous.
# In practice -> use more iterations

# Settings featureSubsetStrategy to "auto" lets the algo choose automatically
model = GradientBoostedTrees.trainClassifier(trainingData,
    categoricalFeaturesInfo={}, numIterations=5)

# Evaluate the model on test instances, compute test error
allPredictions = model.predict(testData.map(lambda x: x.features))
predictionsAndLabels = testData.map(lambda pl: pl.label).zip(allPredictions)
testError = predictionsAndLabels.filter(lambda (v, p): v != p).count() / float(testData.count())

# Printing results
print
print "Tested Error: ", testError
print 
print "Learned classification Gradient Boosted Tree model: "
print model.toDebugString()

"""
Optional Saving/Loading of model
model.save(sc, "myModelPath")
sameModel = DecisionTreeModel.load(sc, "myModelPath")
"""


