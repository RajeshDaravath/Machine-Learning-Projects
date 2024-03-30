from flask import Flask, request
import json
import os
import diagnostics
import scoring

app = Flask(__name__)

with open('custom_config.json','r') as f:
    custom_config = json.load(f) 

custom_output_folder_path = custom_config["custom_output_folder_path"]
custom_prod_deployment_path = custom_config['custom_prod_deployment_path']
custom_test_data_path = custom_config['custom_test_data_path']
custom_final_data_name = custom_config["custom_final_data_name"]
custom_trained_model_name = custom_config["custom_trained_model_name"]
custom_test_data_name = custom_config["custom_test_data_name"]

custom_dataset_csv_path = os.path.join(custom_config['custom_output_folder_path'], custom_final_data_name) 
custom_deployed_model_path = os.path.join(custom_config['custom_prod_deployment_path'], custom_trained_model_name)
custom_test_data_file_path = os.path.join(custom_config['custom_test_data_path'], custom_test_data_name)


@app.route("/custom_prediction", methods=['POST','OPTIONS'])
def custom_predict():        
    custom_test_data_file_path = request.form.get('path')
    result = diagnostics.model_predictions(custom_test_data_file_path[1:-1])
    return json.dumps([int(item) for item in result])


@app.route("/custom_scoring", methods=['GET','OPTIONS'])
def custom_score():        
    f1_score = scoring.score_model(custom_deployed_model_path, custom_test_data_file_path)
    return json.dumps(f1_score)


@app.route("/custom_summarystats", methods=['GET','OPTIONS'])
def custom_summary():        
    df_stat = diagnostics.dataframe_summary()
    return df_stat.to_dict()


@app.route("/custom_diagnostics", methods=['GET','OPTIONS'])
def custom_diagnose():        
    timing = diagnostics.execution_time()
    na_percents = diagnostics.dataframe_missing()
    if os.path.isfile('custom_dependencies.json'):
        dependencies = json.load(open('custom_dependencies.json'))
    else:
        dependencies = diagnostics.dependencies_checking().to_dict('records')
    diagnose_dict = {
        'timing': timing,
        'na_percents': na_percents,
        'dependencies': dependencies
    }
    return json.dumps(diagnose_dict)


if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
