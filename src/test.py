import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split


def data_info(direct):
  files = [file.strip() for file in os.listdir('./data/'+direct)]
  filenames = []
  for file in files:
    add = [file[:-4],file[0]]
    filenames.append(add)
  return filenames



def pixel_info(direct, df):
  pixels = []
  for file in list(df['filename']):
    from PIL import Image
    im = Image.open('./data/'+direct+'/'+file+'.bmp')
    pix = list(im.getdata())
    pixels.append(pix)

  df_pix = pd.DataFrame(pixels, columns = list(range(144**2)))
  return df_pix

df_train = data_info(direct = 'train')
df_test = data_info(direct = 'test')


train = pd.DataFrame(df_train, columns =['filename', 'label'])
test = pd.DataFrame(df_test, columns = ['filename', 'label'])

train_pix = pixel_info('train', train)
test_pix = pixel_info('test', test)
X_train, X_val, y_train, y_val = train_test_split(train_pix.values, train['label'], test_size = 0.3, random_state=42, shuffle=True, stratify=None)


with open('model/model_cb.pkl', 'rb') as f:
    best = pickle.load(f)

val_pred = best.predict(X_val)
pred = pd.DataFrame(val_pred)
pred = list(pred.iloc[:,0])
val = list(y_val)


test_pred = best.predict(test_pix.values)

test['label'] = test_pred
test['filename'] = pd.to_numeric(test["filename"])


result = test.sort_values(by=['filename'], ascending=True)

print("fileName : ", result['filename'][0])

print("label: ", result['label'][0])