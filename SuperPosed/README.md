# Digit Classifier Using VQC

This is a digit classifier which is capable of recognizing digits drawn onto a canvas. We have used the **VQC (Variational Quantum Classifier)** to classify
handwritten digits into digits that can be processed. We have used the *MNIST* handwritten digit dataset for training a VQC classifier that extracts features from
the dataset and classifiew them into individual digits. We first use dimensionality reduction to reduce the number of input features and then train the VQC classifier
on the generated data set. Since VQC classifier is used for binary classification, to categorize data into multiple classes we divided our data using 8 different catgeorizations.
For example one such categorization divided the data into two classes one class containing (0,3,5,6,8) and the second class contatining (1,2,4,7,9).

## Usage

- The file [ml_training.ipynb](https://github.com/Harsh14901/qbraid-qchack/blob/main/ml_training.ipynb) can be used to train the model using the MNIST dataset.
- The file [inference.ipynb](https://github.com/Harsh14901/qbraid-qchack/blob/main/inference.ipynb) can be used to predict a handwritten digit. It includes a canvas on which the digits can be drawn to and then a function call predicts the digits drawn on the canvas.

[Demo Video](https://github.com/Harsh14901/qchack/blob/main/SuperPosed/final4.mp4)
