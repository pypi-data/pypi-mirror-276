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
from inspectnn.Pooling.Pool_kernel import pool, pool_avg, pool2d, pool_avg2d , pool_quant,pool_avg_quant
from inspectnn.Pooling.Pool_cuda import Pool_cuda

class PoolingLayer_TFLITE(BaseLayer):
    layer_name = "Pool"
    total_type_layer_time = 0
    def __init__(self, stride = (1, 1), pool_size = (2, 2), pooling = "max", name = "layer", input_memory = None):
        super().__init__(self, name = name)
        self.stride = stride
        self.pool_size = pool_size
        self.pool = pooling
        self.preA = None
        self.quant = False

    def __deepcopy__(self, memo = None):
        return PoolingLayer_TFLITE(stride = self.stride, pool_size = self.pool_size, pooling = self.pool, name = self.name)

    #@jit
    def forward_pass(self):
        if self.preA != self.pre_layer.results:
            A_global_mem = self.pre_layer.results
            self.preA  = A_global_mem
            #self.test_cuda.setConvolutiontexSrc(A_global_mem.device_ctypes_pointer())
            #print(self.name,"Ok ####################################################")
            self.test_cuda.cuda_set(self, A_global_mem )
        else:
            A_global_mem = self.preA
            
        #A_global_mem=self.pre_layer.results
        avg = (self.pool == "avg" or self.pool == "Avg")

        if avg:
            cuda.synchronize()
            if self._2d:
                if self.quant:
                    print("!!!! Implementare pool_avg2d quantizzata !!!!")
                else:
                    pool_avg2d[self.griddim, self.blockdim](self.results, A_global_mem,self.stride_global_mem, self.pool_size_global_mem,self.k_p)#, pooling)
            else:
                
                if self.quant:
                    #print("pool")
                    #self.test_cuda.print_parameters()
                    self.test_cuda.PoolGPU()
                    #print(self.name,"output:",self.quant_results.copy_to_host())
                    #pool_avg_quant[self.griddim, self.blockdim](self.quant_results, A_global_mem,self.stride_global_mem, self.pool_size_global_mem,self.quant_output_mul,self.quant_output_offset)
                    #print(self.name,"output:",self.quant_results.copy_to_host())
                else:
                    pool_avg      [self.griddim, self.blockdim](self.results, A_global_mem,self.stride_global_mem, self.pool_size_global_mem,self.k_p)

        else:
            cuda.synchronize()
            if self._2d:
                if self.quant:
                    print("!!!! Implementare pool2d quantizzata !!!!")
                else:
                    pool2d[self.griddim, self.blockdim](self.results, A_global_mem,self.stride_global_mem, self.pool_size_global_mem,self.k_p)#, pooling)
        
            else:
                if self.quant:
                    pool_quant[self.griddim, self.blockdim](self.results, A_global_mem,self.stride_global_mem, self.pool_size_global_mem,self.k_p,self.quant_output_mul,self.quant_output_offset,self.output_mul, self.output_offset)
                
                else:
                    pool[self.griddim, self.blockdim](self.results, A_global_mem,self.stride_global_mem, self.pool_size_global_mem,self.k_p)#, pooling)
        
        
        #print(self.name,"output:\n",self.results.copy_to_host()[0][0])
        #if self.gpu_output_memory == False:
            #self.outputv[:,:,:] =self.results.copy_to_host()


    def load_weights(self, **kwargs):
        
        self.test_cuda = Pool_cuda()
         
        self.input_shape, self.enable_gpu = kwargs["input_shape"],kwargs["enable_gpu"]
        #print(self.pool_size,self.stride)
        if "output_shape" in kwargs :
            #print("output_shape",kwargs["output_shape"])
            self.output_shape = kwargs["output_shape"]
        else:
            self.output_shape = [int(np.floor((self.input_shape[i] - self.pool_size[i]) / self.stride[i]) + 1) for i in range(2)] + [self.input_shape[2]]      
        
        self._2d = len(self.output_shape) == 2
        self.outputv = np.zeros(self.output_shape)
        
        if self.enable_gpu:
            self.k_p=1
            if self._2d:
                self.blockdim = (8,8)
                self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1)#,n_channels)
            
            else:
                self.blockdim = (1,1,1)
                self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1,self.output_shape[2] // (self.blockdim[2]*self.k_p) + 1)#,n_channels)
            self.use_gpu=True

            self.results = cuda.device_array(self.output_shape, dtype=np.int8)
            self.stride_global_mem = cuda.to_device(self.stride)
            self.pool_size_global_mem = cuda.to_device(self.pool_size)
            self.gpu_input_memory = kwargs["gpu_input_memory"]

            self.output_mul= 1/kwargs["quant_output_k"]
            self.output_offset= kwargs["quant_output_offset"]
        return self.output_shape
    
    
    def research_hyperparameters(self):
        
        best_blockdim = self.blockdim
        best_griddim = self.griddim 
        best_kp = self.kp
        best_time = 100000000
        for i in range(0,4):
            for j in range(0,4):
                for k in range(1,8):
                    for kp in range(1,32):
                        if k*kp <= self.output_shape[2]:
                            self.k_p = kp
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
                                best_kp = self.k_p
            
        print("best_blockdim:",best_blockdim,"best_griddim:",best_griddim,"kp:",best_kp,"time:",best_time)
        self.k_p = best_kp
        self.blockdim = best_blockdim
        self.griddim = best_griddim