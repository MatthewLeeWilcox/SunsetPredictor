import torch
import torch.nn as nn
from flask import current_app
import os
current_directory = os.getcwd()

path = current_directory + "/src/Model/GeneartorModel"
# Number of workers for dataloader
workers = 8

# Batch size during training
batch_size = 128

# Spatial size of training images. All images will be resized to this
#   size using a transformer.
image_size = 64

# Number of channels in the training images. For color images this is 3
nc = 3

# Size of z latent vector (i.e. size of generator input)
nz = 100

# Size of feature maps in generator
ngf = 64

# Size of feature maps in discriminator
ndf = 64

# Number of training epochs
num_epochs = 25

# Learning rate for optimizers
lr = 0.0002

# Beta1 hyperparameter for Adam optimizers
beta1 = 0.5

# Number of GPUs available. Use 0 for CPU mode.
ngpu = 0


class Generator(nn.Module):
    def __init__(self, ngpu):
        super(Generator, self).__init__()
        self.ngpu = ngpu
        self.weatherInput = nn.Sequential(nn.Linear(21,50), nn.ReLU(),)
        self.inputDense = nn.Sequential(nn.Linear(nz, nz), nn.ReLU(),)
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(nz, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. ``(ngf*8) x 4 x 4``
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. ``(ngf*4) x 8 x 8``
            nn.ConvTranspose2d( ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. ``(ngf*2) x 16 x 16``
            nn.ConvTranspose2d( ngf * 2, ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. ``(ngf) x 32 x 32``
            nn.ConvTranspose2d( ngf, nc, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. ``(nc) x 64 x 64``
        )

    def forward(self, noise, weather):
        # print("GENERATOR:")

        winput = self.weatherInput(weather)
        # print(winput.shape)
        noise = noise.squeeze(-1).squeeze(-1)
        # print(winput.shape)
        inputConcat = torch.cat((noise, winput), dim = 1)
        # print(inputConcat.shape)
        # print("Begin ")
        mod = self.inputDense(inputConcat)
        # print(mod.shape)
        mod = mod.unsqueeze(-1).unsqueeze(-1)
        output = self.main(mod)
        # print(output.shape)
        
        return output
device = torch.device('cpu')
# 1. Load the model
model = Generator(ngpu).to(device)

model.load_state_dict(torch.load(path))


# 2. Instantiate the model
# If the entire model object was saved


# # If only the state dict was saved and you have the model architecture defined elsewhere
# # Example:
# # model = YourModelClass()
# # model.load_state_dict(saved_model)

# # 3. Set model to evaluation mode
model.eval()

# from future_weather_api import get_future_weather
import pandas as pd
import numpy as np 
import cv2
import matplotlib.pyplot as plt
# weather = get_future_weather('01/01/2024')

def genSunsetImage(weather):
    new_column_names = {'{}'.format(col): 'weather_{}'.format(col) for col in weather.columns}
    weather.rename(columns=new_column_names, inplace=True)
    # Get the 13th column
    col_13 = weather.iloc[:, 12]

    # List of all possible weather conditions
    possible_conditions = ['Clear', 'Overcast', 'Partially cloudy', "Rain, Overcast",'Rain, Partially cloudy', 'Snow, Fog', 'Snow, Overcast', "Snow, Partially cloudy"]

    # Create dummy variables with all possible categories
    dummy_df = pd.get_dummies(col_13, columns=possible_conditions)

    weather.iloc[0,0] = -6
    weather = weather.drop(weather.columns[[12,13]],axis = 1)

    # Add missing columns if any
    missing_columns = set(possible_conditions) - set(dummy_df.columns)
    for col in missing_columns:
        dummy_df[col] = 0

    # Sort the columns alphabetically for consistency
    dummy_df = dummy_df.reindex(sorted(dummy_df.columns), axis=1)
    result_df = pd.concat([weather, dummy_df], axis=1)

    print(result_df)
    tdw2 = np.array([result_df.values, result_df.values])
    todayWeatherTorch = torch.from_numpy(tdw2.astype(float)).to(device).float().squeeze(1)

    fixed_noise = torch.randn(2, nz-50, 1, 1, device=device).float()
    print(todayWeatherTorch.shape)
    print(fixed_noise.shape)
    todayImg = model(fixed_noise,todayWeatherTorch).permute(0, 2, 3, 1).cpu().detach().numpy()
    first_image = todayImg[0]

    # Plot the first image
    print(first_image.shape)

    folder_path = os.path.join(current_app.root_path, 'static')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Define the file path for the image
    image_path = os.path.join(folder_path, 'sunset.png')

    plt.imshow(first_image)
    # plt.show
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
    # Save the image using OpenCV
    # cv2.imwrite(image_path, first_image)

    # return first_image


# plt.imshow(genSunsetImage(weather))
# plt.show()