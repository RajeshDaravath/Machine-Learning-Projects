import pandas as pd
import pickle
import os
from sklearn.metrics import f1_score
import json

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def score_model(deployed_model_path, test_data_file_path, output_model_path, latest_score_name):
    """Score the model using F1 score and write the result to the latestscore.txt file."""
    model = pickle.load(open(deployed_model_path, 'rb'))
    df = pd.read_csv(test_data_file_path)
    X_test = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y_test = df['exited']
    pred = model.predict(X_test)
    f1 = f1_score(y_test, pred)

    if not os.path.exists(output_model_path):
        os.makedirs(output_model_path)
    with open(os.path.join(output_model_path, latest_score_name), 'w') as f:
        f.write(str(f1))

    return f1

def main():
    config = load_config('config.json')

    output_model_path = config['output_model_path']
    test_data_path = config["test_data_path"]
    trained_model_name = config["trained_model_name"]
    test_data_name = config["test_data_name"]
    latest_score_name = config["latest_score_name"]

    deployed_model_path = os.path.join(output_model_path, trained_model_name) 
    test_data_file_path = os.path.join(test_data_path, test_data_name)

    f1_score = score_model(deployed_model_path, test_data_file_path, output_model_path, latest_score_name)
    print(f1_score)

if __name__ == '__main__':
    main()
