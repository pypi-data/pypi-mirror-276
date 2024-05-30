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
from inspectnn.Add.Add_kernel_tflite import add3d_tflite,add3dv2_tflite
import os

import ctypes

class Test_cuda(object):
    def __init__(self, size_H=3, SIZE_W=3, size_filter=3):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.lib = ctypes.cdll.LoadLibrary(f'{dir_path}/libAddTexture.so')
        #self.lib = ctypes.cdll.LoadLibrary('/home/ssaa/Git/inspect-nn/inspectnn/Conv/conv_cuda/convolutionTexture/libconvolutionTexture.so')
        self.size_H = size_H
        self.size_W = SIZE_W
        self.size_filter = size_filter

        self.lib.cuda_add.argtypes = [ctypes.c_void_p]
        self.lib.cuda_add.restype = ctypes.c_void_p
        

        #lib.DataConv
        self.lib.getStruct.argtypes = []
        self.lib.getStruct.restype =  ctypes.c_void_p
        self.obj = self.lib.getStruct()
        #self.obj = lib.convolutionRowsGPU(val)
        
        self.lib.setSizeData.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
        self.lib.setSizeData.restype =  ctypes.c_void_p
        
        self.lib.setPointerMul.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
        self.lib.setPointerMul.restype = ctypes.c_void_p
        
        
        self.lib.setPointerData.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,
                                                        ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,
                                                        ctypes.c_float,ctypes.c_int]
        self.lib.setPointerData.restype = ctypes.c_void_p
        
        self.lib.print_parameters.argtypes= [ctypes.c_void_p]
        
        self.lib.setData.argtypes = [ctypes.c_void_p,ctypes.c_float,ctypes.c_float,ctypes.c_float,ctypes.c_float]
        
        
        self.lib.setPointerInput.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]

    def setPointerInput(self,Input,activation):
        self.lib.setPointerInput(self.obj,Input,activation)
        
        
    def setData(self,of_A,k_A,of_B,k_B):
        self.lib.setData(self.obj,of_A,k_A,of_B,k_B)
        
    def setSizeData(self,in_x,in_y,in_z,out_x, out_y, out_z, k_x, k_y, k_z, k_p, size_m):
        self.lib.setSizeData(self.obj,in_x,in_y,in_z,out_x, out_y, out_z, k_x, k_y, k_z, k_p, size_m)
        
        
    def setPointerData(self,Input,d_Dst, Kernel,k_mul,k_filtri,k_bias,out_mul, out_offset):
        self.lib.setPointerData(self.obj,d_Dst, Input, Kernel,k_mul,k_filtri,k_bias,out_mul, out_offset)
            
    def setPointerMul(self, M):
        self.lib.setPointerMul(self.obj,M)
        
        return
    
    def cuda_add(self):
        cuda.synchronize()
        self.lib.cuda_add(self.obj)
         
    def setConvolutionKernel(self,kernel):
        self.lib.setConvolutionKernel(kernel)
    
    def print_parameters(self):
        self.lib.print_parameters(self.obj)


class AddLayer(BaseLayer):
    layer_name = "Add"
    def __init__(self, name = "cocatenate",activation = ""):
        super().__init__(self, name = name)
        self.activation = (activation == "relu" or activation == "Relu")

    def __deepcopy__(self, memo = None):
        return AddLayer(name = self.name)

    def load_weights(self, **kwargs):
        self.input_shape_A,self.input_shape_B, self.enable_gpu = kwargs["input_shape_A"],kwargs["input_shape_B"], kwargs["enable_gpu"] 
        self.output_shape = kwargs["output_shape"]
        self.outputv = np.zeros(self.output_shape)

        self.blockdim = (2,2,8)
        self.stride = 1
        self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1,self.output_shape[2] // (self.stride*self.blockdim[2]) + 1)#,n_channels)

        self.test_cuda = Test_cuda()
        
        
        
        if self.enable_gpu:
            self.use_gpu = True
           
            self.results = cuda.device_array(self.output_shape, dtype=np.int8)
            self.gpu_layer_A = None
            self.gpu_layer_B = None

            self.output_K = kwargs["quant_output_k"]
            self.output_mul = 1/kwargs["quant_output_k"]
            self.output_offset = kwargs["quant_output_offset"]
        return self.output_shape
    
    #@jit
    def forward_pass(self):
        if self.gpu_layer_A is None:
            print("add no buoeno")

        else:
            
            
            
            self.test_cuda.cuda_add()
            #cuda.synchronize()
            #add3d_tflite[self.griddim, self.blockdim](self.results,self.gpu_layer_A.results,self.gpu_layer_B.results,
            #                                         self.A_mul,self.B_mul, self.A_off,self.B_off,
            #                                         self.activation,self.output_mul,self.output_offset)


            

    def load_input_layer(self,layers,tensors_out):
        op_in1=self.code_tensor_inputs[0]
        op_in2=self.code_tensor_inputs[1]

        self.gpu_layer_A = layers[tensors_out.index(op_in1)]
        self.gpu_layer_B = layers[tensors_out.index(op_in2)]

        self.gpu_output_memory = True

        self.A_mul=1/self.gpu_layer_A.output_mul
        self.B_mul=1/self.gpu_layer_B.output_mul

        self.A_off=self.gpu_layer_A.output_offset*1.0
        self.B_off=self.gpu_layer_B.output_offset*1.0
        
        self.cuda_set()
        
        
        
      
    def cuda_set(self ):
       
        #self.test_cuda.setConvolutiontexSrc(A_global_mem.device_ctypes_pointer())
        
        self.test_cuda.setPointerData(self.gpu_layer_A.results.device_ctypes_pointer.value,
                                      self.results.device_ctypes_pointer.value,
                                      self.gpu_layer_B.results.device_ctypes_pointer.value,
                                      None,None,None,
                                      self.output_mul,self.output_offset)
                
        self.test_cuda.setSizeData(self.input_shape_A[0],self.input_shape_A[1],self.input_shape_A[2],self.output_shape[0],self.output_shape[1],self.output_shape[2],
                                   self.input_shape_B[0],self.input_shape_B[1],self.input_shape_B[2],0,256)
                                   
        self.test_cuda.setPointerInput(self.gpu_layer_A.results.device_ctypes_pointer.value,
                                      self.activation)

        self.test_cuda.setData(self.A_off,self.A_mul,self.B_off,self.B_mul)

        