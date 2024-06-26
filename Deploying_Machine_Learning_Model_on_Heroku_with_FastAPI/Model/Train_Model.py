import logging
from sklearn.model_selection import train_test_split
from joblib import dump
from data import process_data
from clean_data import load_data, cleaned_data
from model_functions import train_model, compute_model_metrics, model_predictions

logging.basicConfig(
    filename='./log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)

cat_features = [
    "workclass",
    "education",
    "marital-status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "native-country",
]

def split_data(data):
    try:
        train, test = train_test_split(data, test_size=0.20, random_state=0)
        logging.info('SUCCESS: Data split successfully')
        return train, test
    except Exception as e:
        logging.error(f'ERROR: Error while splitting data. {e}')

def model_slicing(data, model, encoder, lb):
    """
    Slice model for categorical features
    """
    try:
        slice_values = []
        for cat in cat_features:
            for cls in data[cat].unique():
                df_temp = data[data[cat] == cls]
                X_test_temp, y_test_temp, _, _ = process_data(
                    df_temp, categorical_features=cat_features,
                    label="salary", encoder=encoder, lb=lb, training=False)
                y_preds = model.predict(X_test_temp)
                precision_temp, recall_temp, fbeta_temp = compute_model_metrics(
                    y_test_temp, y_preds)
                results = "[%s->%s] Precision: %s Recall: %s FBeta: %s" % (
                    cat,
                    cls,
                    precision_temp,
                    recall_temp,
                    fbeta_temp)
                slice_values.append(results)

        with open('slice_model_output.txt', 'w') as out:
            for slice_value in slice_values:
                out.write(slice_value + '\n')
    except Exception as e:
        logging.error(f'ERROR: Error occurred during model slicing. {e}')

if __name__ == '__main__':
    try:
        df = load_data('census_cleaned.csv')
        train, test = split_data(df)
        test.to_csv('testings.csv')
        X_train, y_train, encoder, lb = process_data(
            train, categorical_features=cat_features,
            label="salary", training=True)
        X_test, y_test, encoder_t, lb_t = process_data(
            test, categorical_features=cat_features,
            label="salary", training=False, encoder=encoder, lb=lb)
        dump(encoder_t, 'encoder.joblib')
        dump(lb_t, 'lb.joblib')
        model = train_model(X_train, y_train)
        dump(model, 'model.joblib')
        predictions = model_predictions(X_test, model)
        precision, recall, fbeta = compute_model_metrics(y_test, predictions)
        model_slicing(df, model, encoder, lb)
    except Exception as e:
        logging.error(f'ERROR: An error occurred. {e}')
