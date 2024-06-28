import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader, TensorDataset
from torch import nn
from transformers import BertTokenizer, BertModel
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import re
from matplotlib import font_manager
import time

# 데이터 로딩 및 전처리
def load_data(train_path, test_path, sheet_name='Sheet1'):
    train_df = pd.read_excel(train_path, sheet_name=sheet_name)
    test_df = pd.read_excel(test_path, sheet_name=sheet_name)
    train_df['사람문장1'] = train_df['사람문장1'].apply(preprocess_text)
    test_df['사람문장1'] = test_df['사람문장1'].apply(preprocess_text)
    return train_df, test_df

def preprocess_text(text):
    return re.sub(r"[^가-힣a-zA-Z0-9 ]", "", re.sub(r'\s+', ' ', text)).strip()

# 토큰화 및 인코딩
def tokenize_and_encode(sentences, tokenizer, max_length=64):
    input_ids, attention_masks = [], []
    for sent in sentences:
        encoded_dict = tokenizer.encode_plus(
            sent, add_special_tokens=True, max_length=max_length,
            pad_to_max_length=True, return_attention_mask=True, return_tensors='pt'
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])
    return torch.cat(input_ids, dim=0), torch.cat(attention_masks, dim=0)

# 모델 정의 및 최적화
class BertClassifier(nn.Module):
    def __init__(self, bert, num_labels):
        super(BertClassifier, self).__init__()
        self.bert = bert
        self.dropout = nn.Dropout(p=0.1)
        self.linear = nn.Linear(bert.config.hidden_size, num_labels)

    def forward(self, input_id, mask):
        outputs = self.bert(input_id, attention_mask=mask)
        dropout_output = self.dropout(outputs.pooler_output)
        return self.linear(dropout_output)

def init_model_and_optimizer(num_labels, learning_rate=2e-5):
    model = BertClassifier(BertModel.from_pretrained('klue/bert-base'), num_labels)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    return model, optimizer

# 훈련 및 평가
def train_model(model, optimizer, train_loader, loss_fn, num_epochs=3):
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            batch_input_ids, batch_attention_mask, batch_labels = batch
            optimizer.zero_grad()
            outputs = model(batch_input_ids, batch_attention_mask)
            loss = loss_fn(outputs, batch_labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_loader)}")

def evaluate_model(model, test_loader, y_test_encoded, label_encoder):
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for batch in test_loader:
            batch_input_ids, batch_attention_mask, batch_labels = batch
            outputs = model(batch_input_ids, batch_attention_mask)
            predictions = torch.argmax(outputs, dim=1)
            y_true.extend(batch_labels.tolist())
            y_pred.extend(predictions.tolist())
    cm = confusion_matrix(y_true, y_pred, labels=np.unique(y_test_encoded))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
    disp.plot(cmap=plt.cm.Blues)
    plt.show()

# 폰트 설정
def set_font(font_path='C:/Windows/Fonts/malgun.ttf'):
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)

# 모델 저장 및 불러오기
def save_model(model, optimizer, label_encoder, file_name='bert_sentiment_model.pth'):
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'label_encoder': label_encoder
    }, file_name)

def load_model(file_name='bert_sentiment_model.pth'):
    checkpoint = torch.load(file_name)
    model, optimizer = init_model_and_optimizer(len(checkpoint['label_encoder'].classes_))
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    label_encoder = checkpoint['label_encoder']
    return model, optimizer, label_encoder

# 예측
def predict_sentiment(text, model, tokenizer, label_encoder):
    model.eval()
    with torch.no_grad():
        preprocessed_text = preprocess_text(text)
        encoded_dict = tokenizer.encode_plus(
            preprocessed_text, add_special_tokens=True, max_length=64,
            pad_to_max_length=True, return_attention_mask=True, return_tensors='pt'
        )
        input_id = encoded_dict['input_ids']
        attention_mask = encoded_dict['attention_mask']
        output = model(input_id, attention_mask)
        prediction = torch.argmax(output, dim=1)
        predicted_label = label_encoder.inverse_transform(prediction.numpy())[0]
        return predicted_label


def train_model(model, optimizer, train_loader, loss_fn, num_epochs=3):
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        start_time = time.time()  # 각 에폭의 시작 시간
        print(f"Training started for epoch {epoch + 1}")

        for batch_idx, batch in enumerate(train_loader):
            batch_input_ids, batch_attention_mask, batch_labels = batch
            optimizer.zero_grad()
            outputs = model(batch_input_ids, batch_attention_mask)
            loss = loss_fn(outputs, batch_labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            # 현재 배치 처리 상태를 10개 배치마다 출력
            if (batch_idx + 1) % 10 == 0:
                print(f"Batch {batch_idx + 1}/{len(train_loader)} processed.")

        elapsed_time = time.time() - start_time  # 에폭 처리 시간 계산
        print(f"Epoch {epoch + 1} completed in {elapsed_time:.2f} seconds with Loss: {total_loss / len(train_loader)}")

def train_predict():
    # 설정된 경로에 따라 데이터 로드
    train_path = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/sentences/감성대화말뭉치(최종데이터)_Training.xlsx'
    test_path = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/sentences/감성대화말뭉치(최종데이터)_Validation.xlsx'
    # 설정된 경로에 따라 데이터 로드
    print("Loading data...")
    train_df, test_df = load_data(train_path, test_path)

    print("Preparing tokenizer and label encoder...")
    tokenizer = BertTokenizer.from_pretrained('klue/bert-base')
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(train_df['감정_대분류'])
    y_test_encoded = label_encoder.transform(test_df['감정_대분류'])

    print("Tokenizing and preparing data loaders...")
    X_train_ids, X_train_masks = tokenize_and_encode(train_df['사람문장1'], tokenizer)
    X_test_ids, X_test_masks = tokenize_and_encode(test_df['사람문장1'], tokenizer)

    train_data = TensorDataset(X_train_ids, X_train_masks, torch.tensor(y_train_encoded).long())
    test_data = TensorDataset(X_test_ids, X_test_masks, torch.tensor(y_test_encoded).long())
    train_loader = DataLoader(train_data, batch_size=32*16)
    test_loader = DataLoader(test_data, batch_size=32*16)

    print("Initializing model and optimizer...")
    model, optimizer = init_model_and_optimizer(len(label_encoder.classes_))

    print("Starting training process...")
    train_model(model, optimizer, train_loader, nn.CrossEntropyLoss(), num_epochs=3)

    print("Evaluating model...")
    evaluate_model(model, test_loader, y_test_encoded, label_encoder)

    print("Saving model...")
    save_model(model, optimizer, label_encoder, 'bert_sentiment_model.pth')

    print("Loading model...")
    model, optimizer, label_encoder = load_model('bert_sentiment_model.pth')

    print("Running prediction...")
    input_text = "오늘 정말 행복한 날이네요!"
    predicted_emotion = predict_sentiment(input_text, model, tokenizer, label_encoder)
    print("Predicted Emotion:", predicted_emotion)


def bertPredict(input_text):
    # print("Running prediction...")
    # input_text = "오늘 정말 행복한 날이네요!"
    tokenizer = BertTokenizer.from_pretrained('klue/bert-base')
    model, optimizer, label_encoder = load_model('bert_sentiment_model.pth')
    predicted_emotion = predict_sentiment(input_text, model, tokenizer, label_encoder)
    print("Predicted Emotion:", predicted_emotion)
    return predicted_emotion