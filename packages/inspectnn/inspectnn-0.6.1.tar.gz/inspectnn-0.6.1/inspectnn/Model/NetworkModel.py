"""
Copyright 2022  Salvatore Barone <salvatore.barone@unina.it>
                Filippo Ferrandino <fi.ferrandino@studenti.unina.it>

This is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3 of the License, or any later version.

This is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
RMEncoder; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
import numpy as np, json, copy, time,os,tempfile,mmap
from numba import cuda, jit

from distutils.dir_util import mkpath
from inspectnn.Conv.ConvLayer_TFLITE import ConvLayer
from inspectnn.Conv.ConvLayer_TFLITE import ConvLayer_TFLITE
from inspectnn.Dense.DenseLayer_TFLITE import DenseLayer
from inspectnn.Dense.DenseLayer_TFLITE import DenseLayer_TFLITE
from inspectnn.Pooling.PoolingLayer import PoolingLayer
from inspectnn.Pooling.PoolingLayer_TFLITE import PoolingLayer_TFLITE
from inspectnn.Flatten.FlattenLayer import FlattenLayer
from inspectnn.Quantizate.QuantizateLayer import QuantizateLayer
from inspectnn.Add.AddLayer import AddLayer
from inspectnn.PAD.PadLayer import PadLayer
#from .OutputLayer import OutputLayer
from inspectnn.Utils.utils import grouped, flatten


class NetworkModel:
    def __init__(self, learned_parameters, layers,input_shape,print_input=False,quant_data=None,quant_data_scale=None):
        self.learned_parameters = learned_parameters
        self.layers = layers
        self.outputs = []
        self.input_shape=input_shape
        self.print_input = print_input
        self.total_time = 0
        self.n_frame_inference = 0
        self.elapsed_time = np.zeros(len(layers))
        self.quant_data=quant_data
        self.N_layer_with_multiply = 0
       
        gpu_input_memory=None
        
        lp = 0
        last_layer=None
        disponibilita_gpu=True#tf.test.is_gpu_available()

        quantization_bias=None
        quantization_pesi=None
        quant_input_k=None
        quant_input_offset=None
        quant_output_k = None
        quant_output_offset=None
        self.init_quantizate = True
        
        #pre_quant_data_scale = DATA_layer_quant(1/255,-128)
        for id_layer in range(len(self.layers)):
            
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                if(self.quant_data != None):

                    quantization_pesi = quant_data[lp].scales
                    quantization_bias = quant_data[lp+1].scales
                    quant_input_k = pre_quant_data_scale.scales
                    quant_input_offset = pre_quant_data_scale.offset
                    quant_output_k = quant_data_scale[lp//2].scales
                    quant_output_offset = quant_data_scale[lp//2].offset
                   
                    pre_quant_data_scale = quant_data_scale[lp//2]

               
                output_shape =self.layers[id_layer].load_weights(input_shape = input_shape, weights = self.learned_parameters[lp], biases = self.learned_parameters[lp + 1],
                                                                        enable_gpu=disponibilita_gpu,gpu_input_memory=gpu_input_memory,pre_layer=last_layer,
                                                                        quant_data=quantization_pesi,quant_bias=quantization_bias,quant_input_k=quant_input_k,
                                                                        quant_input_offset=quant_input_offset,quant_output_k=quant_output_k,quant_output_offset=quant_output_offset)
                lp += 2
            
                
            elif isinstance(self.layers[id_layer], (PoolingLayer, FlattenLayer, QuantizateLayer)):
                output_shape =self.layers[id_layer].load_weights(input_shape = input_shape,enable_gpu=disponibilita_gpu,gpu_input_memory=gpu_input_memory,pre_layer=last_layer)
                
            else:
                print(f"Layer {self.layers[id_layer].name} not supported yet")
            
            gpu_input_memory=self.layers[id_layer].results
            if self.layers[id_layer].use_gpu  and   last_layer != None and last_layer.use_gpu:
                last_layer.gpu_output_memory = True
            else:
                print(f"Layer {self.layers[id_layer].name} no gpu")

            input_shape = output_shape
            self.layers[id_layer].pre_layer = last_layer
            last_layer = self.layers[id_layer]
        

    def __deepcopy__(self, memo = None):
        return NetworkModel(self.learned_parameters, copy.deepcopy(self.layers),self.input_shape)

    def export_learned_parameters(self):
        data = []
        for i, p in enumerate(grouped(self.learned_parameters, 2)):
            tmp = list(flatten(p[0].astype(int).tolist()))
            with open(f"layer_{i}.json", 'w') as outfile:
                outfile.write(json.dumps(tmp))
            data.append(tmp)
        data = list(flatten(data))
        with open("network.json", 'w') as outfile:
            outfile.write(json.dumps(data))
                
    def update_multipler(self,multipliers,layer_apx=None):
        idx=0

        if layer_apx is None:
            n_layer_apx = len(self.layers)
        else:
            n_layer_apx = layer_apx
        
        #modifica epr tutti i layer
        for id_layer in range(n_layer_apx):
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                
                if(len(multipliers)==1):
                    self.layers[id_layer].M = multipliers[0].multiplier #[idx]
                    #stampa l' indirizzo in esadecimale
                    
                    #3if isinstance(self.layers[id_layer], (ConvLayer)):#TODO: add DenseLayer
                    self.layers[id_layer].test_cuda.setPointerMul( self.layers[id_layer].M.device_ctypes_pointer.value)
                        
                    self.layers[id_layer].multiplier = multipliers[0]
                else:
                    
                    self.layers[id_layer].multiplier = multipliers[idx]
                    
                    #print(f"Moltiplicatori per il layer {self.layers[id_layer]}: ", self.layers[id_layer].multiplier)
                    #TODO: aggiungere update_bias_for_mul per ogni layer conv e dense
                    #QUesto valore è un vector di bias per per ogni moltiplier
                    #self.layers[id_layer].update_bias = self.layers[id_layer].update_bias_for_mul[idx]
                    
                    self.layers[id_layer].M = multipliers[idx].multiplier
                    self.layers[id_layer].test_cuda.setPointerMul( self.layers[id_layer].M.device_ctypes_pointer.value)
                    idx+=1
       
    def get_number_of_all_filters(self, recalculated=False):
        if recalculated or self.n_filter is None:
            self.n_filter=0
            for id_layer in range(len(self.layers)):
                if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                    print(f"[{id_layer}]Layer {self.layers[id_layer].name} n_filter {self.layers[id_layer].n_filter}")
                    self.n_filter+=self.layers[id_layer].n_filter
        
        return self.n_filter
    
    def update_multipler_filters(self,multipliers, dense_multiplier):#TODO: add for cluster
        
        
        
        cont_conv=0
        dense_cont = 0
        for id_layer in range(len(self.layers)):
            if isinstance(self.layers[id_layer], (ConvLayer)):
                
                n_filter = self.layers[id_layer].n_filter
                #print("nfilter", n_filter)
                self.layers[id_layer].idx_multiply = multipliers[cont_conv:(cont_conv+n_filter)]
                #print(f"Moltiplicatori per il layer {self.layers[id_layer]}: ", self.layers[id_layer].idx_multiply)
                #print(multipliers[idx:(idx+n_filter)])
                cont_conv += n_filter
                
            elif isinstance(self.layers[id_layer], (DenseLayer)):
                
                n_filter = self.layers[id_layer].n_filter
                #print("Numero di filtri:", n_filter)
                self.layers[id_layer].idx_multiply = dense_multiplier[dense_cont:(dense_cont+n_filter)]
                #print(f"Moltiplicatori per il layer {self.layers[id_layer]}: ", self.layers[id_layer].idx_multiply)
                
                dense_cont += n_filter
                
                
    
    
    #Call this function to approximate all Conv Layer by fibres. You need to specify all multipliers for all layer 
    def update_multiplier_for_fibers(self,fibers_multiplier_id, dense_multiplier):#TODO: add for cluster
        
        # print("Multiplier Conv")
        # for elem in fibers_multiplier_id:
        #     print(elem)
            
        # print("Multiplier Dense")
        # for elem in dense_multiplier:
        #     print(dense_multiplier)

        
        
        
        #!NOTA: fibers_multiplier_id è la matrice di id di moltiplicatori per fibra per i layer a convoluzione
        #!      dense_multiplier è l'oggetto moltiplicatore per i layer dense.
        
        conv_counter = 0
        dense_counter = 0
        for id_layer in range(len(self.layers)):
            if isinstance(self.layers[id_layer], (ConvLayer)):
                
                self.layers[id_layer].mul_per_fibers = fibers_multiplier_id[conv_counter]
                
                #print(f"Moltiplicatori per il layer {self.layers[id_layer]}: ", self.layers[id_layer].mul_per_fibers)
                conv_counter += 1
                
            elif isinstance(self.layers[id_layer], (DenseLayer)):
                
                
                
                self.layers[id_layer].multiplier = dense_multiplier[dense_counter]
            #     #TODO: aggiungere update_bias_for_mul per ogni layer conv e dense
            #     #QUesto valore è un vector di bias per per ogni moltiplier
            #     #self.layers[id_layer].update_bias = self.layers[id_layer].update_bias_for_mul[idx]
                self.layers[id_layer].M = dense_multiplier[dense_counter].multiplier
                
                #print(f"Moltiplicatori per il layer {self.layers[id_layer]}: ", dense_multiplier[dense_counter])
                dense_counter +=1
        
    
    #Call this function to approximate a specifi Conv layer by fibres. You need to specify all multipliers for the layer 
    def update_multiplier_fibers_by_layer():
        #if isinstance(self.layers[id_layer], (ConvLayer)): #!TODO: Add Dense Layer
        #    fibers = self.layers[id_layer].fibers
            
        return
    
    

    def update_multipler_filter(self,multipliers,id_layer,cluster = None):
        if cluster is None:
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                
                n_filter = self.layers[id_layer].n_filter
                self.layers[id_layer].idx_multiply = multipliers
                #print(multipliers[idx:(idx+n_filter)])
            else:
                print(f"Layer{ self.layers[id_layer].name} not valid")
        else:
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                n_filter = self.layers[id_layer].n_filter
                multipliers_for_layer = np.zeros(n_filter)
                for i in range (n_filter):
                    multipliers_for_layer[i] = multipliers[cluster[i]]
                
                self.layers[id_layer].idx_multiply = multipliers_for_layer
                #print(multipliers[idx:(idx+n_filter)])
            else:
                print(f"Layer{ self.layers[id_layer].name} not valid")

    def load_total_multiply_gpu(self,all_multipliers):
        
        for id_layer in range(len(self.layers)):
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                
                self.layers[id_layer].all_M = all_multipliers
            
    def total_filter(self):
        total_filter=0
        for id_layer in range(len(self.layers)):
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                total_filter+=self.layers[id_layer].n_filter
        
        print("Total filter:",total_filter)

        return total_filter
    
    def predict(self, test_image, enable_multiprocess = False):
        self.outputs = [test_image]
        self.n_frame_inference+=1
        print("Predict:", test_image.copy_to_host()[0][0])
        if self.print_input:
            with open('test_image.txt', 'w', encoding='UTF8', newline='') as f:
                print(self.outputs,file=f)
            
        for id_layer in range(len(self.layers)):
            
            st = time.time()
            if(self.print_input):
                self.layers[id_layer].update_save_path()
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer,PoolingLayer, FlattenLayer,QuantizateLayer)):
                self.outputs =       [self.layers[id_layer].forward_pass(inputv = self.outputs[-1])]
            else:
                print(f"Layer {self.layers[id_layer].name} not supported yet")
            
            et = time.time()
            self.elapsed_time[id_layer] += et - st
            self.total_time += et - st

            
        
        return self.outputs[-1] / np.max(self.outputs[-1])
        
    def print_time_statics(self):
        print(f"Total Layers Time = {self.total_time}")
        print(f"Total FPS ={self.n_frame_inference/self.total_time}")
        idx=0
        for layer in self.layers:
            line_new = 'Layer {:>30}\tTime:{:>8}s ({:>5}% )'.format(layer.name,round(self.elapsed_time[idx], 2),round(self.elapsed_time[idx]/self.total_time*100,1))
            print(line_new,f"\tGPU:{layer.use_gpu}\tGPU_OUT:{layer.gpu_output_memory}")
            idx+=1
            
            
            
    def print_time_statics_v2(self,print_all_layer=True):
        self.fps = self.n_frame_inference/self.total_time
        print(f"Total Layers Time = {round(self.total_time,2)}s\t [{round(self.fps,1)} FPS]")
        n_total_multiply = 0
        for layer in self.layers:
            n_total_multiply =  n_total_multiply + layer.n_moltiplicazioni
        
        print(f"Total multiply = {n_total_multiply} --> {round(self.n_frame_inference*n_total_multiply/(1000000000*self.total_time),1)} GOPS")
        idx=0
        if(print_all_layer):
            for layer in self.layers:
                line_new = '[{:>7}] {:>30}\tTime:{:>8}s ({:>5}%)  Power {:>8} mW ({:>5}%) '.format(layer.layer_name,layer.name,round(self.elapsed_time[idx], 2),round(self.elapsed_time[idx]/self.total_time*100,1),
                                                                                                round(layer.power,1),round(100*layer.n_moltiplicazioni/n_total_multiply,2))
                print(line_new)
                idx+=1
    
    def print_type_time(self):
        type_l = [ConvLayer_TFLITE, DenseLayer_TFLITE,PoolingLayer_TFLITE, FlattenLayer,QuantizateLayer,AddLayer,PadLayer]
        total= 0
        for i in type_l:
            total+=i.total_type_layer_time
        
        print(f"Total Time: {round(total,2)}s")
        for i in type_l:
              print(f"{str(i.layer_name).ljust(15)} \t {round(i.total_type_layer_time,2)}s \t( {str(round(100*i.total_type_layer_time/total,2)).ljust(5)}% )")
        
        
            
    def mimt_do_inference(self, labels, images):
        assert isinstance(labels, (list, tuple))
        assert isinstance(images, (list, tuple))
        assert len(labels) == len(images)
        result=[]
        for l, i in zip(labels, images):
            result_predict = self.predict(i)[0]
            result.append(np.argmax(result_predict) == l)

        return result
        
    def evaluate_accuracy(self, labels, images):
        assert isinstance(labels, (list, tuple)), f"labels must be a list or tuple. labels is {type(labels)}"
        assert isinstance(images, (list, tuple)), f"images must be a list or tuple. labels is {type(images)}"
        assert len(labels) == len(images), f"images and labes must be the same size. len(labels): {len(labels)}, len(images): {len(images)}"

        result=0

        for i in range(len(images)):
            #result+=1
            #print("evaluate: ",images[i].copy_to_host())
            predict_class = self.predict(images[i])
            result+=np.argmax(predict_class) == labels[i]#.append()
        
        return 100*result / len(labels)
    
    def evaluate_accuracyv2(self, labels, images,threshold=0.2,K_ratio=10):
        assert isinstance(labels, (list, tuple))
        assert isinstance(images, (list, tuple))
        assert len(labels) == len(images)

        result=0#[]

        for i in range(len(images)//K_ratio):
            #result+=1
            result+=np.argmax(self.predict(images[i])) == labels[i]#.append()
        
        if result > threshold*len(images)//K_ratio :
            for i in range(len(images)//K_ratio,len(images)):
                #result+=1
                result+=np.argmax(self.predict(images[i])) == labels[i]#.append()

            return 100*result / len(labels)
        
        else:
            return 100*result / (len(labels)//K_ratio)
        

    def evaluate_confusion_matrix(self, images,labels,n_class=10):

        result_matrix=np.zeros((n_class,n_class),dtype=int)

        for i in range(len(images)):
            #result+=1
            predict_class = np.argmax(self.predict(images[i]))
            result_matrix[predict_class,labels[i]] +=1
            #result=np.argmax(predict_class) == labels[i]#.append()

        result_matrix_norm=result_matrix/np.sum(result_matrix,0)
        return result_matrix_norm
    

    def evaluate_delta_gradient(self, images1, images2):
        
        result=0#[]

        predict_class1 = self.predict(images1).copy()
        predict_class2 = self.predict(images2).copy()

        return predict_class1 - predict_class2
    

    def get_Numbers_layer_with_multiply(self):
        self.N_layer_with_multiply = 0
        for id_layer in range(len(self.layers)):
            if isinstance(self.layers[id_layer], (ConvLayer, DenseLayer)):
                self.N_layer_with_multiply+=1

        return self.N_layer_with_multiply
    
    def return_Area(self):
        total_area= 0
        for layer in self.layers:

            if isinstance(layer, (ConvLayer, DenseLayer)):
                total_area +=  layer.multiplier.Area
                
        return total_area
    
    # def return_Power(self):
    #     total_power = 0
    #     for layer in self.layers:
    #         if isinstance(layer, (ConvLayer, DenseLayer)):
    #             layer.power = 0
                
    #             layer.power = layer.multiplier.Power*layer.n_moltiplicazioni
    #             print("LayerPower: ", layer.power, "n_moltiplicazioni: ", layer.n_moltiplicazioni, "multiplier_power: ", layer.multiplier.Power )
                
    #             total_power +=  layer.power
                
    #     return total_power
    
    
    def return_Power(self):
        total_power = 0
        for layer in self.layers:
            if isinstance(layer, (ConvLayer, DenseLayer)):
                layer.power = layer.multiplier.Power*layer.n_moltiplicazioni
                total_power +=  layer.multiplier.Power*layer.n_moltiplicazioni
                #print("LayerPower: ", layer.power, "n_moltiplicazioni: ", layer.n_moltiplicazioni, "multiplier_power: ", layer.multiplier.Power )

            
        return total_power
    
    
    def return_power_for_fibers(self):
        total_power = 0
        
        for id_layer in range(len(self.layers)):
            if isinstance(self.layers[id_layer], (ConvLayer)):
                
                #! DEVO CAPIRE COME SI CALCOLA LA POTENZA PER FIBRE
                print("LEN: ", np.shape((self.layers[id_layer].mul_per_fibers)))
                print("Mul_Per_fibers_", self.layers[id_layer].mul_per_fibers)
                print("NMoltipl_",self.layers[id_layer].n_moltiplicazioni)
                exit()
                temp_power = self.layers[id_layer].mul_per_fibers * self.layers[id_layer].n_moltiplicazioni
                total_power += temp_power
                
            elif isinstance(self.layers[id_layer], (DenseLayer)):
                
                
                
                self.layers[id_layer].multiplier = dense_multiplier[dense_counter]
            #     #TODO: aggiungere update_bias_for_mul per ogni layer conv e dense
            #     #QUesto valore è un vector di bias per per ogni moltiplier
            #     #self.layers[id_layer].update_bias = self.layers[id_layer].update_bias_for_mul[idx]
                self.layers[id_layer].M = dense_multiplier[dense_counter].multiplier
                dense_counter +=1
        
        
        
        
        return total_power
    

    def save_occorenze(self,base_name):
        for layer in self.layers:
            if isinstance(layer, (ConvLayer, DenseLayer)):
                np.save(base_name+layer.name,layer.occorenza.copy_to_host())
