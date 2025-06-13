import pandas as pd

def load_project_inputs(file_path):
    df = pd.read_excel(file_path, sheet_name="Factory Project Drivers")
    return df
