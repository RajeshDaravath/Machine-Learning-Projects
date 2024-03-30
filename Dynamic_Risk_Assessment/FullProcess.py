import json
import os
import subprocess
import scoring

def load_config(config_file):
    """Load configuration from a JSON file."""
    with open(config_file, 'r') as f:
        return json.load(f)

def check_new_data(input_folder_path, ingested_files_path):
    """Check for new data by comparing files in the input folder with ingested files list."""
    with open(ingested_files_path) as f:
        ingested_files_list = f.read().splitlines()

    for file_name in os.listdir(input_folder_path):
        file_path = os.path.join(input_folder_path, file_name)
        if file_path not in ingested_files_list:
            return True
    return False

def main():
    config = load_config('config.json')

    input_folder_path = config['input_folder_path']
    output_folder_path = config['output_folder_path']
    prod_deployment_path = config['prod_deployment_path']
    trained_model_name = config["trained_model_name"]
    ingested_files_name = config['ingested_files_name']
    latest_score_name = config["latest_score_name"]

    deployed_model_path = os.path.join(prod_deployment_path, trained_model_name)
    ingested_files_path = os.path.join(prod_deployment_path, ingested_files_name)
    latest_score_path = os.path.join(prod_deployment_path, latest_score_name)

    if check_new_data(input_folder_path, ingested_files_path):
        print("New data found. Ingest new datasets from", input_folder_path)
        subprocess.call(['python', 'ingestion.py'])
    else:
        print("No new data found. Exiting the process.")
        return

    with open(latest_score_path, 'r') as f:
        latest_score = float(f.read())

    final_data_name = config['final_data_name']
    final_data_path = os.path.join(output_folder_path, final_data_name)
    new_score = scoring.score_model(deployed_model_path, final_data_path)

    print('Latest score: {}, score on newly ingested data: {}'.format(latest_score, new_score))

    if new_score < latest_score:
        print('Detected model drift. Retrain and redeploy model')
        subprocess.call(['python', 'training.py'])
        subprocess.call(['python', 'scoring.py'])
        subprocess.call(['python', 'deployment.py'])
    else:
        print('No model drift detected.')

    subprocess.call(['python', 'diagnostics.py'])
    subprocess.call(['python', 'reporting.py'])
    subprocess.call(['python', 'apicalls.py'])

if __name__ == '__main__':
    main()
