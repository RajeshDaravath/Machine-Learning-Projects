from flask import Flask, jsonify
import os
import shutil
import json
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='./logs/logs.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

# Load configuration from config.json
with open('config.json','r') as f:
    config = json.load(f) 

# Extract required paths from config
output_folder_path = config.get('output_folder_path', '')
prod_deployment_path = config.get('prod_deployment_path', '')
output_model_path = config.get('output_model_path', '')
test_data_path = config.get('test_data_path', '')

def store_model_into_production(path):
    try:
        # List of files to copy
        files_to_copy = [
            'trainedmodel.pkl',  # Assuming this is the model file
            'latestscore.txt',   # File containing latest score
            'ingestedfiles.txt'  # File containing ingested data list
        ]

        # Copy files to the production path
        for filename in files_to_copy:
            src_path = os.path.join(output_folder_path, filename)
            shutil.copy(src_path, path)

        logging.info("SUCCESS: All files moved to production folder")
    except Exception as e:
        logging.error(f"ERROR: Files could not be moved to production folder: {e}")

@app.route("/")
def home():
    return "Welcome to the deployment endpoint!"

@app.route("/deploy", methods=['POST'])
def deploy_model():
    try:
        store_model_into_production(prod_deployment_path)
        return jsonify({"message": "Model deployment successful."}), 200
    except Exception as e:
        logging.error(f"ERROR: Model deployment failed: {e}")
        return jsonify({"error": "Model deployment failed."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
