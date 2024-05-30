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
from numba import cuda, int8,int32,uint8
import numpy as np
from tqdm import tqdm

@cuda.jit(cache=True)    
def convolve_tflite_occorenza(result,a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,stride,occorenza,K_p):

    x, y,p = cuda.grid(3) 
    n_channels = params[0]
    offset1 = params[1]
    offset2 = params[2]
    p=K_p*p
    max_x=result.shape[0]
    max_y=result.shape[1]

    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return  


    xi = stride[0] * x
    yi = stride[1] * y

    range_i = range(xi,xi+b.shape[1])
    range_j = range(yi,yi+b.shape[2])
    range_p = range(0,K_p)
    
    s = cuda.local.array(shape=(K_p), dtype=int32)

    for pp in range_p:
        s[pp]=0
        #calcolo cella convoluzione
        #todo: aggiungere lo step
    for i in range_i:
        for j in range_j:
            for k in range(b.shape[3]):
                #s+=1
                A = uint8(a[i,j,k]+offset1)
                for pp in range_p:
                    s[pp] += M[A,uint8(b[pp+p,i-xi,j-yi,k]+offset2)]
                    occorenza[pp+p,A,int8(b[pp+p,i-xi,j-yi,k]+offset2)] += 1

    for pp in range_p:
        ris = s[pp]*k_mul[pp+p] - k_filtri[pp+p] + k_bias[pp+p]

        if activation and ris<0:
            ris =0
        result[x,y,pp+p] = round(ris*out_mul + out_offest)


@cuda.jit(cache=True)    
def convolve_tflite(result,a,b,params,k_mul,k_filtri,k_bias,
                    M,activation,out_mul,out_offest,stride,update_bias,K_p):

    x, y,p = cuda.grid(3) 
    n_channels = params[0]
    offset1 = params[1]
    offset2 = params[2]
    p=K_p*p
    max_x=result.shape[0]
    max_y=result.shape[1]

    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return  


    xi = stride[0] * x
    yi = stride[1] * y

    range_i = range(xi,xi+b.shape[1])
    range_j = range(yi,yi+b.shape[2])
    range_p = range(0,K_p)
    
    s = cuda.local.array(shape=(16), dtype=int32)

    for pp in range_p:
        s[pp]=0
        #calcolo cella convoluzione
        #todo: aggiungere lo step
        
    for i in range_i:
        for j in range_j:
            for k in range(b.shape[3]):
                #s+=1
                A = uint8(a[i,j,k]+offset1)
                for pp in range_p:
                    s[pp] += M[A,uint8(b[pp+p,i-xi,j-yi,k]+offset2)]

    for pp in range_p:
        ris = s[pp]*k_mul[pp+p] - k_filtri[pp+p] + k_bias[pp+p] 

        if activation and ris<0:
            ris =0
        if activation == 6 and ris>6:
            ris =6
        result[x,y,pp+p] = round(ris*out_mul + out_offest)

@cuda.jit(cache=True)  
def convolve_tflite_padding(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,value_null,stride,update_bias,K_p):

    x, y,p = cuda.grid(3)
    n_channels = params[0]
    offset1 = params[1]
    offset2 = params[2]  
    max_x=result.shape[0]
    max_y=result.shape[1]

    p=K_p*p
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return
   
    xi = stride[0] * x
    yi = stride[1] * y
    
    delta_i = int((b.shape[1]-1)/2)
    delta_j = int((b.shape[2]-1)/2)
    

    if(stride[0] > 1):
        offset_i=xi -delta_i+1 
        
    else:
        offset_i=xi-delta_i
        
       
        

    if(stride[1] > 1):
        offset_j=yi-delta_j+1
       
    else:
        offset_j=yi-delta_j
    
    delta_i=2*delta_i
    delta_j=2*delta_j

    range_i = range(offset_i,offset_i+delta_i+1)
    range_j = range(offset_j,offset_j+delta_j+1)
    range_p = range(0,K_p)
    
        #calcolo cella convoluzione
        #todo: aggiungere lo step
    s = cuda.local.array(shape=(16), dtype=int32)

    for pp in range_p:
        s[pp]=0

    for i in range_i:
        for j in range_j:
            for k in range(b.shape[3]):
                #s+=1
                if i >= 0 and  i<a.shape[0] and j >= 0 and j < a.shape[1]:
                    A=uint8(a[i,j,k]+offset1)
                    for pp in range_p:
                        s[pp] += M[A,uint8(b[pp+p,i-offset_i,j-offset_j,k]+offset2)]
                else:
                    A=uint8(value_null+offset1)
                    for pp in range_p:
                        s[pp] += M[A,uint8(b[pp+p,i-offset_i,j-offset_j,k]+offset2)]

    for pp in range_p:
        ris = s[pp]*k_mul[pp+p] - k_filtri[pp+p] + k_bias[pp+p]

        if activation and ris<0:
            ris =0
        
        if activation == 6 and ris>6:
            ris =6
            
        result[x,y,pp+p] = round(ris*out_mul + out_offest)


@cuda.jit(cache=True)  
def convolve_deepwise(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,stride,update_bias):

    x, y,p = cuda.grid(3)
    n_channels = result.shape[2]
    offset1 = params[1]
    offset2 = params[2]  
    max_x=result.shape[0]
    max_y=result.shape[1]

   
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return
   
    xi = stride[0] * x
    yi = stride[1] * y

    range_i = range(xi,xi+b.shape[1])
    range_j = range(yi,yi+b.shape[2])
    
    
        #calcolo cella convoluzione
        #todo: aggiungere lo step

    s = cuda.local.array(shape=(1), dtype=int32)

    k=p
    for i in range_i:
        for j in range_j:
            
            #s+=1
            A = uint8(a[i,j,k]+offset1)
            s[0] += M[A,uint8(b[0,i-xi,j-yi,k]+offset2)]

    
    ris = s[0]*k_mul[p] - k_filtri[p] + k_bias[p] 

    if activation>0 and ris<0:
        ris =0
        
    if activation == 6 and ris>6: ris =6
    result[x,y,p] = round(ris*out_mul + out_offest)


@cuda.jit(cache=True)  
def convolve_deepwise_padding(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,value_null,stride,update_bias):

    x, y,p = cuda.grid(3)
    n_channels = result.shape[2]
    offset1 = params[1]
    offset2 = params[2]  
    max_x=result.shape[0]
    max_y=result.shape[1]

   
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return
   
    xi = stride[0] * x
    yi = stride[1] * y
    
    delta_i = int((b.shape[1]-1)/2)
    delta_j = int((b.shape[2]-1)/2)
    

    if(stride[0] > 1):
        offset_i=xi
        delta_i=2*delta_i
    else:
        offset_i=xi-delta_i
        

    if(stride[1] > 1):
        offset_j=yi
        delta_j=2*delta_j
    else:
        offset_j=yi-delta_j

    range_i = range(offset_i,xi+delta_i+1)
    range_j = range(offset_j,yi+delta_j+1)
    
    
        #calcolo cella convoluzione
        #todo: aggiungere lo step

    s = cuda.local.array(shape=(1), dtype=int32)

    k=p
    for i in range_i:
        for j in range_j:
        
            #s+=1
            if i >= 0 and  i<a.shape[0] and j >= 0 and j < a.shape[1]:
                A=uint8(a[i,j,k]+offset1)
                
                s[0] += M[A,uint8(b[0,i-offset_i,j-offset_j,p]+offset2)]
            else:
                A=uint8(value_null+offset1)
                
                s[0] += M[A,uint8(b[0,i-offset_i,j-offset_j,p]+offset2)]

    
    ris = s[0]*k_mul[p] - k_filtri[p] + k_bias[p] 

    if activation > 0 and ris<0:
        ris =0
    
        
    if activation == 6 and ris>6: ris =6
    
    result[x,y,p] = round(ris*out_mul + out_offest)

@cuda.jit(cache=True)  
def convolve_tflite_fake(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,stride,update_bias,K_p):

    #impone che la dimensione del kernel sia 1x1
    x, y,p = cuda.grid(3)    
    max_x=result.shape[0]
    max_y=result.shape[1]
    
    p=K_p*p
    n_channels = params[0]
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return
    
    offset1 = params[1]
    offset2 = params[2]
    
    xi = stride[0] * x
    yi = stride[1] * y
    
    range_p = range(0,K_p)
    
        #calcolo cella convoluzione
        #todo: aggiungere lo step
    s = cuda.local.array(shape=(16), dtype=int32)

    for pp in range_p:
        s[pp]=0

    for k in range(b.shape[3]):

        A=uint8(a[xi,yi,k]+offset1)
        for pp in range_p:
            #s[pp] += M[A,uint8(b[pp+p,0,0,k]+offset2)]
            s[pp] += A*b[pp+p,0,0,k]

    for pp in range_p:
        
        ris = s[pp]*k_mul[pp+p] - k_filtri[pp+p] + k_bias[pp+p] # #unire k_filtri e k_bias

        if activation and ris<0:
            ris =0
            
        if activation == 6 and ris>6:
            ris =6
            
        result[x,y,pp+p] = round(ris*out_mul + out_offest)


@cuda.jit(cache=True)
def quant_3d_FakeMinMax(results, values,tmp_max,tmp_min,quant_nbits):

    i, j,k = cuda.grid(3)
    
    max_i=results.shape[0]
    max_j=results.shape[1]
    max_k=results.shape[2]
    
    #if the thread coordinates are outside of the image, we ignore the thread:
    if ((i >= max_i)  or (j >= max_j) or (k >= max_k)): 
        return

    t_min=tmp_min[0,1,2]
    t_max=tmp_max[0,1,2]

    #TODO:fare variante per ogni canale, mannacia
    results[i,j,k] = round(156* (values[i,j,k] -48 - t_min)/(t_max-2*t_min))#TODO:parametrizare il 48 e 56 dai dati del tflite


#kernel con multi filtro



@cuda.jit(cache=True)    
def convolve_tflite_mf(result,a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,stride,idx_multiply,K_p):

    x, y,p = cuda.grid(3) 
    
    p=K_p*p
    max_x=result.shape[0]
    max_y=result.shape[1]
    n_channels = params[0]
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return  

   
    offset1 = params[1]
    offset2 = params[2]
    xi = stride[0] * x
    yi = stride[1] * y

    range_i = range(xi,xi+b.shape[1])
    range_j = range(yi,yi+b.shape[2])
    range_p = range(0,K_p)
    
    s = cuda.local.array(shape=(16), dtype=int32)

    for pp in range_p:
        s[pp]=0
        #calcolo cella convoluzione
        #todo: aggiungere lo step
    for i in range_i:
        for j in range_j:
            for k in range(b.shape[3]):
                #s+=1
                A = int8(a[i,j,k]+offset1)
                for pp in range_p:
                    
                    s[pp] += M[int8(idx_multiply[pp+p]),A,int8(b[pp+p,i-xi,j-yi,k]+offset2)]

    for pp in range_p:
        ris = s[pp]*k_mul[pp+p] - k_filtri[pp+p] + k_bias[pp+p]

        if activation and ris<0:
            ris =0
        result[x,y,pp+p] = round(ris*out_mul + out_offest)

@cuda.jit(cache=True)  
def convolve_tflite_padding_mf(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,value_null,stride,idx_multiply,K_p):

    x, y,p = cuda.grid(3)    
    max_x=result.shape[0]
    max_y=result.shape[1]
    n_channels = params[0]
    p=K_p*p
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return
    
  
    offset1 = params[1]
    offset2 = params[2]
    xi = stride[0] * x
    yi = stride[1] * y
    
    delta_i = int((b.shape[1]-1)/2)
    delta_j = int((b.shape[2]-1)/2)
    

    if(stride[0] > 1):
        offset_i=xi
        delta_i=2*delta_i
    else:
        offset_i=xi-delta_i
        

    if(stride[1] > 1):
        offset_j=yi
        delta_j=2*delta_j
    else:
        offset_j=yi-delta_j

    range_i = range(offset_i,xi+delta_i+1)
    range_j = range(offset_j,yi+delta_j+1)
    range_p = range(0,K_p)
    
        #calcolo cella convoluzion
        #todo: aggiungere lo step
    s = cuda.local.array(shape=(16), dtype=int32)

    for pp in range_p:
        s[pp]=0

    for i in range_i:
        for j in range_j:
            for k in range(b.shape[3]):
                #s+=1
                if i >= 0 and  i<a.shape[0] and j >= 0 and j < a.shape[1]:
                    A=int8(a[i,j,k]+offset1)
                    for pp in range_p:
                        s[pp] += M[int8(idx_multiply[pp+p]),A,int8(b[pp+p,i-offset_i,j-offset_j,k]+offset2)]
                else:
                    for pp in range_p:
                        A=int8(value_null+offset1)
                        s[pp] += M[int8(idx_multiply[pp+p]),A,int8(b[pp+p,i-offset_i,j-offset_j,k]+offset2)]

    for pp in range_p:
        ris = s[pp]*k_mul[pp+p] - k_filtri[pp+p] + k_bias[pp+p]

        if activation and ris<0:
            ris =0

        result[x,y,pp+p] =round(ris*out_mul + out_offest)


@cuda.jit(cache=True)  
def convolve_tflite_fake_mf(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,stride,idx_multiply,K_p):

    #impone che la dimensione del kernel sia 1x1
    x, y,p = cuda.grid(3)    
    max_x=result.shape[0]
    max_y=result.shape[1]

    p=K_p*p
   
    
    n_channels = params[0]
    offset1 = params[1]
    offset2 = params[2]
    xi = stride[0] * x
    yi = stride[1] * y
    
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return

    range_p = range(0,K_p)
    
        #calcolo cella convoluzione
        #todo: aggiungere lo step
    s = cuda.local.array(shape=(16), dtype=int32)

    for pp in range_p:
        s[pp]=0


    for k in range(b.shape[3]):

        A=int8(a[xi,yi,k]+offset1)
        for pp in range_p:
            s[pp] += M[int8(idx_multiply[pp+p]),A,int8(b[pp+p,0,0,k]+offset2)]


    for pp in range_p:
        ris = s[pp]*k_mul[pp+p] - k_filtri[pp+p] + k_bias[pp+p]

        if activation and ris<0:
            ris =0

        result[x,y,pp+p] =round(ris*out_mul + out_offest)
        
        
#Convoluzione per fibre

@cuda.jit(cache=True)    
def convolve_tflite_mfiber(result,a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,stride,idx_multiply,K_p):
    
    x, y, p = cuda.grid(3) 
    max_x=result.shape[0]
    max_y=result.shape[1]
    
    p=K_p*p

    n_channels = params[0]
    
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return 
    
    offset1 = params[1]
    offset2 = params[2]
    xi = stride[0] * x
    yi = stride[1] * y

    range_i = range(xi,xi+b.shape[1])
    range_j = range(yi,yi+b.shape[2])
    range_p = range(0,K_p)
    
    s = cuda.local.array(shape=(16), dtype=int32)

    s=0
    #calcolo cella convoluzione
    #todo: aggiungere lo step
    for i in range_i:
        for j in range_j:
            for k in range(b.shape[3]):
                A = int8(a[i,j,k]+offset1)
                s += M[np.int8(idx_multiply[x][y]), A, np.int8(b[p, i - xi, j - yi, k] + offset2)]

    
        ris = s*k_mul[p] - k_filtri[p] + k_bias[p]

        if activation and ris<0:
            ris =0
        result[x,y,p] = round(ris*out_mul + out_offest)
        

# def convolve_tflite_mfiber_cpu(result, a, b, params, k_mul, k_filtri, k_bias, M, activation, out_mul, out_offest, stride, idx_multiply, K_p):
#     print("matrice mux:", idx_multiply.copy_to_host())
    
#     max_x = result.shape[0]
#     max_y = result.shape[1]

#     print(params.copy_to_host())
#     n_channels = params[0]

#     offset1 = params[1]
#     offset2 = params[2]

#     for x in tqdm(range(max_x)):
#         for y in range(max_y):
#             for p in range(n_channels):
#                 xi = stride[0] * x
#                 yi = stride[1] * y
                
#                 #print("xi:", xi,"yi:", yi)
#                 s = 0
                
#                 for i in range(xi,xi+b.shape[1]):
#                     for j in range(yi,yi+b.shape[2]):
#                         for k in range(b.shape[3]):
#                             A = np.int8(a[i, j, k] + offset1)
#                             s += M[np.int8(idx_multiply[x][y]), A, np.int8(b[p, i - xi, j - yi, k] + offset2)]
                       
#                 ris = s * k_mul[p] - k_filtri[p] + k_bias[p]

#                 if activation and ris < 0:
#                     ris = 0
#                 result[x, y, p] = round(ris * out_mul + out_offest)


#ANCORA NON TESTATO
@cuda.jit(cache=True)  
def convolve_tflite_fake_mfiber(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,stride,idx_multiply,K_p):

    #impone che la dimensione del kernel sia 1x1
    x, y,p = cuda.grid(3)    
    max_x=result.shape[0]
    max_y=result.shape[1]

    p=K_p*p

    
    n_channels = params[0]
    offset1 = params[1]
    offset2 = params[2]
    xi = stride[0] * x
    yi = stride[1] * y
    
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return
    #range_p = range(0,K_p)
    
        #calcolo cella convoluzione
        #todo: aggiungere lo step
    s = cuda.local.array(shape=(1), dtype=int32)

    #s=0 

    for k in range(b.shape[3]):

        A=int8(a[xi,yi,k]+offset1)
        s[0] += M[int8(idx_multiply[x][y]),A,int8(b[p,0,0,k]+offset2)]


    ris = s[0]*k_mul[p] - k_filtri[p] + k_bias[p]

    if activation and ris<0:
        ris =0

    result[x,y,p] =round(ris*out_mul + out_offest)        
    
    
@cuda.jit(cache=True)  
def convolve_tflite_padding_mfiber(result, a,b,params,k_mul,k_filtri,k_bias,M,activation,out_mul,out_offest,value_null,stride,idx_multiply,K_p):

    x, y,p = cuda.grid(3)    
    max_x=result.shape[0]
    max_y=result.shape[1]
    n_channels = params[0]
    p=K_p*p
    if ((x >= max_x)  or (y >= max_y) or (p >=n_channels)): 
        return
    
  
    offset1 = params[1]
    offset2 = params[2]
    xi = stride[0] * x
    yi = stride[1] * y
    
    delta_i = int((b.shape[1]-1)/2)
    delta_j = int((b.shape[2]-1)/2)
    

    if(stride[0] > 1):
        offset_i=xi
        delta_i=2*delta_i
    else:
        offset_i=xi-delta_i
        

    if(stride[1] > 1):
        offset_j=yi
        delta_j=2*delta_j
    else:
        offset_j=yi-delta_j

    range_i = range(offset_i,xi+delta_i+1)
    range_j = range(offset_j,yi+delta_j+1)
    range_p = range(0,K_p)
    
        #calcolo cella convoluzion
        #todo: aggiungere lo step
    s = cuda.local.array(shape=(16), dtype=int32)

    #for pp in range_p:
    s=0

    for i in range_i:
        for j in range_j:
            for k in range(b.shape[3]):
                #s+=1
                if i >= 0 and  i<a.shape[0] and j >= 0 and j < a.shape[1]:
                    A=int8(a[i,j,k]+offset1)
                    s += M[int8(idx_multiply[x][y]),A,int8(b[p,i-offset_i,j-offset_j,k]+offset2)]
                else:
                    A=int8(value_null+offset1)
                    s += M[int8(idx_multiply[x][y]),A,int8(b[p,i-offset_i,j-offset_j,k]+offset2)]

    ris = s*k_mul[p] - k_filtri[p] + k_bias[p]

    if activation and ris<0:
        ris =0

    result[x,y,p] =round(ris*out_mul + out_offest)      
                