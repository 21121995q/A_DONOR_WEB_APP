import torch
from torchvision import transforms, models
from PIL import Image
import time

def load_model():
    model = models.mobilenet_v2(pretrained=False)
    model.features[0][0] = torch.nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
    model.classifier[1] = torch.nn.Linear(model.last_channel, 4)
    
    # Загрузка модели и перевод ее на CPU
    state_dict = torch.load('best_certificate_orientation_model.pth', map_location=torch.device('cpu'))
    model.load_state_dict(state_dict)
    model.to(torch.device('cpu'))
    model.eval()
    return model

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize(512),
        transforms.CenterCrop(512),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485], std=[0.229])
    ])
    
    image = Image.open(image_path).convert('L')  # Конвертация в оттенки серого
    return transform(image).unsqueeze(0)

def predict(image_path):
    model = load_model()
    image = preprocess_image(image_path)
    
    start_time = time.time()
    with torch.no_grad():
        output = model(image)
    end_time = time.time()
    
    inference_time = end_time - start_time
    
    probabilities = torch.softmax(output, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0][predicted_class].item()
    
    class_names = ['0 градусов', '90 градусов', '180 градусов', '270 градусов']
    prediction = class_names[predicted_class]
    
    return prediction, confidence, inference_time