import torch
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

class ResNet(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.network = models.resnet50(weights=None)
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, num_classes)

    def forward(self, xb):
        return self.network(xb)

model = ResNet(num_classes=6)
model.load_state_dict(torch.load('MyModel_weights.pth', map_location=torch.device('cpu'), weights_only=True))
model.eval()
dataset_classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

transformations = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

def predict_image(img, model, classes=dataset_classes):
    xb = img.unsqueeze(0)
    model = model.to(torch.device('cpu'))
    xb = xb.to(torch.device('cpu'))
    yb = model(xb)
    prob, preds = torch.max(yb, dim=1)
    return classes[preds[0].item()], prob[0].item()

def predict_external_image(image_name):
    image = Image.open(Path('./img/' + image_name))
    example_image = transformations(image)
    plt.imshow(example_image.permute(1, 2, 0))  
    predicted_class, probability = predict_image(example_image, model)
    print(f"'{predicted_class}'")
    return predicted_class