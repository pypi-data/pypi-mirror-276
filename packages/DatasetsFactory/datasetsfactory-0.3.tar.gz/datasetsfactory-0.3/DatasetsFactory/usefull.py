import os


class CreateDirectory:

    def __init__(self, dir_name=None):
        self.path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Datasets")
        self.dir_name = dir_name
        if dir_name is not None:
            self.path_maker = os.path.join(self.path, self.dir_name)

    def make_folder(self):
        """
        Creeaza un folder unde vor fi salvate fisierele
        :return: None
        """
        if self.dir_name is None:
            # Verificam sa nu existe acel folder
            if not os.path.exists(self.path):
                os.mkdir(self.path)
                # print(f"Directory {os.path.basename(self.path)} has been successfully created!")
            else:
                pass
                # print(f"Directory {os.path.basename(self.path)} exists!")
        else:
            if os.path.exists(self.path_maker):
                # print(f'Directory {self.dir_name} has been already created!')
                return self.path_maker
            else:
                os.mkdir(self.path_maker)
                # print(f"Directory {self.dir_name} has been successfully created!")
                return self.path_maker
