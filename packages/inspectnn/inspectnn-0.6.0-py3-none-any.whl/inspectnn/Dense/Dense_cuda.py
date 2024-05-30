import  ctypes,os
from numba import cuda

class Dense_cuda(object):
    def __init__(self, size_H=3, SIZE_W=3, size_filter=3):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        
        self.lib = ctypes.cdll.LoadLibrary(f'{dir_path}/matrixMul.so')
        #self.lib = ctypes.cdll.LoadLibrary('/home/ssaa/Git/inspect-nn/inspectnn/Conv/conv_cuda/convolutionTexture/libconvolutionTexture.so')
        self.size_H = size_H
        self.size_W = SIZE_W
        self.size_filter = size_filter

        # Declare input and output types for each method you intend to use
        #float *d_Dst, int imageW,int imageH, cudaTextureObject_t texSrc
        
        self.lib.setMatrixKernel.argtypes = [ctypes.c_void_p]
        self.lib.setMatrixKernel.restype = ctypes.c_void_p
        
        
        self.lib.MatrixRowsGPU.argtypes = [ctypes.c_void_p]
        self.lib.MatrixRowsGPU.restype =  ctypes.c_void_p
        

        #lib.DataConv
        self.lib.getStruct.argtypes = []
        self.lib.getStruct.restype =  ctypes.c_void_p
        self.obj = self.lib.getStruct()
        #self.obj = lib.convolutionRowsGPU(val)
        
        self.lib.setSizeData.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_int]
        self.lib.setSizeData.restype =  ctypes.c_void_p
        
        self.lib.setPointerMul.argtypes = [ctypes.c_void_p,ctypes.c_void_p]
        self.lib.setPointerMul.restype = ctypes.c_void_p
        
        
        self.lib.setPointerData.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,
                                                        ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,
                                                        ctypes.c_float,ctypes.c_int]
        self.lib.setPointerData.restype = ctypes.c_void_p
        
        self.lib.print_parameters.argtypes= [ctypes.c_void_p]
        
        self.lib.setPointerInput.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_bool]

    def setPointerInput(self,Input,activation):
        #print("Activation: ",activation)
        self.lib.setPointerInput(self.obj,Input,activation)
        
        
    def setStride(self,x,y,val_null=0):
        self.lib.setStride(self.obj,x,y,val_null)
        
    def setSizeData(self,in_x,in_z,out_x, out_z, k_x, k_y, k_p, size_m):
        self.lib.setSizeData(self.obj,in_x,in_z,out_x, out_z, k_x, k_y, k_p, size_m)
        
        
    def setPointerData(self,Input,d_Dst, Kernel,k_mul,weights,k_bias,out_mul, out_offset):
        self.lib.setPointerData(self.obj,d_Dst, Input, Kernel,k_mul,weights,k_bias,out_mul, out_offset)
            
    def setPointerMul(self, M):
        self.lib.setPointerMul(self.obj,M)
        
        return
    
       
    def MatrixRowsGPU(self):
        cuda.synchronize()
        self.lib.MatrixRowsGPU(self.obj)
        
         
    def setMatrixKernel(self,kernel):
        self.lib.setMatrixKernel(kernel)
    
    def setConvolutiontexSrc(self,ASrc):
        self.lib.setConvolutiontexSrc(ASrc)
        
    def setConvolutiontexSrcv2(self,ASrc):
        self.lib.setConvolutiontexSrcv2(ASrc)
        


    def print_parameters(self):
        self.lib.print_parameters(self.obj)
        
        
    def cuda_set(self,classLayer,A_global_mem ):
        
        #self.test_cuda.setConvolutiontexSrc(A_global_mem.device_ctypes_pointer())
        
        self.setPointerData(A_global_mem.device_ctypes_pointer.value,
                                        classLayer.results.device_ctypes_pointer.value,
                                        classLayer.weights.device_ctypes_pointer.value,
                                        classLayer.k_mul.device_ctypes_pointer.value,
                                        classLayer.k_filtri.device_ctypes_pointer.value,
                                        classLayer.k_bias.device_ctypes_pointer.value,
                                        classLayer.output_mul,classLayer.output_offset)
                
        self.setSizeData(classLayer.input_shape[0],1,classLayer.output_shape[0],1,
                                    classLayer.weights_shape[0],classLayer.weights_shape[1],1,256)
                                    
        self.setPointerInput(A_global_mem.device_ctypes_pointer.value,
                                        classLayer.activation)

        if cuda.is_cuda_array(classLayer.M) :
            self.setPointerMul(classLayer.M.device_ctypes_pointer.value)
           
        
        #self.test_cuda.setStride(self.stride[0],self.stride[1],self.pre_layer.output_offset)