import os

def create_business_folder(name, location):
    
    # Create a folder for the business
    folder_name = f"{name}_{location}"
    folder_path = os.path.join("businesses", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    return folder_path