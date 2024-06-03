# mini_scikit_learn

**mini_scikit_learn** is a minimalistic clone of scikit-learn, designed to provide essential machine learning functionalities with minimal overhead. It only depends on numpy and offers a variety of basic and advanced models, utility functions, metrics, data transformers, and model selection tools. 

## Features

### Models
- **Linear Models**: Implementations of linear regression, logistic regression, etc.
- **Tree-Based Models**: Decision trees for classification and regression.
- **K-Nearest Neighbors**: KNN for classification and regression.
- **Random Forest**: Ensemble method for classification and regression.
- **SVM**: Support Vector Machines for classification and regression.(Under Testing)
- **Naive Bayes**: Various naive Bayes classifiers.
- **Neural Networks**: Basic feedforward and backpropagation neural networks, with customizable layers and activation functions.
- **Ensembling Techniques**: Advanced techniques such as voting, stacking, and boosting (AdaBoost, Gradient Boosting).


### Utility Functions
- **Cross Validation**: Functions for k-fold cross-validation, train-test splitting, etc.
- **Train-Test Split**: Simple utility to split datasets into training and testing sets.
- **K-Folds**: Functionality to split data into k folds for cross-validation.

### Metrics
- **Accuracy**: Measure the accuracy of predictions.
- **Precision**: Calculate the precision for classification models.
- **Recall**: Compute the recall for classification models.
- **F1 Score**: Calculate the F1 score for classification models.
- **Mean Squared Error (MSE)**: Compute the mean squared error for regression models.
- **Mean Absolute Error (MAE)**: Compute the mean absolute error for regression models.
- **Log Loss**: Calculate the logistic loss for classification models.

### Data Transformers
- **Encoders**: Various encoding techniques for categorical data.
- **Imputers**: Different strategies for handling missing values, SimpleImputer, IterativeImputer, KNNImputer.
- **Scalers**: MinMaxScaler and StandardScaler for feature scaling.

### Model Selection
- **Grid Search**: Exhaustive search over specified parameter values for an estimator.
- **Random Search**: Random search over specified parameter values for an estimator.

## System Architecture

The design of **mini_scikit_learn** is heavily inspired by scikit-learn, with a strong use of inheritance from abstract classes such as `Estimator` and `Predictor`. The library respects the `fit`, `predict`, and `transform` API for all models and transformers, ensuring consistency and ease of use.

### Core Components
- **Estimator**: Base class for all estimators in the library. Defines the `fit` method.
- **Predictor**: Base class for all predictors, extending `Estimator` with the `predict` method.
- **Transformer**: Base class for all transformers, extending `Estimator` with the `transform` method.

By adhering to these interfaces, **mini_scikit_learn** ensures that all components can be used interchangeably, promoting modularity and ease of integration.

## Installation

To install **mini_scikit_learn**, you can use pip:

```bash
pip install mini_scikit_learn
```

## Requirements

- Python > 3
- numpy

## Example Usage

```python
from mini_scikit_learn.model_selection import GridSearch
from mini_scikit_learn.linear_model import LinearRegression
from mini_scikit_learn.metrics import accuracy_score
from mini_scikit_learn.datasets import load_iris
from mini_scikit_learn.utils import train_test_split

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Define the model
model = LinearRegression()

# Define parameter grid
param_grid = {'alpha': [0.1, 0.01, 0.001]}

# Perform grid search
grid_search = GridSearch(model, param_grid)
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.get_best_params()
print("Best Parameters:", best_model)

# Evaluate the model
accuracy = accuracy_score(y_test, best_model.predict(X_test))
print(f"Accuracy: {accuracy}")
```

## Documentation

For more detailed documentation and examples, please refer to the official [mini_scikit_learn documentation](#). (Under Construction)

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

Inspired by the simplicity and efficiency of scikit-learn. This project aims to provide a lightweight alternative for quick prototyping and educational purposes.