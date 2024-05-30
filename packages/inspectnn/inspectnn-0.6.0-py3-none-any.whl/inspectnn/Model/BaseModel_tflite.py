import time
from numba import cuda
import numpy as np
from inspectnn.Model.BaseModel import BaseModel
class BaseModel_tflite(BaseModel):
    def __init__(self, multiplier,quant_nbits = 8,input_shape=[28, 28, 1],save_csv_path=''):
        
        super().__init__(multiplier,quant_nbits,input_shape,save_csv_path)

        self.elapsed_time = 0
        #self.interpreter = []
        self.total_elapsed_time=0
        self.baseline_accuracy = None
        
        self.net = None
         
    def evaluate2(self,images,labels,log=False):
        num_of_samples=len(images)
        if log : 
            print(f"Testing on {len(images)} images.")
        st = time.time()
        Accuracy = self.net.evaluate_accuracy(labels, images)
        if log :
            print(f"Accuracy: {Accuracy}")
        et = time.time()
        self.elapsed_time = et - st
        self.total_elapsed_time+=self.elapsed_time
        if log :
            print('MIMT execution time:', self.elapsed_time, 'seconds')
            print('FPS:', num_of_samples/self.elapsed_time) 
            self.net.print_time_statics()
        return Accuracy
    

    def evaluate_quantized_model(self, x_test_set, y_test_set):
        input_index = self.interpreter.get_input_details()[0]["index"]
        output_index = self.interpreter.get_output_details()[0]["index"]
        prediction_digits = []
        labels = []
        for i, test_image in enumerate(x_test_set):
            test_image = np.expand_dims(test_image, axis=0).astype(np.float32)
            self.interpreter.set_tensor(input_index, test_image)
            # Run inference.
            self.interpreter.invoke()

            output = self.interpreter.tensor(output_index)
            digit = np.argmax(output()[0])
            prediction_digits.append(np.array(digit))
            labels.append(y_test_set[i])

        prediction_digits = np.array(prediction_digits)
        accuracy = (prediction_digits == np.array(labels)).mean()
        return accuracy
    
    def evaluate_tflite(self, x_test_set, y_test_set,print_debugs=None,print_acc=True):

        input_index = self.interpreter.get_input_details()[0]["index"]
        output_index = self.interpreter.get_output_details()[0]["index"]
        prediction_digits = []
        labels = []
        #print(self.interpreter.get_input_details()[0])
        start_time = time.time()
        for i, test_image in enumerate(x_test_set):
            
            test_image = np.expand_dims(test_image, axis=0).astype(np.float32)#fp32
            #print("test image shape: " ,test_image.shape)
            self.interpreter.set_tensor(input_index, test_image)

            # Run inference.
            self.interpreter.invoke()
            
            if print_debugs is not None:
                #valori resnet8
                quant_layer=6
                conv_lay = 9
                conv1_lay = 12
                for print_debug in print_debugs:
                    print('### tflite interpetrer: -------#####>>>>>> L(',print_debug,")")
                    print("NAME: ",self.interpreter.get_tensor_details()[print_debug]['name'].split('/')[1])
                    print(self.interpreter.get_tensor(print_debug).shape)
                    #print("max:",np.amax(self.interpreter.get_tensor(print_debug)))
                    print(self.interpreter.get_tensor(print_debug)[0][0][0])

                


            output = self.interpreter.tensor(output_index)
            digit = np.argmax(output())
            prediction_digits.append(np.array(digit))
            labels.append(int(y_test_set[i]))
            #print(digit,labels[-1])
        delta_time = time.time() - start_time
        
        #print(prediction_digits)
        prediction_digits = np.array(prediction_digits)     
        accuracy = (prediction_digits == np.array(labels)).mean()
        if print_acc:
            #print(f"Accuracy Tflite: {accuracy * 100:.2f}%, {len(prediction_digits)} images in {delta_time}s - {len(prediction_digits)/delta_time} FPS ")
            print(f"Accuracy Tflite: {accuracy * 100:.2f}%, {len(prediction_digits)} images in {round(delta_time,2)}s - {round(len(prediction_digits)/delta_time,2)} FPS ")
       
        return accuracy
    
   
        

    def trova_dif(self, x_test_set_tf, y_test_set_tf):
        counter = 0
        print("Trova DIFF ....")
        self.net.update_multipler([self.exact_multiplier])
        for i in range(0,len(x_test_set_tf)):
            
            predict_class = self.net.predict(self.images[i])
            nostro_tool=np.argmax(predict_class) == self.labels[i]#.append()

            tflite = self.evaluate_tflite(x_test_set_tf[i:i+1],y_test_set_tf[i:i+1],print_acc=False)
            
            if(nostro_tool!=tflite):
                print(counter,i,nostro_tool,sep='\t')
                counter+=1
        
        return counter/len(x_test_set_tf)
    
    
 
        



                

    

    
    
    
        