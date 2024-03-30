import logging
from sklearn.metrics import fbeta_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE


def train_model(X_train, y_train):
    """
    Trains a machine learning model and returns it.

    Parameters
    ----------
    X_train : np.array
        Training data.
    y_train : np.array
        Labels.

    Returns
    -------
    model : sklearn.ensemble.RandomForestClassifier
        Trained machine learning model.
    """
    try:
        model = RandomForestClassifier()
        smote = SMOTE(random_state=0)
        X_train, y_train = smote.fit_resample(X_train, y_train)
        model.fit(X_train, y_train)
        logging.info('SUCCESS: Model trained and saved')
        return model
    except Exception as e:
        logging.error(f'ERROR: Model not trained and not saved. {e}')


def model_predictions(X_test, model):
    """
    Generate predictions using a trained model.

    Parameters
    ----------
    X_test : np.array
        Test data.
    model : sklearn.ensemble.RandomForestClassifier
        Trained machine learning model.

    Returns
    -------
    predictions : np.array
        Model predictions.
    """
    try:
        predictions = model.predict(X_test)
        logging.info('SUCCESS: Model predictions generated')
        return predictions
    except Exception as e:
        logging.error(f'ERROR: Model predictions not generated. {e}')


def compute_model_metrics(y, preds):
    """
    Validate the trained machine learning model using precision, recall, and F1.

    Parameters
    ----------
    y : np.array
        Known labels, binarized.
    preds : np.array
        Predicted labels, binarized.

    Returns
    -------
    precision : float
    recall : float
    fbeta : float
    """
    try:
        precision = precision_score(y, preds, zero_division=1)
        recall = recall_score(y, preds, zero_division=1)
        fbeta = fbeta_score(y, preds, beta=1, zero_division=1)
        logging.info('SUCCESS: Model scoring completed')
        return precision, recall, fbeta
    except Exception as e:
        logging.error(f'ERROR: Error occurred when scoring model. {e}')


def inference(model, X):
    """
    Run model inferences and return the predictions.

    Parameters
    ----------
    model : sklearn.ensemble.RandomForestClassifier
        Trained machine learning model.
    X : np.array
        Data used for prediction.

    Returns
    -------
    preds : np.array
        Predictions from the model.
    """
    try:
        preds = model.predict(X)
        return preds
    except Exception as e:
        logging.error(f'ERROR: Error occurred during inference. {e}')
        return None
