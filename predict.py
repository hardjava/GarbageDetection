import torch
import torchvision.transforms as transforms
from torchvision import models
import torch.nn as nn
from PIL import Image
import matplotlib.pyplot as plt
from pathlib import Path

# ResNet 클래스 정의
class ResNet(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # Pretrained ResNet50 모델
        self.network = models.resnet50(weights=None)  # 사전 학습 사용 안 함
        num_ftrs = self.network.fc.in_features
        self.network.fc = nn.Linear(num_ftrs, num_classes)

    def forward(self, xb):
        return self.network(xb)

# 모델 클래스 정의
model = ResNet(num_classes=6)  # 클래스 수를 동일하게 설정

# 가중치 로드 (CPU 환경에서 로드)
model.load_state_dict(torch.load('MyModel_weights.pth', map_location=torch.device('cpu'), weights_only=True))
model.eval()  # 평가 모드로 전환

# 클래스 레이블 정의
dataset_classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# 이미지 전처리 정의
transformations = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

# 이미지 예측 함수
def predict_image(img, model, classes=dataset_classes):
    # Convert to a batch of 1
    xb = img.unsqueeze(0)  # 배치 차원 추가 (1, C, H, W)
    model = model.to(torch.device('cpu'))  # 모델을 CPU로 강제 이동
    xb = xb.to(torch.device('cpu'))  # 입력 데이터도 CPU로 이동
    # Get predictions from model
    yb = model(xb)
    # Pick index with highest probability
    prob, preds = torch.max(yb, dim=1)
    # Retrieve the class label
    return classes[preds[0].item()], prob[0].item()

# 외부 이미지 파일 예측 함수
def predict_external_image(image_name):
    image = Image.open(Path('./img/' + image_name))

    example_image = transformations(image)
    plt.imshow(example_image.permute(1, 2, 0))  
    predicted_class, probability = predict_image(example_image, model)
    print(f"'{predicted_class}'")
    return predicted_class

# 메인 함수
if __name__ == "__main__":
    image_path = input("Enter the image file path: ")
    predict_external_image(image_path)
