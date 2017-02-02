# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 16:50:03 2017

@author: khoefle
"""

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




#iterate over layers
for i in range(0,len(layers)):
    sem = 0;
    if i != len(layers) -1:
        #iterate over params
        for j in range(1,20):
            if "}" in x[idxs[i]+j]:
                if last_layer == "Conv":
                    #Do computation for conv here
                    print int(kernel_size)*int(filter_amount);
                    current_dimensions = [1,1,1]; #fill in new stuff
                elif last_layer == "Pool":
                    print "pool";
                    
            ##....continue here!


                
                break;
            
            if "param" in x[idxs[i]+j]:
                sem = 1;
                
            if sem == 1:
                buf = x[idxs[i]+j];
                idx =  buf.find(":");
                no_space = buf[0:idx].strip();
                Param_strings.append(no_space);    
                Param_values.append(buf[idx + 1:len(buf)-1])
                
                #Collection data for Conv...
                if layers[i] == "CONVOLUTION" or  layers[i] == '"Convolution"':
                    last_layer = "Conv";
                    if Param_strings[len(Param_strings)-1] == "num_output":
                        #How many filters?
                       filter_amount = Param_values[len(Param_values)-1];
                    if Param_strings[len(Param_strings)-1] == "kernel_size":
                        kernel_size = Param_values[len(Param_values)-1];

                
                                                   
                                                   
       #     print x[idxs[i]+j]
    else:
        print x[idxs[i]]

        """     
memory = [];
for i in range(0,len(layers)):
    if x[idxs[i]] == "CONVOLUTION" or '"Convolution"':
        if i == 0:
            print "using input";
            print "input:" + str(dims);
            #1. How many filters will there be? 
            #   Depending on the number_of_outputs
         


        else:
            print "using precalculated output"


"""      
"""
    if "num_output" in buf:
        idx =  buf.find(":");
        num_outputs.append(buf[idx + 1:len(buf)-1])
        
    if "kernel_size" in buf:
        idx =  buf.find(":");
        kernel_size.append(buf[idx + 1:len(buf)-1])

    if "stride" in buf:
        idx =  buf.find(":");
        stride.append(buf[idx + 1:len(buf)-1])
"""
