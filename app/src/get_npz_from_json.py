import os
import json
import numpy as np

dontrun = ["1454","1189","940","1583","1773","1063","1389","1940","348","649","775","543","200","153","1146","1829","834","875","1629","921","1071","215","721","828","106","1784","1995","1941","620","857","384","332","1296","1126","270","1877","1756","1256","111","1483","137","1985","1002","1150","204","1447","1143","1475","1659","1897","71","945","639","1237","1589","1769","925","1798","1990","79","80","120","124","128"]

word2id = np.load('../word2id.npz', allow_pickle=True)
word2id = word2id['word2id'][()]

word2behavior = np.load('../word2behavior.npz', allow_pickle=True)
word2behavior = word2behavior['word2behavior'][()]

behavior2id = np.load('../behavior2id.npz', allow_pickle=True)
behavior2id = behavior2id['behavior2id'][()]

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def api_extraction(filename):
    path = '../../report/'

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

    np.savez('../input.npz', x_name=data_x_name, x_semantic=data_x_semantic, y=data_y)
    # print(data_x_name)
    # print(data_x_semantic)
    # print(data_y)

input_generate('test_report.json')