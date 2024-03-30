import pandas as pd
import timeit
import os
import json
import pickle
import subprocess
from collections import defaultdict

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

config = load_config('config.json')

prod_deployment_path = config["prod_deployment_path"]
output_folder_path = config['output_folder_path']
test_data_path = config["test_data_path"]
trained_model_name = config["trained_model_name"]
final_data_name = config["final_data_name"]
test_data_name = config["test_data_name"]

deployed_model_path = os.path.join(prod_deployment_path, trained_model_name)
dataset_csv_path = os.path.join(output_folder_path, final_data_name)
test_data_file_path = os.path.join(test_data_path, test_data_name)

def model_predictions(test_data_file_path):
    """Get model predictions."""
    model = pickle.load(open(deployed_model_path, 'rb'))
    df = pd.read_csv(test_data_file_path)
    X_test = df[['lastmonth_activity', 'lastyear_activity', 'number_of_employees']]
    return model.predict(X_test).tolist()

def dataframe_summary():
    """Calculate summary statistics."""
    df = pd.read_csv(dataset_csv_path)
    return df.describe().iloc[1:3].append(pd.DataFrame([df.median()], index=['median']))

def dataframe_missing():
    """Calculate the percentage of missing data."""
    df = pd.read_csv(dataset_csv_path)
    return (df.isna().sum() / len(df)).tolist()

def execution_time():
    """Calculate the execution time of ingestion and training."""
    start_time = timeit.default_timer()
    subprocess.run(['python', 'ingestion.py'], check=True)
    ingestion_time = timeit.default_timer() - start_time

    start_time = timeit.default_timer()
    subprocess.run(['python', 'training.py'], check=True)
    training_time = timeit.default_timer() - start_time

    return [ingestion_time, training_time]

def dependencies_checking():
    """Check module dependencies."""
    modules_dict = defaultdict(dict)
    subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, check=True)

    with open('requirements.txt', 'r') as f:
        modules = f.read().splitlines()

    for module in modules:
        module_name, current_version = module.split('==')
        latest_version = subprocess.run(['pip', 'show', module_name], stdout=subprocess.PIPE, check=True)
        for line in latest_version.stdout.decode().split('\n'):
            if line.startswith('Version:'):
                latest_version = line.split(': ')[1]
                break
        modules_dict[module_name] = {'current_version': current_version, 'latest_version': latest_version}

    with open('dependencies.json', 'w') as f:
        json.dump(modules_dict, f)

    return pd.DataFrame.from_dict(modules_dict, orient='index')

if __name__ == '__main__':
    print("Model Prediction:\n", model_predictions(test_data_file_path))
    print("-----------------------------------------")

    print("Dataframe Summary:\n", dataframe_summary())
    print("-----------------------------------------")

    print("Dataframe Missing:\n", dataframe_missing())
    print("-----------------------------------------")

    print("Execution Time:\n", execution_time())
    print("-----------------------------------------")

    print("Dependencies Checking:\n", dependencies_checking())
