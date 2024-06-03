import os
from requests import get
from usefull import CreateDirectory


class Datasets:

    def __init__(self, token):
        _urlsite_ = "http://localhost/routes"
        # Link-ul catre endpoint-ul de listare a dataseturilor!
        self.url_list_datasets = f"{_urlsite_}/datasets/list-all/{token}"
        # Link-ul catre endpoint-ul de listare a dataseturilor!
        self.url_load_dataset = f"{_urlsite_}/load/dataset/{token}"
        # Cream un folder la instantiere Datasets unde vom salva toate dataseturile
        folder = CreateDirectory()
        folder.make_folder()
        # Punem caile fiecarui fisier intr-o lista
        self.paths = list()
        # Pastram detaliile din request-ul view_datasets
        self.data_request = None

    def view_datasets(self):
        """
        Make a GET request and retrieve all datasets available for the user with a valid token!
        :return: The list with details of every dataset
        """
        print(f'Establishing connection to url: {self.url_list_datasets}')
        get_datasets = get(self.url_list_datasets)
        print(f'Response code: {get_datasets.status_code}')
        if not get_datasets.ok:
            print(f'Error:\n\t{get_datasets.text}')
        else:
            print(f'Your datasets are: ')
            for dataset in get_datasets.json():
                for key, val in dataset.items():
                    print(f'{key} -> {len(val)} files')
            self.data_request = get_datasets.json()

    def load_dataset(self, details, dataset_name):
        """
        This method load datasets locally!
        :param details: The list which is returned by the method view_datasets!
        :param dataset_name: The name of the dataset you want to load locally!
        :return: None
        """
        flag = 0
        # Cautam datasetul in lista de dictionare primita prin request-ul anterior
        for dataset in details:
            name = list(dataset.keys())
            if dataset_name == name[0]:
                # Prima data ne asiguram ca avem creat un folder unde sa salvam fisierele
                mk_folder = CreateDirectory(dataset_name)
                path_to_dir = mk_folder.make_folder()

                if len(dataset[dataset_name]) != 0:
                    for file in dataset[dataset_name]:
                        id_file = list(file.keys())
                        url_endpoint = self.url_load_dataset + "/" + id_file[0]
                        get_file = get(url_endpoint)
                        abs_path_to_file = os.path.join(path_to_dir, file[id_file[0]])
                        if get_file.ok:
                            if not os.path.exists(abs_path_to_file):
                                self.paths.append({file[id_file[0]]: abs_path_to_file})
                                with open(abs_path_to_file, "wb") as f:
                                    f.write(get_file.content)
                            else:
                                flag = 2
                                self.paths.append({file[id_file[0]]: abs_path_to_file})
                        else:
                            print(f'Something went wrong on server! Error response: {get_file}')
                            flag = 1
                else:
                    print(f'The dataset {dataset_name} has no file!')
                    flag = 1
            else:
                continue
        if flag == 2:
            print(f"The dataset {dataset_name} has been already loaded!")

        if not self.paths and flag == 0:
            print("The dataset you want to load doesn\'t exist!")

    def __call__(self, dataset_name):
        self.load_dataset(self.data_request, dataset_name)
        return self.paths

