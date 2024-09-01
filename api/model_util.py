import os
import json
import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Embedding, TransformerEncoder, TransformerEncoderLayer, Linear, Conv2d, ZeroPad2d
import torch.utils.data as Data

import warnings
warnings.filterwarnings("ignore")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('device', device)

dontrun = ["1454","1189","940","1583","1773","1063","1389","1940","348","649","775","543","200","153","1146","1829","834","875","1629","921","1071","215","721","828","106","1784","1995","1941","620","857","384","332","1296","1126","270","1877","1756","1256","111","1483","137","1985","1002","1150","204","1447","1143","1475","1659","1897","71","945","639","1237","1589","1769","925","1798","1990","79","80","120","124","128"]

word2id = np.load('../src/word2id.npz', allow_pickle=True)
word2id = word2id['word2id'][()]

word2behavior = np.load('../src/word2behavior.npz', allow_pickle=True)
word2behavior = word2behavior['word2behavior'][()]

behavior2id = np.load('../src/behavior2id.npz', allow_pickle=True)
behavior2id = behavior2id['behavior2id'][()]

NPZ = '../npz'

os.makedirs(NPZ, exist_ok=True)

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def api_extraction(filename):
    path = '../reports/'

    report_list = []
    api_num = []
    n = 0

    if os.path.exists(path + filename):
        with open(path + filename, 'r') as load_f:
            try:
                report_dict = {}
                call_list = []
                load_dict = json.load(load_f)
                if 'behavior' not in load_dict:
                    print(file_num + "_notexist")
                    return
                if load_dict['strings'][0] == "This program must be run under Win32":
                    print(file_num + "_mustInWin32")
                    return
                report_dict['md5'] = load_dict['target']['file']['md5']
                for process in load_dict['behavior']['processes']:
                    if len(process['calls']) != 0:
                        for call in process['calls']:
                            if (len(call_list) == 0 or call_list[-1] != call['api']):
                                call_list.append(call['api'])
                                # Statistics API
                                if call['api'] not in api_num:
                                     api_num.append(call['api'])
                report_dict['call_list'] = call_list
                report_list.append(report_dict)
            except:
                print(file_num + "_error")

    return(api_num)

def input_generate(filename):
    data = api_extraction(filename)

    data_x_name = []
    data_x_semantic = []
    data_y = []
    md5 = []

    api_sequence = []
    semantic_sequence = []
    
    while(len(data) < 1000):
        data.append("_PAD_")
    count = 0
    
    for api in data:
        if count == 1000:
            break
        api_id = word2id.get(api)
        api_sequence.append(api_id)

        behavior = word2behavior.get(api)
        semantic_ids = [behavior2id.get(b) for b in behavior]
        semantic_sequence.extend(semantic_ids)
        count += 1

    data_x_name.append(api_sequence)
    data_x_semantic.append(semantic_sequence)
    data_y.append(int(0))

    data_x_name = np.array(data_x_name)
    data_x_semantic = np.array(data_x_semantic)
    data_y = np.array(data_y).reshape(-1, 1)

    np.savez('../npz/input.npz', x_name=data_x_name, x_semantic=data_x_semantic, y=data_y)
    print(data_x_name)
    print(data_x_semantic)
    print(data_y)



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

model = torch.load('../src/model.pkl', map_location=device)
model = model.to(device)

def get_result(input_npz):
    input_data = np.load('../npz/' + input_npz, allow_pickle=True)
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

    if not hasattr(model, 'transformer_encoder'):
        encoder_layer = TransformerEncoderLayer(d_model=512, nhead=4, dim_feedforward=512, dropout=0.2)
        model.transformer_encoder = TransformerEncoder(encoder_layer, num_layers=2)
        model.transformer_encoder = model.transformer_encoder.to(device)

    predictions = predict(input_loader)
    print("Predictions:")
    print(predictions)

# get_result('input.npz')
