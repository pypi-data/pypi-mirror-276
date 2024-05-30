from sklearn.model_selection import train_test_split


import os,pandas
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

my_PATH = os.path.dirname(__file__)+ '/CaniGatti'

def GattidmvsCani(num_of_samples,sequenzial=False,PATH=my_PATH):
    

    animals = os.listdir(PATH)
    
    images = [os.path.join(PATH, animal) for animal in animals]
    
    label = []
    categories = []
    for animal in images:
        if "Cat" in animal:
            categories.append('0')
        elif "Dog" in animal:
            categories.append('1')
            
        else:
            print(animal + " non identificato!")
            
    animals = pandas.DataFrame({'Image_name': np.array([f'{f}' for f in images]), 'Category': categories})
    
    if num_of_samples > 0:
        batch_size = num_of_samples
    else:
        batch_size = 1-num_of_samples
        
        
    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_dataframe(animals, x_col='Image_name', y_col='Category', class_mode = 'binary', target_size = (224, 224), batch_size = batch_size, validate_filenames = False,shuffle=not sequenzial)
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
        # for i in range(1,num_of_samples):
        #     batch_images, batch_labels = test_generator[i]
        #     img.concatenate(batch_images)
        #     lab.concatenate(batch_labels)
        
        
        label = [int(j) for j in lab]
        return  None,label ,img, lab
    
    
    else:
        batch_images, batch_labels = test_generator[0]
        
        label = [int(batch_labels[-num_of_samples])]
        return  None,label,[batch_images[-num_of_samples]], [batch_labels[-num_of_samples]]