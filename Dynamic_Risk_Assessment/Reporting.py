import pickle
import pandas as pd
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def score_model(model_path, test_data_path, output_path, confusion_matrix_name):
    """Calculate a confusion matrix using the test data and the deployed model."""
    model = pickle.load(open(model_path, 'rb'))
    df = pd.read_csv(test_data_path)
    X_test = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y_test = df['exited']
    preds = model.predict(X_test)
    cf_matrix = confusion_matrix(y_test, preds)
    sns.heatmap(cf_matrix, annot=True)
    plt.savefig(os.path.join(output_path, confusion_matrix_name))
    plt.close()

def main():
    config = load_config('config.json')

    prod_deployment_path = config["prod_deployment_path"]
    test_data_path = config["test_data_path"]
    output_model_path = config["output_model_path"]
    trained_model_name = config["trained_model_name"]
    test_data_name = config["test_data_name"]
    confusion_matrix_name = config["confusion_matrix_name"]

    deployed_model_path = os.path.join(prod_deployment_path, trained_model_name)
    test_data_file_path = os.path.join(test_data_path, test_data_name)

    score_model(deployed_model_path, test_data_file_path, output_model_path, confusion_matrix_name)

if __name__ == '__main__':
    main()
