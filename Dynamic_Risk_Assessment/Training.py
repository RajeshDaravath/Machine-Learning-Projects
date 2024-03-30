import pandas as pd
import pickle
import os
from sklearn.linear_model import LogisticRegression
import json

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def train_model(dataset_csv_path, model_path):
    """Train the logistic regression model and save it to the specified path."""
    lr = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                            intercept_scaling=1, l1_ratio=None, max_iter=100,
                            n_jobs=None, penalty='l2',
                            random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                            warm_start=False)
    
    df = pd.read_csv(dataset_csv_path)
    X = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    y = df['exited']

    lr.fit(X, y)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(lr, f)

def main():
    config = load_config('config.json')

    output_model_path = config['output_model_path']
    output_folder_path = config['output_folder_path']
    final_data_name = config['final_data_name']
    trained_model_name = config["trained_model_name"]

    dataset_csv_path = os.path.join(output_folder_path, final_data_name) 
    model_path = os.path.join(output_model_path, trained_model_name)

    train_model(dataset_csv_path, model_path)

if __name__ == '__main__':
    main()
