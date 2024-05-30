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
import numpy as np
from numba import cuda, jit
from inspectnn.BaseLayer import BaseLayer


@cuda.jit(cache=True)   
def concatena_tflite(result,input,offset,size):

    x, y,z= cuda.grid(3) 
    
    max_x=result.shape[0]
    max_y=result.shape[1]
    max_z=size

    if ((x >= max_x)  or (y >= max_y) or (z >= max_z)): 
        return 

    result[x,y,offset+z] = input[x,y,z]
    
#TODO: Agiungre a inspectnn

class Concatenate(BaseLayer):
    def __init__(self, name = "cocatenate"):
        super().__init__(self, name = name)
        self.gpu_layers = None

    def __deepcopy__(self, memo = None):
        return Concatenate(name = self.name)

    def load_weights(self, **kwargs):
        #self.input_shape, self.enable_gpu = kwargs["input_shape"], kwargs["enable_gpu"] 
        self.output_shape = kwargs["output_shape"]
        self.enable_gpu = kwargs["enable_gpu"] 
        
        #self.outputv = np.zeros(self.output_shape)
        if self.enable_gpu:
            self.use_gpu = True
            self.results = cuda.device_array(self.output_shape, dtype=np.int8)
            self.gpu_input_memory = kwargs["gpu_input_memory"]
            #self.pre_layer = kwargs["pre_layer"]
            
            self.output_mul = 1/kwargs["quant_output_k"]
            self.output_offset = kwargs["quant_output_offset"]
        return self.output_shape
    
    #@jit
    def forward_pass(self, **kwargs):
        if self.gpu_layers is None:
            print("concatenate no buoeno! =( ")
            
        else:
            # TODO reshape su GPU
            #cuda.synchronize()
            i = 0
            cuda.synchronize()
            for input in self.gpu_layers:
                #print(input.name)
                #copia 
                concatena_tflite[self.griddim[i], self.blockdim](self.results,input.results,self.offset[i],self.size[i])
                i += 1
               
            #self.results = self.gpu_input_memory.reshape(self.output_shape[0],self.output_shape[1])
            #self.results = self.gpu_input_memory.ravel()
            
            #self.outputv[:,:]=self.results.copy_to_host()
            #print(self.name,"output:\n",self.results.copy_to_host()[0][0])


    def load_input_layer(self,layers,tensors_out):
        
        self.gpu_output_memory = True
        
        self.gpu_layers = []
        self.griddim = []
        self.blockdim = []
        self.offset = [0]
        self.size = []
        
        self.blockdim = (1,1,8)


        for op_in in self.code_tensor_inputs:
        
            #op_in = self.code_tensor_inputs[i]
            #print(op_in)
            self.gpu_layers.append(layers[tensors_out.index(op_in)])
            
            output_shape = self.gpu_layers[-1].output_shape
            self.size.append(output_shape[2])
            self.offset.append(self.offset[-1]+self.size[-1])#incrementa l'offset con il valore della dimensione dell'ultimo tensore
            
            #calcolo della griddim in base al valore di uscita del layer di ingresso (è indispensabile perche vanno lanciati piu kernel in parallelo per ogni tensore di ingresso)
            self.griddim.append((output_shape[0] // self.blockdim[0] + 1, output_shape[1] // self.blockdim[1] + 1,output_shape[2] // self.blockdim[2] + 1))#,n_channels)


            
            

        
        #op_in1=self.code_tensor_inputs[0]
        #op_in2=self.code_tensor_inputs[1]


        

        
      