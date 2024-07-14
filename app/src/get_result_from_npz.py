import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Embedding, TransformerEncoder, TransformerEncoderLayer, Linear, Conv2d, ZeroPad2d
import torch.utils.data as Data

import warnings
warnings.filterwarnings("ignore")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('device', device)

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.embedder1 = Embedding(num_embeddings=316, embedding_dim=16)
        self.embedder2 = Embedding(num_embeddings=289, embedding_dim=8)

        self.cnn1_1 = Conv2d(in_channels=1, out_channels=128, kernel_size=(3, 16), stride=1, padding=(1, 0))
        self.cnn1_2 = Conv2d(in_channels=1, out_channels=128, kernel_size=(4, 16), stride=1)
        self.cnn1_3 = Conv2d(in_channels=1, out_channels=128, kernel_size=(5, 16), stride=1, padding=(2, 0))

        self.cnn2 = Conv2d(in_channels=1, out_channels=128, kernel_size=(4, 8), stride=4)

        encoder_layer = TransformerEncoderLayer(d_model=512, nhead=4, dim_feedforward=512, dropout=0.2)
        self.transformer_encoder = TransformerEncoder(encoder_layer, num_layers=2)

        self.lin1 = Linear(512, 64)
        self.lin2 = Linear(64, 32)
        self.lin3 = Linear(32, 1)

    def forward(self, data):
        x_name, x_behavior = data.split([1000, 4000], 1)

        x_name = self.embedder1(x_name)
        x_behavior = self.embedder2(x_behavior)

        x_name = x_name.unsqueeze(1)
        x_behavior = x_behavior.unsqueeze(1)

        pad = ZeroPad2d(padding=(0, 0, 2, 1))
        x_name_pad = pad(x_name)

        x_name_cnn1 = F.relu(self.cnn1_1(x_name)).squeeze(-1).permute(0, 2, 1)
        x_name_cnn2 = F.relu(self.cnn1_2(x_name_pad)).squeeze(-1).permute(0, 2, 1)
        x_name_cnn3 = F.relu(self.cnn1_3(x_name)).squeeze(-1).permute(0, 2, 1)

        x_behavior = F.relu(self.cnn2(x_behavior)).squeeze(-1).permute(0, 2, 1)

        x = torch.cat([x_name_cnn1, x_name_cnn2, x_name_cnn3, x_behavior], dim=-1)

        x = self.transformer_encoder(x)

        x, max_index = torch.max(x, dim=1)
        
        x = F.relu(self.lin1(x))
        x = F.dropout(x, p=0.2, training=self.training)
        x = F.relu(self.lin2(x))
        x = F.dropout(x, p=0.2, training=self.training)
        x = torch.sigmoid(self.lin3(x))

        return x
    
def predict(loader):
    model.eval()
    with torch.no_grad():
        for step, batch in enumerate(loader):
            b_x = batch[0].to(device)
            pred = model(b_x)
            pred = torch.where(pred >= 0.5, torch.ones_like(pred), torch.zeros_like(pred))
        return pred.to('cpu').detach().numpy().tolist()[0]

input_data = np.load('../input.npz', allow_pickle=True)
input_x_name = input_data['x_name']
input_x_semantic = input_data['x_semantic']

input_x = np.concatenate([input_x_name, input_x_semantic], 1)

input_xt = torch.from_numpy(input_x)

input_dataset = Data.TensorDataset(input_xt)

input_loader = Data.DataLoader(
    dataset=input_dataset,
    batch_size=64,
    num_workers=1,
)

model = torch.load('../model.pkl', map_location=device)
model = model.to(device)

# Check if the loaded model has transformer_encoder, otherwise initialize it
if not hasattr(model, 'transformer_encoder'):
    encoder_layer = TransformerEncoderLayer(d_model=512, nhead=4, dim_feedforward=512, dropout=0.2)
    model.transformer_encoder = TransformerEncoder(encoder_layer, num_layers=2)
    model.transformer_encoder = model.transformer_encoder.to(device)

predictions = predict(input_loader)
print("Predictions:")
print(predictions)
