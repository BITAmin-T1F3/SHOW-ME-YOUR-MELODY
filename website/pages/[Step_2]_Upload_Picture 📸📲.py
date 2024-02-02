import streamlit as st
from PIL import Image
import io
import numpy as np
import torch
import torchvision.models as models
import torch.nn as nn
from torchvision.transforms import transforms
from torchvision.models import resnet50
import dlib
import cv2

st.set_page_config(page_title="#SHOW_ME_YOUR_MELODY", page_icon="🌃🎧")

st.markdown('<h2 style="text-align:center;">[Step 2] Upload Picture 📸📲</h2>', unsafe_allow_html=True)
st.markdown("""
    <style>
        .big-font {
            font-size: 20px !important;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# classes
background_classes = ['공연장', '공원', '공항', '기차', '도시_낮',
                '도시_밤', '바다_낮', '바다_밤', '설원', '스포츠경기장',
                '시골', '음식점', '카페', '칵테일바', '포차', '노을',
                '밝은하늘', '밤하늘', '헬스장']

emotion_classes = ["Happy", "Neutral", "Sad", "Surprising"]

nb_classes = len(emotion_classes)
class CustomResNet50(nn.Module):
    def __init__(self):
        super(CustomResNet50, self).__init__()
        self.resnet50 = resnet50(pretrained=False)
        in_features = self.resnet50.fc.in_features
        self.fc = nn.Linear(in_features, nb_classes)

    def forward(self, x):
        x = self.resnet50(x)
        x = self.fc(x)
        return x

def load_model(device):
    # Load the background classification model
    model_path = 'resnet50_best_adamW.pth'
    model = models.resnet50(pretrained=False)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(background_classes))
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint)
    model = model.to(device)
    model.eval()

    # Load the emotion classification model
    face_model = torch.load('emotion_classification.pth')
    face_model = face_model.to(device)  # Initialize the model and send it to the device
    face_model.eval()

    return model, face_model


def preprocess_image(uploaded_file, device):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_image = Image.open(uploaded_file).convert("RGB")
    input_tensor = transform(input_image).unsqueeze(0)  # Add batch dimension
    input_tensor = input_tensor.to(device)
    
    #st.image(input_image, caption="Uploaded Image")

    return input_tensor

# 배경 분류
def classify_background(model, image_tensor, background_classes):
    with torch.no_grad():
        output = model(image_tensor)
    predicted_class_index = torch.argmax(output, dim=1).item()
    background = background_classes[predicted_class_index]
    
    st.markdown(f"<strong><p class='big-font' style='text-align: center;'>🌃 Predicted background label: {background}</p></strong>", unsafe_allow_html=True)
    st.session_state.background_result = background

    return background

# 감정 분류
def classify_emotion(model, pil_image, emotion_classes, device):
    # Convert PIL Image to OpenCV format
    frame = np.array(pil_image)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Convert color to gray scale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Face detection using Dlib
    detector = dlib.get_frontal_face_detector()
    faces = detector(gray)

    if len(faces) > 0:
        # Process each face found
        for face in faces:
            fX, fY, fW, fH = face.left(), face.top(), face.width(), face.height()

            # Crop and resize the face region
            face_roi = frame[fY:fY + fH, fX:fX + fW]
            face_roi = cv2.resize(face_roi, (224, 224))
            face_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)

            # Convert to PyTorch tensor with correct shape and channels
            face_tensor = transforms.Compose([
                transforms.ToPILImage(),
                transforms.ToTensor(),
            ])(face_roi).unsqueeze(0).to(device)

            # Emotion prediction using PyTorch model
            model.eval()
            with torch.no_grad():
                outputs = model(face_tensor)
                _, preds = torch.max(outputs, 1)
                label = emotion_classes[preds.item()]

            # Draw a rectangle around the face and put the label
            cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (0, 255, 0), 2)
            cv2.putText(frame, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

        # Convert BGR image to RGB for display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the image using Streamlit
        st.image(frame_rgb, caption="Uploaded Image")

        if label == 'Happy':
            emoticon = '😊'
        elif label == 'Neutral':
            emoticon = '😐'
        elif label == 'Sad':
            emoticon = '😭'
        elif label == 'Surprised':
            emoticon = '🫢'
        
        st.markdown(f"<strong><p class='big-font' style='text-align: center;'>Predicted emotion label: {label} {emoticon}</p></strong>", unsafe_allow_html=True)
        st.session_state.emotion_result = label

    else:
        st.write("No face detected in the image.")


# Create a file uploader widget
uploaded_file = st.file_uploader("📸 인스타그램에 올리고싶은 이미지를 업로드해주시길 바랍니다!", type=['png', 'jpg', 'jpeg'])

# device
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

# models
background_model, face_model = load_model(device)

# predict background & emotion
if uploaded_file is not None:
    # Preprocess the image and predict the background and emotion
    processed_image = preprocess_image(uploaded_file, device)
    background_label = classify_background(background_model, processed_image, background_classes)
    image = Image.open(uploaded_file).convert("RGB")
    emotion_label = classify_emotion(face_model, image, emotion_classes, device)
else:
    st.warning("Please upload an image before processing.")