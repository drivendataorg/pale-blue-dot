import os
import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from typing import Dict, List, Tuple, Optional, Any, Union
# Load environment variables from .env file
load_dotenv()


def login(username: str, password: str) -> Optional[str]:
    """
    Perform a login to the AppEEARS API and retrieve the authentication token.

    Args:
    username: The NASA Earthdata Login username.
    password: The NASA Earthdata Login password.

    Returns:
    The authentication token if login is successful; None otherwise.
    """
    url = 'https://appeears.earthdatacloud.nasa.gov/api/login'
    try:
        response = requests.post(url=url, auth=(username, password))
        response.raise_for_status()
        token_info = response.json()
        return token_info.get('token')
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    

def get_products(token: str, pretty: bool = True) -> Optional[Dict[str, Any]]:
    """
    Retrieve the list of available products from the AppEEARS API.

    Args:
    token: The authentication token obtained from the login function.
    pretty: Boolean to toggle pretty JSON formatting.

    Returns:
    A dictionary of available products if successful; None otherwise.
    """
    url = 'https://appeears.earthdatacloud.nasa.gov/api/product'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'pretty': pretty}
    try:
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    

def create_dataframe(products: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Convert a list of product dictionaries into a DataFrame.

    Args:
    products: A list of dictionaries, each representing a product.

    Returns:
    A pandas DataFrame where each row represents a product.
    """
    return pd.DataFrame(products)

def submit_task(token: str, task_params: Dict) -> str:
    """
    Submit a task to the AppEEARS API and return the task ID.

    Args:
        token (str): Authentication token.
        task_params (Dict): Parameters for the task.

    Returns:
        str: Task ID.
    """
    response = requests.post(
        url='https://appeears.earthdatacloud.nasa.gov/api/task',
        json=task_params,
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.json()['task_id']

def check_all_tasks_status(token: str) -> Dict:
    """
    Check the status of all tasks associated with the account.

    Args:
        token (str): Authentication token.

    Returns:
        Dict: Status of all tasks.
    """
    response = requests.get(
        url='https://appeears.earthdatacloud.nasa.gov/api/task',
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.json()

def check_specific_task_status(token: str, task_id: str) -> Dict:
    """
    Check the status of a specific task.

    Args:
        token (str): Authentication token.
        task_id (str): ID of the task to check.

    Returns:
        Dict: Status of the task.
    """
    response = requests.get(
        url=f'https://appeears.earthdatacloud.nasa.gov/api/task/{task_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.json()

def create_and_submit_task(username: str, password: str, task_type: str, task_name: str, start_date: str, end_date: str, product: str, layers: List[str], lat: Union[float, None] = None, long: Union[float, None] = None, file_type: str = 'geotiff', geojson: Union[Dict, None] = None) -> Optional[str]:
    """
    Authenticate, create, and submit a task to the AppEEARS API with more flexibility.

    Args:
        username (str): Username for authentication.
        password (str): Password for authentication.
        task_type (str): Type of the task ('area' or 'point').
        task_name (str): User-defined name of the task.
        start_date (str): Start date in 'MM-DD-YYYY' format.
        end_date (str): End date in 'MM-DD-YYYY' format.
        product (str): Product to use.
        layer (str): Layer of the product.
        lat (float, optional): Latitude for the point task.
        long (float, optional): Longitude for the point task.
        file_type (str): Type of data file (geotiff or netcdf4), default is 'geotiff'.
        geojson (Dict, optional): GeoJSON object for area task.

    Returns:
        Optional[str]: Task ID if task is successfully submitted, None otherwise.
    """
    # Authenticate and get token
    auth_response = requests.post(
        url='https://appeears.earthdatacloud.nasa.gov/api/login',
        auth=(username, password)
    )
    if auth_response.status_code != 200:
        print(f"Authentication failed: {auth_response.json().get('message')}")
        return None

    token = auth_response.json()['token']

    # Define task parameters
    task_params = {
        'task_type': task_type,
        'task_name': task_name,
        'params': {
            'dates': [{'startDate': start_date, 'endDate': end_date}],
            'layers': [{'product': product, 'layer': layer} for layer in layers],
            'output': {'format': {'type': file_type}}
        }
    }

    # Add coordinates for point task
    if task_type == 'point' and lat is not None and long is not None:
        task_params['params']['coordinates'] = [{'latitude': lat, 'longitude': long}]

    # Add GeoJSON for area task
    if task_type == 'area' and geojson is not None:
        task_params['params']['geo'] = geojson

    # Submit the task
    task_id = submit_task(token=token, task_params=task_params)
    return task_id

def list_files_in_bundle(token: str, task_id: str) -> dict:
    """
    List all files in a bundle associated with a given task_id.

    Args:
        token (str): Authentication token.
        task_id (str): Unique identifier for the task.

    Returns:
        dict: Information about the bundle and its files.
    """
    try:
        response = requests.get(
            url=f'https://appeears.earthdatacloud.nasa.gov/api/bundle/{task_id}',  
            headers={'Authorization': f'Bearer {token}'}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def download_file_from_bundle(token: str, task_id: str, file_id: str, file_path: str) -> None:
    """
    Download a file from a bundle using task_id and file_id.

    Args:
        token (str): Authentication token.
        task_id (str): Unique identifier for the task.
        file_id (str): Unique identifier for the file in the bundle.
        file_path (str): Complete file path (including name and extension) where the downloaded file will be saved.

    Returns:
        None: Writes the file to the specified file path.
    """
    try:
        response = requests.get(
            url=f'https://appeears.earthdatacloud.nasa.gov/api/bundle/{task_id}/{file_id}',  
            headers={'Authorization': f'Bearer {token}'}, 
            allow_redirects=True,
            stream=True
        )
        response.raise_for_status()

        # Create the directory for the file if it does not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            for data in response.iter_content(chunk_size=8192):
                f.write(data)
        print(f"File downloaded successfully: {file_path}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")



import csv
from typing import List

import csv
from typing import List, Union, Optional

def read_last_processed_index(file_path: str) -> int:
    """
    Reads the last processed index from a file.

    Args:
        file_path (str): Path to the file containing the last processed index.

    Returns:
        int: The last processed index. Returns -1 if the file does not exist or is empty.
    """
    try:
        with open(file_path, 'r') as file:
            last_index = file.readline()
            return int(last_index.strip()) if last_index else -1
    except FileNotFoundError:
        return -1



def process_csv_and_submit_tasks(csv_file: str, 
                                 results_csv: str,
                                 username: str, 
                                 password: str, 
                                 task_type: str, 
                                 base_task_name: str, 
                                 start_date: str, 
                                 end_date: str, 
                                 product: str, 
                                 file_type: str, 
                                 layers: List[str],
                                 geojson: Optional[Dict] = None,
                                 last_processed_file: str = 'last_processed.txt'
                                 ) -> None:
    """
    Reads a CSV file, submits a task for each row, and saves results to a CSV file.
    """
    last_processed_index = read_last_processed_index(last_processed_file)

    with open(csv_file, mode='r') as file, open(results_csv, mode='a', newline='') as results_file:
        csv_reader = csv.DictReader(file)
        results_writer = csv.DictWriter(results_file, fieldnames=['Index', 'Latitude', 'Longitude', 'Task_ID'])
        
        # Check if the results file is empty and write the header if it is
        results_file.seek(0, os.SEEK_END)
        if results_file.tell() == 0:
            results_writer.writeheader()

        for index, row in enumerate(csv_reader):
            if index <= last_processed_index:
                continue  # Skip already processed rows

            # Procesamiento de las coordenadas
            if 'Latitude' in row and 'Longitude' in row:
                latitude = float(row['Latitude'])
                longitude = float(row['Longitude'])
            elif 'lat' in row and 'long' in row:
                latitude = float(row['lat'])
                longitude = float(row['long'])
            else:
                print(f"Latitude and Longitude columns not found in row: {row}")
                continue  # Skip to the next row

            # Uso del índice como ID de ubicación
            location_id = index
            task_name = f"{location_id}-{base_task_name}"

            # Llamada a create_and_submit_task (asegúrate de que esta función exista en tu código)
            task_id = create_and_submit_task(
                username=username,
                password=password,
                task_type=task_type,
                task_name=task_name,
                start_date=start_date,
                end_date=end_date,
                product=product,
                layers=layers,
                lat=latitude,
                long=longitude,
                file_type=file_type,
                geojson=geojson
            )

            print(f"Submitted task for Index {location_id}, coordinates ({latitude}, {longitude}). Task ID: {task_id}")

            # Escribir en el CSV de resultados
            results_writer.writerow({'Index': location_id, 'Latitude': latitude, 'Longitude': longitude, 'Task_ID': task_id})
            results_file.flush()

            # Pausa después de cada 100 filas
            if index % 100 == 0 and index != 0:
                print("Processing paused for 60 seconds to prevent overload.")
                time.sleep(60)  # Pause for 60 seconds

            # Actualizar el archivo de último índice procesado después de cada fila
            with open(last_processed_file, 'w') as f:
                f.write(str(index))

    return results_writer

def save_task_ids_to_csv(task_data: List[dict], 
                         output_csv: str
                         ) -> None:
    """
    Saves task IDs along with IDs and coordinates to a CSV file.

    Args:
        task_data (List[dict]): List of dictionaries containing IDs, coordinates, and task IDs.
        output_csv (str): Path to the output CSV file.

    Returns:
        None
    """
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'Latitude', 'Longitude', 'Task_ID'])
        writer.writeheader()
        for data in task_data:
            writer.writerow(data)
    print(f"Task IDs saved to {output_csv}")


import csv
import os

def download_and_save_results(tasks_csv: str, destination_dir: str, token: str):
    """
    Reads tasks from a CSV file, downloads the first file in each task's bundle, and saves it.

    Args:
        tasks_csv (str): Path to the CSV file containing task details.
        destination_dir (str): Directory where result files will be saved.
        token (str): Authentication token.

    Returns:
        None
    """
    with open(tasks_csv, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            task_id = row['Task_ID']
            location_id = row['ID']
            print(f"Processing Task ID: {task_id} for Location ID: {location_id}")

            # Get the list of files in the bundle
            bundle_files = list_files_in_bundle(token=token, task_id=task_id)
            if bundle_files and 'files' in bundle_files and len(bundle_files['files']) > 0:
                # Assuming the first file is the desired file
                file_id = bundle_files['files'][0]['file_id']

                # Define destination file path (corrected)
                dest_file_path = os.path.join(destination_dir, f"{location_id}.csv")

                # Ensure the destination directory exists
                os.makedirs(destination_dir, exist_ok=True)

                # Download the file
                download_file_from_bundle(token=token, task_id=task_id, file_id=file_id, file_path=dest_file_path)
                print(f"Downloaded file for Location ID: {location_id} to {dest_file_path}")
            else:
                print(f"No files found for Task ID: {task_id}")