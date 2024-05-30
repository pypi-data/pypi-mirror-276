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
from numba import cuda,jit
from inspectnn.BaseLayer import BaseLayer
from inspectnn.Quantizate.Quant_kernel_tflite import quant_3d,quant_2d


class QuantizateLayer(BaseLayer):
    layer_name = "Quant"
    def __init__(self,type='FakeMinMax', name = "Quantize",quant_nbits = 8):
        super().__init__(self, name = name,quant_nbits=quant_nbits)
        self.type=type
        
    def __deepcopy__(self, memo = None):
        return QuantizateLayer( name = self.name,type=self.type,quant_nbits=self.quant_nbits)

    #@jit
    def forward_pass_input(self, inputv ):

        
        if cuda.is_cuda_array(inputv):
            A_global_mem = inputv
        else:
            A_global_mem = cuda.to_device(np.ascontiguousarray(inputv))
        input_mul = 1
        input_offset = 0


        #A_global_mem = inputv
        #print(self.name,"input v1",A_global_mem.copy_to_host()[0][4])
        
        #if True or self.use_3d:
        cuda.synchronize()
        #print(f"{self.name} Input_mul : {input_mul}")
        quant_3d[self.griddim, self.blockdim](self.results, A_global_mem,self.output_mul,self.output_offset,input_mul,input_offset)
        #else:
        #    cuda.synchronize()
        #    quant_2d[self.griddim, self.blockdim](self.results, A_global_mem,self.output_mul,self.output_offset,input_mul,input_offset)
        
        #print(self.name,"out",self.results.copy_to_host().shape)
        #print(self.name,"out",self.results.copy_to_host()[0])
        #print(self.name,"avg",np.average(self.results.copy_to_host()))
        #if self.gpu_output_memory == False:          
        #    self.outputv[:,:,:] =self.results.copy_to_host()
    def forward_pass(self, **kwargs):
        if self.bypass:
            return
        if self.gpu_input_memory is None:
            try:
                inputv = kwargs["inputv"]
            except KeyError as e:
                print(e)
                print(kwargs)
                exit()
            if cuda.is_cuda_array(inputv):
                A_global_mem = inputv
            else:
                A_global_mem = cuda.to_device(np.ascontiguousarray(inputv))
            input_mul = 1
            input_offset = 0
        else:
            
            A_global_mem=self.pre_layer.results
            input_mul = self.pre_layer.output_mul
            input_offset = self.pre_layer.output_offset  
            
            self.pre_layer.quant_output_mul = self.output_mul/input_mul
            self.pre_layer.quant_output_offset = round(self.output_offset - self.pre_layer.output_offset* self.pre_layer.quant_output_mul)
            
            self.pre_layer.quant_results = self.results
            self.pre_layer.quant = True
            self.bypass = True
            
            #ricarica i puntatori dei layer nella strutura c del layer precedente
            self.pre_layer.test_cuda.setPointerData(self.pre_layer.preA.device_ctypes_pointer.value,
                                                    self.pre_layer.quant_results.device_ctypes_pointer.value,
                                                    self.pre_layer.quant_output_mul,
                                                    self.pre_layer.quant_output_offset)
            
            
        #print(self.name,"input v2",A_global_mem.copy_to_host()[0][0])
        
        #if True or self.use_3d:
        cuda.synchronize()
        #print(f"{self.name} Input_mul : {input_mul} offset {input_offset} output_mul {self.output_mul} output_offset {self.output_offset}")
        quant_3d[self.griddim, self.blockdim](self.results, A_global_mem,self.output_mul,self.output_offset,input_mul,input_offset)
        #else:
        #    cuda.synchronize()
        #    quant_2d[self.griddim, self.blockdim](self.results, A_global_mem,self.output_mul,self.output_offset,input_mul,input_offset)
        
        #print(self.name,"out",self.results.copy_to_host().shape)
        #print(self.name,"out",self.results.copy_to_host()[0])
        
        #print(self.name,"avg",np.average(self.results.copy_to_host()))
        #if self.gpu_output_memory == False:          
        #    self.outputv[:,:,:] =self.results.copy_to_host()

    def load_weights(self, **kwargs):
        #TODO:mettere tutto a int8
        self.input_shape, self.enable_gpu = kwargs["input_shape"],kwargs["enable_gpu"] 
        self.output_shape = self.input_shape      
        self.outputv = np.zeros(self.output_shape,dtype=np.int16)#TODO: mettere dentro if parametrico

        self.dimension = len(self.input_shape)
        if self.enable_gpu:
            self.use_gpu=True

            if self.dimension == 3 and self.input_shape[2] > 1:
                self.use_3d = True
                self.blockdim = (2,2,2)
                self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1,self.output_shape[2] // self.blockdim[2] + 1)#,n_channels)
            elif self.dimension == 2 or self.input_shape[2] == 1:
                self.use_3d = False
                self.blockdim = (4,4)
                self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1)#,n_channels)
            else:
                print("Errore Input shape:",self.input_shape)


            self.results = cuda.device_array(self.output_shape, dtype=np.int8)#int16 o 8
            
            self.gpu_input_memory = kwargs["gpu_input_memory"]
           
            self.output_mul= 1/kwargs["quant_output_k"]
            self.output_offset= kwargs["quant_output_offset"]
            #print(f"{self.name} Output_mul : {self.output_mul} offset {self.output_offset}")

        return self.output_shape
    
