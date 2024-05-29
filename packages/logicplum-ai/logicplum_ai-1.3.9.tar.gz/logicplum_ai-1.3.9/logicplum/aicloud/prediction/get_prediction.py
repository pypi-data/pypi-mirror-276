import requests
from ..config import base_url

def read_file(file_path):
    with open(file_path, "rb") as file:
        uploaded_filename = file_path.split('/')[-1]  # Use '/' for UNIX paths
        content = file.read()
        return uploaded_filename, content

def make_request(url, token, method='GET', data=None, files=None):
    access_token = 'Bearer ' + token
    headers = {"Authorization": access_token}
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, data=data, files=files, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

def make_prediction(file_path, endpoint, token, data):
    uploaded_prediction_filename, content = read_file(file_path)
    url = f"{base_url}/prediction/{endpoint}" if endpoint else f"{base_url}/prediction/"
    files = {'prediction_file': (uploaded_prediction_filename, content)}
    return make_request(url, token, method='POST', data=data, files=files)

def aipilot_prediction(file_path, token, deployment_id):
    data = {"deployment_id": deployment_id}
    return make_prediction(file_path, "", token, data)

def quick_prediction(file_path, token, deployment_id):
    data = {"deployment_id": deployment_id}
    return make_prediction(file_path, "quick-predict", token, data)

def manual_prediction(file_path, token, project_id):
    data = {"project_id": project_id}
    return make_prediction(file_path, "manual-predict", token, data)

def comprehensive_prediction(file_path, token, deployment_id):
    data = {"deployment_id": deployment_id}
    return make_prediction(file_path, "comprehensive-predict", token, data)

def get_prediction_result(deployment_or_project_id, token, mode):
    if mode.lower() == "quick":
        url = f"{base_url}/prediction/get-prediction-score/{deployment_or_project_id}"
    else:
        url = f"{base_url}/prediction/get-prediction-score/{deployment_or_project_id}"
    return make_request(url, token)


def cancel_prediction_task(deployment_id, token):
    url = f"{base_url}/prediction/cancel-job/{deployment_id}"
    access_token = 'Bearer '+ token
    headers = {"Authorization": access_token}
    response = requests.get(url, headers=headers)
    if response.status_code != 500 and response.status_code != 400:
        return response.json()
    else:
        return f"Request failed with status code: {response.status_code}"