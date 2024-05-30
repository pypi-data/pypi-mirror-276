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
from inspectnn.Conv.Conv_kernel_tflite import convolve_tflite_occorenza,convolve_tflite, convolve_tflite_padding,convolve_tflite_fake,convolve_tflite_mf, convolve_tflite_padding_mf,convolve_tflite_fake_mf
from inspectnn.Conv.ConvLayer import ConvLayer

import ctypes

class Conv_cuda(object):
    def __init__(self, size_H=3, SIZE_W=3, size_filter=3):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.lib = ctypes.cdll.LoadLibrary(f'{dir_path}/libconvolutionTexture.so')
        #self.lib = ctypes.cdll.LoadLibrary('/home/ssaa/Git/inspect-nn/inspectnn/Conv/conv_cuda/convolutionTexture/libconvolutionTexture.so')
        self.size_H = size_H
        self.size_W = SIZE_W
        self.size_filter = size_filter

        # Declare input and output types for each method you intend to use
        #float *d_Dst, int imageW,int imageH, cudaTextureObject_t texSrc
        self.lib.convolutionRowsGPU.argtypes = [ctypes.c_void_p]
        self.lib.convolutionRowsGPU.restype = ctypes.c_void_p
        
        self.lib.convolutionRowsGPU_fake.argtypes = [ctypes.c_void_p]
        self.lib.convolutionRowsGPU_fake.restype =  ctypes.c_void_p
        
        self.lib.convolutionRowsGPU_padding.argtypes = [ctypes.c_void_p]
        self.lib.convolutionRowsGPU_padding.restype =  ctypes.c_void_p
        
        self.lib.convolutionRowsGPU_deepwise.argtypes = [ctypes.c_void_p]
        self.lib.convolutionRowsGPU_deepwise.restype = ctypes.c_void_p
        
        self.lib.convolutionRowsGPU_padding_deepwise.argtypes = [ctypes.c_void_p]
        self.lib.convolutionRowsGPU_padding_deepwise.restype =  ctypes.c_void_p
        
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
                                                        ctypes.c_double,ctypes.c_int]
        self.lib.setPointerData.restype = ctypes.c_void_p
        
        self.lib.print_parameters.argtypes= [ctypes.c_void_p]
        
        self.lib.setStride.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int]
        
        
        self.lib.setPointerInput.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_char]

    def setPointerInput(self,Input,activation):
        #print("Activation: ",activation)
        self.lib.setPointerInput(self.obj,Input,activation)
        
        
    def setStride(self,x,y,val_null=0):
        self.lib.setStride(self.obj,x,y,val_null)
        
    def setSizeData(self,in_x,in_y,in_z,out_x, out_y, out_z, k_x, k_y, k_z, k_p, size_m):
        self.lib.setSizeData(self.obj,in_x,in_y,in_z,out_x, out_y, out_z, k_x, k_y, k_z, k_p, size_m)
        
        
    def setPointerData(self,Input,d_Dst, Kernel,k_mul,weights,k_bias,out_mul, out_offset):
        self.lib.setPointerData(self.obj,d_Dst, Input, Kernel,k_mul,weights,k_bias,out_mul, out_offset)
            
    def setPointerMul(self, M):
        self.lib.setPointerMul(self.obj,M)
        
        return
    
    def convolutionRowsGPU_fake(self):
        cuda.synchronize()
        self.lib.convolutionRowsGPU_fake(self.obj)
    
    def convolutionRowsGPU_padding(self):
        cuda.synchronize()
        self.lib.convolutionRowsGPU_padding(self.obj)
       
    def convolutionRowsGPU(self):
        cuda.synchronize()
        self.lib.convolutionRowsGPU(self.obj)
    
    def convolutionRowsGPU_deepwise(self):
        cuda.synchronize()
        self.lib.convolutionRowsGPU_deepwise(self.obj)
    def convolutionRowsGPU_padding_deepwise(self):
        cuda.synchronize()
        self.lib.convolutionRowsGPU_padding_deepwise(self.obj)
           
    def print_parameters(self):
        self.lib.print_parameters(self.obj)

    def cuda_set(self,classLayer,A_global_mem ):
       
        if A_global_mem is not None:
            self.setPointerData(A_global_mem.device_ctypes_pointer.value,
                                      classLayer.results.device_ctypes_pointer.value,
                                      classLayer.kernel_global_mem.device_ctypes_pointer.value,
                                      classLayer.k_mul.device_ctypes_pointer.value,
                                      classLayer.weights.device_ctypes_pointer.value,
                                      classLayer.k_bias.device_ctypes_pointer.value,
                                      classLayer.output_mul,classLayer.output_offset)
            
            self.setPointerInput(A_global_mem.device_ctypes_pointer.value,
                                      classLayer.activation)
            self.setPointerMul(classLayer.M.device_ctypes_pointer.value)
            
        self.setSizeData(classLayer.input_shape[0],classLayer.input_shape[1],classLayer.input_shape[2],classLayer.output_shape[0],classLayer.output_shape[1],classLayer.output_shape[2],
                                   classLayer.kernel_shape[0],classLayer.kernel_shape[1],classLayer.kernel_shape[2],classLayer.kernel_shape[3],256)

        self.setStride(classLayer.stride[0],classLayer.stride[1],classLayer.pre_layer.output_offset)
        
    