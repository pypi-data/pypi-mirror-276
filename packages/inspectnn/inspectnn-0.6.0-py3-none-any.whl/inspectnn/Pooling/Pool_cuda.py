import  ctypes,os
from numba import cuda

class Pool_cuda(object):
    def __init__(self, size_H=3, SIZE_W=3, size_filter=3):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.lib = ctypes.cdll.LoadLibrary(f'{dir_path}/poolMul.so')
        #self.lib = ctypes.cdll.LoadLibrary('/home/ssaa/Git/inspect-nn/inspectnn/Conv/conv_cuda/convolutionTexture/libconvolutionTexture.so')
        self.size_H = size_H
        self.size_W = SIZE_W

        # Declare input and output types for each method you intend to use
        #float *d_Dst, int imageW,int imageH, cudaTextureObject_t texSrc
        

        self.lib.PoolGPU.argtypes = [ctypes.c_void_p]
        self.lib.PoolGPU.restype =  ctypes.c_void_p
        

        #lib.DataConv
        self.lib.getStruct.argtypes = []
        self.lib.getStruct.restype =  ctypes.c_void_p
        self.obj = self.lib.getStruct()
        #self.obj = lib.convolutionRowsGPU(val)
        
        self.lib.setSizeData.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
        self.lib.setSizeData.restype =  ctypes.c_void_p
        
        self.lib.setStride.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
        self.lib.setStride.restype =  ctypes.c_void_p
        
        self.lib.setPointerData.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p, ctypes.c_float,ctypes.c_int]
        self.lib.setPointerData.restype = ctypes.c_void_p
        
        self.lib.print_parameters.argtypes= [ctypes.c_void_p]
        
        self.lib.setPointerInput.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]

    def setPointerInput(self,Input,activation):
        #print("Activation: ",activation)
        self.lib.setPointerInput(self.obj,Input,activation)
        
        
    def setStride(self,x,y,sizex,sizey):
        self.lib.setStride(self.obj,x,y,sizex,sizey)
        
    def setSizeData(self,in_x,in_y,in_z,out_x,out_y, out_z):
        self.lib.setSizeData(self.obj,in_x,in_y,in_z,out_x,out_y, out_z)
        
        
    def setPointerData(self,Input,d_Dst, out_mul, out_offset):
        self.lib.setPointerData(self.obj,d_Dst, Input,out_mul, out_offset)
            
    def PoolGPU(self):
        cuda.synchronize()
        self.lib.PoolGPU(self.obj)
        
         
    def setMatrixKernel(self,kernel):
        self.lib.setMatrixKernel(kernel)
    
    def setConvolutiontexSrc(self,ASrc):
        self.lib.setConvolutiontexSrc(ASrc)
        
    def setConvolutiontexSrcv2(self,ASrc):
        self.lib.setConvolutiontexSrcv2(ASrc)
        


    def print_parameters(self):
        self.lib.print_parameters(self.obj)
        
        
    def cuda_set(self,classLayer,A_global_mem ):
       
        self.setPointerData(A_global_mem.device_ctypes_pointer.value,
                                      classLayer.results.device_ctypes_pointer.value,
                                      classLayer.output_mul,classLayer.output_offset)
        
        if classLayer._2d:
            self.setSizeData(classLayer.input_shape[0],classLayer.input_shape[1],classLayer.input_shape[2],classLayer.output_shape[0],classLayer.output_shape[1],0)
        else:
            self.setSizeData(classLayer.input_shape[0],classLayer.input_shape[1],classLayer.input_shape[2],classLayer.output_shape[0],classLayer.output_shape[1],classLayer.output_shape[2])
                                   
        self.setPointerInput(A_global_mem.device_ctypes_pointer.value,
                                      classLayer.activation)

        self.setStride(classLayer.stride[0],classLayer.stride[1],classLayer.pool_size[0],classLayer.pool_size[1])