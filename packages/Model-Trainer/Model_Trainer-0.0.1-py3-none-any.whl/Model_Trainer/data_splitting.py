import os
import random
import shutil
from itertools import islice

class Data_Splitter:

    def __init__(self, data_folder, dest_fold, no_classes):
        self.In_Fold_Path = data_folder   # Enter the absolute folder path where the combine data will save
        self.Out_Fold_Path = dest_fold    # Enter the absolute folder path where the final split data will save
        self.classes_Number = no_classes  # Enter the total number of classes in the data
        self.classes_names = []
        self.classes_paths = []

    def class_path_folder(self):

        for i in range(self.classes_Number):
            class_name = input(f"Enter the Class_Name for {i + 1}th Class: ")
            class_path = input(f"Enter the absolute path of {class_name}: ")
            self.classes_names.append(class_name)
            self.classes_paths.append(class_path)

    def split(self):
        split_ratio = {'train': 0.7, 'valid': 0.2, 'test': 0.1}

        #------------------ Directory Creation ------------------#
        try:
            shutil.rmtree(self.Out_Fold_Path)
            shutil.rmtree(self.In_Fold_Path)
            print("Directory Reset")

        except OSError as e:
            os.mkdir(self.Out_Fold_Path)

        os.makedirs(f"{self.Out_Fold_Path}/train/images", exist_ok=True)
        os.makedirs(f"{self.Out_Fold_Path}/train/labels", exist_ok=True)
        os.makedirs(f"{self.Out_Fold_Path}/test/images", exist_ok=True)
        os.makedirs(f"{self.Out_Fold_Path}/test/labels", exist_ok=True)
        os.makedirs(f"{self.Out_Fold_Path}/valid/images", exist_ok=True)
        os.makedirs(f"{self.Out_Fold_Path}/valid/labels", exist_ok=True)

        #------------------ Data merging to input folder ------------------#

        os.makedirs(self.In_Fold_Path, exist_ok=True)
        for path in self.classes_paths:
            items = os.listdir(path)
            for item in items:
                shutil.copy(os.path.join(path, item), self.In_Fold_Path)

        #------------------ Get the Names ------------------#
        listNames = os.listdir(self.In_Fold_Path)

        unique_names = []
        for name in listNames:
            unique_names.append(name.split('.')[0])
        unique_names = list(set(unique_names))
        no_of_unique = len(unique_names)

        #------------------ Shuffles ------------------#
        random.shuffle(unique_names)

        #------------------ No.of image for train, test and valid ------------------#

        len_train = int(no_of_unique*split_ratio['train'])
        len_valid = int(no_of_unique*split_ratio['valid'])
        len_test = int(no_of_unique*split_ratio['test'])

        #------------------ Remaning Images ------------------#

        if no_of_unique != len_train + len_valid + len_test:
            remaning_images = no_of_unique - (len_train + len_valid + len_test)
            len_train += remaning_images


        #------------------ Remaning Images ------------------#

        length_to_split = [len_train, len_valid, len_test]
        Input = iter(unique_names)
        Output = [list(islice(Input, elem)) for elem in length_to_split]
        print(f'Total Images: {no_of_unique} \nSplit: {len(Output[0])}, {len(Output[1])}, {len(Output[2])}')


        #------------------ Copy Files ------------------#

        Sequence = ['train', 'valid', 'test']
        for i,out in enumerate(Output):
            for filename in out:
                shutil.copy(f'{self.In_Fold_Path}/{filename}.jpg',f'{self.Out_Fold_Path}/{Sequence[i]}/images/{filename}.jpg')
                shutil.copy(f'{self.In_Fold_Path}/{filename}.txt', f'{self.Out_Fold_Path}/{Sequence[i]}/labels/{filename}.txt')

        print("Dataset is splited among test train and valid")

        #------------------ Data.Yaml file content ------------------#

        data_yaml = f'path: {self.Out_Fold_Path}\ntrain: train\images\nval: valid\images\ntest: test\images\n\nnc: {len(self.classes_names)}\nnames1: {self.classes_names}'

        #------------------ Data.Yaml creation ------------------#

        f = open(f'{self.Out_Fold_Path}/data.yaml', 'a')
        f.write(data_yaml)
        print("Data.yaml File is created Successfully!")
        f.close()
