import pandas as pd
import uuid
import requests
from datetime import datetime


def check_nested_dict(nested_dict:dict, keys_list:list)->bool:
    """
    Helper function to recursively search for keys in a nested dictionary.
    
    Args:
        nested_dict (dict): The dictionary to search.
        keys_list (list): The list of keys to check for.
    
    Returns:
        bool: True if all keys are found, False otherwise.
    """
    for keys in keys_list:
        temp_dict = nested_dict
        for key in keys:
            if key in temp_dict:
                temp_dict = temp_dict[key]
            else:
                break
        else:
            return True
    return False


def convert_df_to_csv(df: pd.DataFrame, encoding:str = 'utf-8', sep:str = '\t', index=False):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv(encoding=encoding, sep=sep, index=index)


def generate_filename(station:str, name:str ):
    # Generate a global unique ID
    unique_id = uuid.uuid4()
    
    # Get the current date and time
    now = datetime.now()
    
    # Format date and time as a string with no spaces or special characters
    date_time_str = now.strftime("%Y-%m-%dT%H%M%S")
    
    # Combine all parts to form the final string
    filename = f"{date_time_str}_{station}_{name}_{unique_id}.dat"
    
    return filename


def fetch_markdown_instructions_from_github(url:str = "https://raw.githubusercontent.com/SITES-spectral/sstc-fixedsensors/main/src/sstc_fixedsensors/app/instructions.md"):
    # TODO: Move the instru
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None