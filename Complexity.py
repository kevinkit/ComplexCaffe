

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 14:02:28 2017

@author: kevinkit

"""

#Define the .prototxt
filename = "deploy.prototxt";

def O_conv(filter_size,input_size,output_size):
    return 1;

proto_file = open(filename,"r");
x = proto_file.readlines();
cnt = 0;
layers = [];
idxs = [];
#num_outputs = [];
#kernel_size = [];
#stride = [];
input_dims = [1,2,3,4];

for i in range(0,len(x)):
    buf = str(x[i]);
    
    if "input_dim" in buf:
        input_dims[cnt] =  int(buf[len("input_dim") +2:len(buf)])
        cnt = cnt +1;
        
        if cnt == 5:
            print "More than 4 dimensions found on input, invalid!";
            break;
 
    #find layers
    if "type" in buf:
        #layers = get_pure(buf,layers);
        idx =  buf.find(":");
        layers.append(buf[idx + 1:len(buf)-1].strip());  
        idxs.append(i);

Param_strings = [];
Param_values = [];


current_dims = [];
O = [];


#iterate over layers
for i in range(0,len(layers)):
    sem = 0;
    if i != len(layers) -1:
        #iterate over params
        for j in range(1,20):
            if "}" in x[idxs[i]+j]:
                #check what was the latest layer to caclulate the dimensions of the input
                if last_layer == "Conv":
                    print "calc conv data";
                    #Do computation for conv here;
                    
                    #Calculate resulting output dimensions
                    
                    current_dims.append([i,int(kernel_size)*int(filter_amount)])   
                   
                    
                    #Caclulate complexity (O) for convolution 
                    

                    #Add complexity for conv to overall complexity
                elif last_layer == "Pool":
                    print "Calc Pool data";
                    
                    if Pool_type == 'MAX':
                         print "max pool..";      
                    elif Pool_type == 'AVG':
                        print "avg pool....";
                    elif Pool_type == 'MIN':
                        print "min pool...";
                
                    
                    
                    
                    
                elif last_layer == "Relu":
                   
                    
                    if Leaky:
                        print "calc for leaky relu"
                    else:
                        print "calc for normal relu"
                        
                    #Calculate resultiing output dimensions
                    
                    
                    #Calculate complexity (O) for pooling
                    

                    #Add complexity for Pool to overall complexity
                elif last_layer == "lrn":
                    print "calculate lrn data";
                elif last_layer == "fc":
                    print "calculate fully connected data";
                elif last_layer == "Dropout":
                    print "Dropout is not used in deployment, therefore not included in calc";
          #      elif last_layer == "Softmax":
          #          print "calculate softmax data";
                
                    

                
                break;
            
            if "param" in x[idxs[i]+j] or layers[i] == "RELU"  or  layers[i] == '"Relu"' or layers[i] == "Relu":
                sem = 1;
            
               
            #Collect params for layer
            if sem == 1:
                buf = x[idxs[i]+j];
                idx =  buf.find(":");
                no_space = buf[0:idx].strip();
                Param_strings.append(no_space);    
                Param_values.append(buf[idx + 1:len(buf)-1])
                
                #Collection data for Conv...
                if layers[i] == "CONVOLUTION" or  layers[i] == '"Convolution"' or layers[i] == "Convolution":
                    last_layer = "Conv";
                    
                    #fill in optional params with default values:
                    stride =1;
                    pad = 0;
                    group = 1;
                    if Param_strings[len(Param_strings)-1] == "num_output":
                       filter_amount = Param_values[len(Param_values)-1];
                    if Param_strings[len(Param_strings)-1] == "kernel_size":
                        kernel_size = Param_values[len(Param_values)-1];
                    if Param_strings[len(Param_strings)-1] == "stride":
                        stride = Param_values[len(Param_values)-1];
                    if Param_strings[len(Param_strings)-1] == "pad":
                        pad = Param_values[len(Param_values)-1];                
                    if Param_strings[len(Param_strings)-1] == "group":
                        group = Param_values[len(Param_values)-1];                
                
                #Relu                                 
                elif layers[i] == "RELU" or  layers[i] == '"Relu"' or layers[i] == "Relu":
                    last_layer = "Relu";
                    Leaky = False;
                    #need to do stuff with leaky relu, cause this will have slightly more operations
                    if Param_strings[len(Param_strings)-1] == "negative_slope":
                        Leaky = True;
                elif layers[i] == "LRN" or  layers[i] == '"Lrn"' or layers[i] == "Lrn":
                    last_layer = "lrn";                    
                    if Param_strings[len(Param_strings)-1] == "local_size":
                        local_size =  Param_values[len(Param_values)-1];
                #Pooling
                elif layers[i] == "POOLING" or  layers[i] == '"Pooling"' or layers[i] == "Pooling":
                    last_layer = "Pool";                    
                    if Param_strings[len(Param_strings)-1] == "pool":
                        Pool_type = Param_values[len(Param_values)-1];
                        Pool_type = Pool_type.strip();                   
                    if Param_strings[len(Param_strings)-1] == "kernel_size":
                        kernel_size = Param_values[len(Param_values)-1];                          
                #Full connected        
                elif layers[i] == "INNER_PRODUCT" or  layers[i] == '"InnerProduct"' or layers[i] == "InnerProduct":
                    last_layer = "fc";
                    if Param_strings[len(Param_strings)-1] == "num_output":
                       fcout = Param_values[len(Param_values)-1];
                #Dropout - NOT USED IN DEPLOYMENET!!! CAREFUL!
                elif layers[i] == "DROPOUT" or  layers[i] == '"Dropout"' or layers[i] == "Dropout":
                    last_layer = "Dropout";
                    if Param_strings[len(Param_strings)-1] == "dropout_ratio":
                       drop_ratio = Param_values[len(Param_values)-1];
                #Softmax
                elif layers[i] == "SOFTMAX" or  layers[i] == '"Softmax"' or layers[i] == "Softmax":
                    last_layer = "Softmax";
                
         
                                                   
       #     print x[idxs[i]+j]
    else:
        if  layers[i] == "SOFTMAX" or  layers[i] == '"Softmax"' or layers[i] == "Softmax":
            print "calc softmax";
