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
import numpy as np, os
import time

from numba import cuda

from inspectnn.BaseLayer import BaseLayer
from inspectnn.Conv.Conv_kernel_tflite import convolve_tflite_occorenza,convolve_tflite, convolve_tflite_padding,convolve_deepwise_padding,convolve_deepwise,convolve_tflite_mf, convolve_tflite_padding_mf,convolve_tflite_fake_mf, convolve_tflite_mfiber, convolve_tflite_fake_mfiber, convolve_tflite_padding_mfiber,convolve_tflite_fake #, convolve_tflite_mfiber_cpu
from inspectnn.Conv.ConvLayer import ConvLayer
from inspectnn.Conv.Conv_cuda import Conv_cuda


class ConvLayer_TFLITE(ConvLayer):
    total_type_layer_time = 0
    def __init__(self, stride = (1, 1), padding = (0,0),padding_type='valid', activation = "relu", quant_nbits = 8, multiplier = BaseLayer.default_multiplier, name = "Conv_TFlite",offset=[128,128],print_output=None,DEPTHWISE_CONV_2D=False):
        super().__init__(stride=stride,activation=activation, quant_nbits=quant_nbits, multiplier=multiplier, name=name,print_output=print_output,padding=padding,offset=offset)
        self.padding_type = padding_type
        self.idx_multiply = None
        self.mul_per_fibers = None
        self.preA = None
        self.DEPTHWISE_CONV_2D = DEPTHWISE_CONV_2D
       
        

    def __deepcopy__(self, memo = None):
        return ConvLayer_TFLITE(stride = self.stride, padding = self.padding, activation = self.activation, quant_nbits = self.quant_nbits, multiplier = self.multiplier, name = self.name)

    #@jit
    def forward_pass_input(self, inputv):
        #(np.sum(A_global_mem.copy_to_host()[7:14,7:14]*self.kernel_global_mem.copy_to_host()[k])*self.k_mul.copy_to_host()[k] + self.k_bias.copy_to_host()[k] - self.weights.copy_to_host()[k])*self.output_mul+self.output_offset
        A_global_mem = inputv
        #print(self.input_shape)
        self.test_cuda.setPointerInput(A_global_mem.device_ctypes_pointer.value,
                                      self.activation)
       

        #TODO: rinominare M
        #print(self.name,'dati input',A_global_mem.copy_to_host()[0])
        

        if(self.idx_multiply is None and self.mul_per_fibers is None):

            if (self.normal_kernel):
                
                #?direct CUDA conv
                self.test_cuda.convolutionRowsGPU()
                #cuda.synchronize()
                #convolve_tflite[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                #                                             self.activation,self.output_mul,self.output_offset,self.stride,self.update_bias,self.kp)
            elif (self.fake_kernel):
                
                #?direct CUDA conv
                self.test_cuda.convolutionRowsGPU_fake()
                #cuda.synchronize()
                #convolve_tflite_fake[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                #                                             self.activation,self.output_mul,self.output_offset,self.stride,self.update_bias,self.kp)
            else:
                
                value_null = self.pre_layer.output_offset
                #self.test_cuda.setStride(self.stride[0],self.stride[1],value_null)
                
                #?direct CUDA conv
                self.test_cuda.convolutionRowsGPU_padding()
                
                #?Non direct CUDA conv
                #cuda.synchronize()
                convolve_tflite_padding[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride,self.update_bias,self.kp)
        #! Fiber-based approximation 
        elif(self.mul_per_fibers is not None):
            
            # print(cuda.to_device(self.all_M))
            # exit()
            
            idxm = cuda.to_device(np.ascontiguousarray(self.mul_per_fibers))
            if (self.normal_kernel):
                cuda.synchronize()

                
                #convolve_tflite_mfiber_cpu(self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                #                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
                convolve_tflite_mfiber[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
            elif (self.fake_kernel):
                
                cuda.synchronize()
                convolve_tflite_fake_mfiber[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)

            else:
                value_null = self.pre_layer.output_offset
                
                cuda.synchronize()
                convolve_tflite_padding_mfiber[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride,idxm,self.kp)   
        #! Filter-based approximation    
        else:
            
            idxm = cuda.to_device(np.ascontiguousarray(self.idx_multiply))
            if (self.normal_kernel):
                cuda.synchronize()
                convolve_tflite_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
            elif (self.fake_kernel):
                cuda.synchronize()
                convolve_tflite_fake_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
            else:
                value_null = self.pre_layer.output_offset
                cuda.synchronize()
                convolve_tflite_padding_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride,idxm,self.kp)
        #else:
            # idxm = cuda.to_device(np.ascontiguousarray(self.idx_multiply))
            # if (self.normal_kernel):
            #     cuda.synchronize()
            #     convolve_tflite_fibre[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
            #                                                 self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
            # elif (self.fake_kernel):
            #     cuda.synchronize()
            #     convolve_tflite_fake_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
            #                                                 self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
            # else:
            #     value_null = self.pre_layer.output_offset
            #     cuda.synchronize()
            #     convolve_tflite_padding_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
            #                                                                     self.activation,self.output_mul,self.output_offset,value_null,self.stride,idxm,self.kp)
        
        
        #print(self.name,"out:\n",self.results.copy_to_host()[0][0])  
        
        #self.test_cuda.convolutionRowsGPU(self.results.device_ctypes_pointer.value)
        #TODO: calcolare grid_dim per quant 3d

        #print(self.name,"out",self.results.copy_to_host()[0][0])
        

        if self.gpu_output_memory == False:
            self.outputv[:,:,:] = self.results.copy_to_host()            
    #@jit
    def forward_pass(self):
        
        #TODO: rinominare variabili

        if self.preA != self.pre_layer.results:
            A_global_mem = self.pre_layer.results
            self.preA  = A_global_mem
            #self.test_cuda.setConvolutiontexSrc(A_global_mem.device_ctypes_pointer())
            #print(self.name,"Ok ####################################################")
            self.test_cuda.cuda_set(self, A_global_mem )
            
            if not self.fake_kernel and not self.normal_kernel:
                self.value_null2 = self.pre_layer.output_offset
                self.test_cuda.setStride(self.stride[0],self.stride[1], self.value_null2)
            

        else:
            A_global_mem = self.preA
        
        #print(self.name)#,"in",A_global_mem.copy_to_host()[0])      
           
        #TODO: rinominare M
        #! Layer-based approximation  
        if(self.idx_multiply is None and self.mul_per_fibers is None):
            #self.cuda_set( A_global_mem )
            
            
            if (self.DEPTHWISE_CONV_2D):
                if( self.padding_type == "same"):
                    value_null = self.pre_layer.output_offset
                    
                    #self.test_cuda.convolutionRowsGPU_deepwise()
                    cuda.synchronize()
                    #print("Valid padding")
                    
                    convolve_deepwise_padding[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                                                                                    self.activation,self.output_mul,self.output_offset,value_null,self.stride,self.update_bias)
                    #print(self.name,"out:\n",self.results.copy_to_host()[0][0])  
                else:
                    #print("No padding: ",self.padding_type)
                    #self.test_cuda.print_parameters()
                    #self.test_cuda.convolutionRowsGPU_deepwise()
                    #print(self.name,"out:\n",self.results.copy_to_host()[0][0])  
                    cuda.synchronize()
                    convolve_deepwise[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                                                                                    self.activation,self.output_mul,self.output_offset,self.stride,self.update_bias)
                    
                    #print(self.name,"out:\n",self.results.copy_to_host()[0][0])  
            elif(self.normal_kernel):
                
                #?direct CUDA conv
                #cuda.synchronize()
                self.test_cuda.convolutionRowsGPU()

                #?Non direct CUDA conv
                #cuda.synchronize()
                #convolve_tflite[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                #                                            self.activation,self.output_mul,self.output_offset,self.stride,self.update_bias,self.kp)
            elif (self.fake_kernel):
                #?direct CUDA conv
                self.test_cuda.convolutionRowsGPU_fake()

                #?Non direct CUDA conv
                #TODO:funzione in numba bugata
                #cuda.synchronize()
                #convolve_tflite_fake[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                #                                            self.activation,self.output_mul,self.output_offset,self.stride,self.update_bias,self.kp)
            
              
                
            else:
                value_null = self.pre_layer.output_offset

                #?direct CUDA conv
                self.test_cuda.convolutionRowsGPU_padding()
                
                #?Non direct CUDA conv
                cuda.synchronize()
                convolve_tflite_padding[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.M,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride,self.update_bias,self.kp)

           
        #! Fiber-based approximation         
        elif(self.mul_per_fibers is not None):
            
        
            idxm = cuda.to_device(np.ascontiguousarray(self.mul_per_fibers))
            
            # print(cuda.to_device(self.all_M))
            # exit()
            if (self.normal_kernel):
                
                cuda.synchronize()
                
                
                #convolve_tflite_mfiber_cpu(self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                #                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
                
                convolve_tflite_mfiber[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
     
            elif (self.fake_kernel):
                cuda.synchronize()
                convolve_tflite_fake_mfiber[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                        self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)

            
            else:
                value_null = self.pre_layer.output_offset
                cuda.synchronize()
                convolve_tflite_padding_mfiber[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride,idxm,self.kp)
                    
        #! Filter-based approximation    
        else:
            
            idxm = cuda.to_device(np.ascontiguousarray(self.idx_multiply))
            if (self.normal_kernel):
                cuda.synchronize()
                convolve_tflite_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
            elif (self.fake_kernel):
                cuda.synchronize()
               
                convolve_tflite_fake_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm,self.kp)
            else:
                value_null = self.pre_layer.output_offset
                cuda.synchronize()
                
                convolve_tflite_padding_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.params,self.k_mul,self.weights,self.k_bias,self.all_M,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride,idxm,self.kp)
        
        if self.gpu_output_memory == False:
            self.outputv[:,:,:] = self.results.copy_to_host()          
    
        #print(self.name,"out:\n",self.results.copy_to_host()[0][0])      
        #exit()  
    
    def load_weights(self, **kwargs):
        #TODO: sfrutare anche super().load_weights(**kwargs)
        
        self.test_cuda = Conv_cuda()
        
        self.kp=np.int8(1)
        self.enable_gpu = kwargs["enable_gpu"] 
        self.input_shape= kwargs["input_shape"]
        self.weights_cpu=np.array(kwargs["weights"],dtype=np.int16)
        self.kernel_shape = np.shape(kwargs["weights"])        
        self.output_shape = kwargs["output_shape"]

        self.n_channels=self.kernel_shape[0]

        self.params = cuda.to_device([self.n_channels,128,128])
        self.n_filter = self.n_channels
        self.quanto_k = None
        self.quanto_b = None

        
        #TODO: considera che è sempre su gpu
        if self.enable_gpu:
            self.use_gpu=True
            self.M = self.multiplier
            #TODO: parametrizare il k
            self.blockdim = (2,2,4)
            self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1,self.output_shape[2] // (self.blockdim[2]*self.kp) + 1)#,n_channels)
            self.occorenza = None#cuda.to_device(np.zeros((self.n_filter,256,256),dtype=np.int32))
            self.kernel_global_mem = cuda.to_device(np.array(kwargs["weights"],dtype=np.int8))
           
             
            
            self.results = cuda.device_array(self.output_shape, dtype=np.int8)
            self.results2 = cuda.device_array(self.output_shape, dtype=np.int32)

            self.gpu_input_memory = kwargs["gpu_input_memory"]

            if ( kwargs["quant_data"] is not None):
                self.quantization=True

                self.quanto_b = cuda.to_device(np.ascontiguousarray(kwargs["quant_bias"]))
                self.quanto_k = cuda.to_device(np.ascontiguousarray(kwargs["quant_data"]))

                self.update_bias = cuda.to_device(np.ascontiguousarray(np.zeros(self.n_filter)))
                
                self.k_mul = cuda.to_device(np.ascontiguousarray(np.double( kwargs["quant_data"])*kwargs["quant_input_k"],dtype=np.double))#TODO:parametrizare il 255
                if(self.DEPTHWISE_CONV_2D):
                    self.weights = cuda.to_device(np.ascontiguousarray(np.sum(kwargs["weights"],(0,1,2),dtype=np.double)*kwargs["quant_data"]*kwargs["quant_input_offset"]*kwargs["quant_input_k"],dtype=np.double))#TODO:parametrizare il diviso 2 con alfa input+offest input
                
                else:
                    self.weights = cuda.to_device(np.ascontiguousarray(np.sum(kwargs["weights"],(1,2,3),dtype=np.double)*kwargs["quant_data"]*kwargs["quant_input_offset"]*kwargs["quant_input_k"],dtype=np.double))#TODO:parametrizare il diviso 2 con alfa input+offest input
                
                self.k_bias = cuda.to_device(np.ascontiguousarray(kwargs["biases"]*kwargs["quant_bias"],dtype=np.double))

                self.output_mul= 1.0/kwargs["quant_output_k"]
                self.output_offset= kwargs["quant_output_offset"]

            if self.print_output:
                self.outputv = np.zeros(self.output_shape)              
        else:
            self.convkernel, self.biases =kwargs["weights"], kwargs["biases"]
            self.outputv = np.zeros(self.output_shape)
        
        
        self.test_cuda.setPointerData(None,
                                      self.results.device_ctypes_pointer.value,
                                      self.kernel_global_mem.device_ctypes_pointer.value,
                                      self.k_mul.device_ctypes_pointer.value,
                                      self.weights.device_ctypes_pointer.value,
                                      self.k_bias.device_ctypes_pointer.value,
                                      self.output_mul,self.output_offset)
                
        self.test_cuda.setSizeData(self.input_shape[0],self.input_shape[1],self.input_shape[2],self.output_shape[0],self.output_shape[1],self.output_shape[2],
                                   self.kernel_shape[0],self.kernel_shape[1],self.kernel_shape[2],self.kernel_shape[3],256)
           
        self.test_cuda.setStride(self.stride[0],self.stride[1],0)
        
        #TODO: valutare se spostare nella convLayerBase
        self.padding_kernel = (self.padding_type != 'valid')#mannagia
        self.fake_kernel = (kwargs["weights"].shape[1] == 1 and kwargs["weights"].shape[2] == 1)
        self.normal_kernel = not self.padding_kernel and not self.fake_kernel
        if(self.activation == "relu" or self.activation == "Relu"):
            
            self.activation = 1
        elif(self.activation == "relu6" or self.activation == "Relu6"):
            self.activation = 6
        else:
            self.activation = 0
            
        #if True:#None == self.gpu_input_memory:#TODO:parametrizare meglio
                #self.outputv = np.zeros(self.output_shape,dtype=np.int32)          
        return self.output_shape
  
    # def cuda_set(self,A_global_mem ):
       
    #     #self.test_cuda.setConvolutiontexSrc(A_global_mem.device_ctypes_pointer())
        
    #     self.test_cuda.setPointerData(A_global_mem.device_ctypes_pointer.value,
    #                                   self.results.device_ctypes_pointer.value,
    #                                   self.kernel_global_mem.device_ctypes_pointer.value,
    #                                   self.k_mul.device_ctypes_pointer.value,
    #                                   self.weights.device_ctypes_pointer.value,
    #                                   self.k_bias.device_ctypes_pointer.value,
    #                                   self.output_mul,self.output_offset)
                
    #     self.test_cuda.setSizeData(self.input_shape[0],self.input_shape[1],self.input_shape[2],self.output_shape[0],self.output_shape[1],self.output_shape[2],
    #                                self.kernel_shape[0],self.kernel_shape[1],self.kernel_shape[2],self.kernel_shape[3],256)
                                   
    #     self.test_cuda.setPointerInput(A_global_mem.device_ctypes_pointer.value,
    #                                   self.activation)

    #     self.test_cuda.setPointerMul(self.M.device_ctypes_pointer.value)
        
    #     self.test_cuda.setStride(self.stride[0],self.stride[1],self.pre_layer.output_offset)
    def load_input_layer(self,layers,tensors_out):
        
        super().load_input_layer(layers,tensors_out)
        self.test_cuda.cuda_set( self,None )
        if not self.fake_kernel and not self.normal_kernel:
                self.value_null2 = self.pre_layer.output_offset
                self.test_cuda.setStride(self.stride[0],self.stride[1], self.value_null2)
        
    def research_hyperparameters(self):
        
        best_blockdim = self.blockdim
        best_griddim = self.griddim 
        best_kp = self.kp
        best_time = 100000000
        for i in range(0,16):
            for j in range(0,10):
                for k in range(0,5):
                    for kp in range(1,5):
                        if k*kp <=self.output_shape[2]:
                            self.kp = kp
                            self.blockdim = (i+1,j+1,k+1)
                            self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1,self.output_shape[2] // (self.blockdim[2]*kp) + 1)
                            init_time = time.time()
                            
                            for asd in range(2):
                                self.forward_pass()
                                
                            tot_time = time.time() - init_time
                            #print("blockdim:",self.blockdim,"griddim:",self.griddim,"time:",tot_time)
                            if tot_time < best_time:
                                best_blockdim = self.blockdim
                                best_griddim = self.griddim
                                best_time = tot_time
                                best_kp = self.kp
                
        print("best_blockdim:",best_blockdim,"best_griddim:",best_griddim,"kp:",best_kp,"time:",best_time)
        self.kp = best_kp
        self.blockdim = best_blockdim
        self.griddim = best_griddim