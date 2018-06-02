import numpy as np
import pandas as pd
import re, json, glob



def get_id_label_dict(train_labels,val_labels):
    labels = pd.read_csv(train_labels, index_col=0, sep=';', header=None)
    labels = json.loads(labels.to_json())['1']
    validation_labels = pd.read_csv(val_labels, index_col=0, sep=';', header=None)
    validation_labels = json.loads(validation_labels.to_json())['1']
    labels.update(validation_labels)

    return labels

def get_all_labels(all_labels):
    df = pd.read_csv(all_labels, header = None).reset_index()
    label_class_dict = dict(df[[0,'index']].values)
    
    return label_class_dict



def get_class(file, id_label_dict, label_class_dict):
  f_id = re.findall(r'([0-9]*).(npy|json)', file)[0][0]
  f_label = id_label_dict[f_id]
  f_class = label_class_dict[f_label]

  return f_class


def make_numpy_array(file, db_type):
  if db_type == 'all':
    result = np.zeros((37,120))
  elif db_type == 'body':
    result = np.zeros((37,36))
  elif db_type == 'hands':
    result = np.zeros((37,84))
  
  for k in sorted(list(file['data'].keys())):
    k_int = int(k)
    try:
      data = file['data'][k][0]
      
      if db_type == 'all':
        bla = np.r_[data['pose_keypoints'], data['hand_left_keypoints'], data['hand_right_keypoints']]
      if db_type == 'body':
        bla = data['pose_keypoints']
      if db_type == 'hands':
        bla = np.r_[data['hand_left_keypoints'], data['hand_right_keypoints']]
        
      bla = bla[[False if i %3 ==2 else True for i in range(len(bla))]]
      result[k_int-1] = bla
    except:
      None
  return result

