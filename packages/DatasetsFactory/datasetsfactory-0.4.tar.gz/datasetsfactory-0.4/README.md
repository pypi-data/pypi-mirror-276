# DatasetsFactory

This library is meant to DatasetsFactory app users, and is used for loading the available datasets locally!
<br>
It is user-friendly and easy to use! 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install DatasetsFactory.

```bash
pip install DatasetsFactory
```

## Usage
> [!IMPORTANT] 
> Everytime you want to load a dataset you must follow every step bellow !
```python
from DatasetsFactory import Datasets
# Get the token from your profile!
token = "928e4f5f-50e7-4f06-aaac-459d4c5db8ac"
# Initialize the library with the token of the user
init_dataset = Datasets(token)

# Visualize the datasets on which you have privileges
init_dataset.view_datasets() # -> return None

# Load locally only one dataset at a time!
init_dataset("name_of_dataset_from_previous_visualization") # -> return A list with paths to every file from the dataset loaded!
```

## License

[MIT License](https://choosealicense.com/licenses/mit/)
Copyright (c) 2024  DatasetsFactory


