from sklearn.model_selection import train_test_split
import numpy as np, tensorflow as tf, random
from sklearn.model_selection import train_test_split

import pandas as pd
import os,pandas

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils import shuffle



IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224
IMAGE_CHANNELS = 3

my_PATH = os.path.dirname(__file__)+ '/FGVC7/train.csv'



def get_class(row):
    
    if row['multiple_diseases'] == 1:
        return 'multiple_diseases'
    
    elif row['rust'] == 1:
        return 'rust'
    
    elif row['scab'] == 1:
        return 'scab'
    
    else:
        return 'healthy'

     
def Dataset_FGVC7(num_of_samples,sequenzial=False,PATH=None):
    
        
    
    df_train_all = pd.read_csv(PATH+"train.csv")
    
    df_train_all['target'] = df_train_all.apply(get_class, axis=1)

    df_train_all.head()
    df_train_all['target'].value_counts()
    
    # shuffle
    df_train_all_shuffle = shuffle(df_train_all, random_state=101)
    # select the column that we will use for stratification
    y = df_train_all_shuffle['target']

    df_train, df_val = train_test_split(df_train_all_shuffle, test_size=0.2, random_state=101, stratify=y)
    

    
    animals = os.listdir(PATH)
    
    images = [os.path.join(PATH, "images/"+images_id +".jpg") for images_id in df_train_all['image_id']]
    
    label = []
    categories = []
    for animal in df_train_all['target']:
        if "rust" in animal:
            categories.append('2s')
        elif "scab" in animal:
            categories.append('3')

        elif "healthy" in animal:
            categories.append('0')
        elif "multiple_diseases" in animal:
            categories.append('1')
        else:
            print(animal + " non identificato!")
            
    animals = pandas.DataFrame({'Image_name': np.array([f'{f}' for f in images]), 'Category': categories})
    
    if num_of_samples > 0:
        batch_size = num_of_samples
    else:
        batch_size = 1-num_of_samples
        
        
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_dataframe(animals, x_col='Image_name', y_col='Category', class_mode = 'sparse', target_size = (224, 224), batch_size = batch_size, validate_filenames = False,shuffle=not sequenzial)
    y_test = animals['Category']
    len_test_dataset = animals.shape[0]
    
  
    # for i in range(len(test_generator)):
    #    batch_images, batch_labels = test_generator[i]
    #    for j in range(batch_images.shape[0]):
    #        image = batch_images[j]
    #        label = batch_labels[j]

    if(num_of_samples > 0):

        img, lab = test_generator[0]
        #print(lab)
        #for i in range(1,num_of_samples):
        #    #trasforma img2 da bgr a rgb senza utilizare cv
        #    img = img2[i][:,:,::-1]
        
        label = [int(j) for j in lab]
        return  None,label ,img, lab
    
    
    else:
        batch_images, batch_labels = test_generator[0]
        
        label = [int(batch_labels[-num_of_samples])]
        return  None,label,[batch_images[-num_of_samples]], [batch_labels[-num_of_samples]]