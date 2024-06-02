from ultralytics import YOLO
import os
import shutil
import torch
class YOLO_Trainer:
    def __init__(self, Data_yaml_fold_path, Best_Weight_dest, epochs=50):
        self.path = Data_yaml_fold_path
        self.destination = Best_Weight_dest
        self.model = None
        self.epochs = epochs

    def model_selection(self):
        while True:
            model_version = input("Enter the YOLO version (5 or 8): ")
            model_name = input("Enter the name for the model (e.g., 'n', 's', 'm', 'l', 'x'): ")
            if model_version in ['5', '8'] and model_name in ['n', 's', 'm', 'l', 'x']:
                self.model = YOLO(f'Models/yolov{model_version}{model_name}.pt')
                break
            else:
                print('Please choose the correct model name and version!')

    def model_training(self):
        if torch.cuda.is_available():
            print(f"⚡⚡⚡⚡ Running on GPU and CUDA Device Name: {torch.cuda.get_device_name(0)} ⚡⚡⚡⚡")
        else:
            print("⚠️⚠️⚠️ CUDA is NOT available. Please ensure that GPU drivers are properly installed and configured ⚠️⚠️⚠️")

        if self.model is not None:
            self.model.train(data=f'{self.path}/data.yaml', epochs=self.epochs)
        else:
            print("Model is not selected. Please select a model first.")

    def model_saving(self):
        runs_dir = os.path.join('runs', 'detect')
        latest_run = sorted(os.listdir(runs_dir))[-1]
        best_weights = os.path.join(runs_dir, latest_run, 'weights', 'best.pt')

        if os.path.exists(best_weights):
            if not os.path.exists(self.destination):
                os.makedirs(self.destination)
            shutil.copy(best_weights, self.destination)
            print(f'Best weights copied to {self.destination}')
        else:
            print('Best weights file not found.')
