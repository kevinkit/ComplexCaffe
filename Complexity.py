#!/usr/bin/env python
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from google.protobuf import text_format
import matplotlib.pyplot as plt
import caffe
from caffe.proto import caffe_pb2
import math as m


def get_pydot_graph(caffe_net, rankdir, label_edges=True, phase=None):
    dimensions = []
    weights = [];
    O = [];
    dim_cnt = -1
#   layer_cnt = 0;
    conv_cnt = 0;
    fc_cnt = 0;
    pool_cnt = 0;
    
    for layer in caffe_net.layer:
        if phase is not None:
          included = False
          if len(layer.include) == 0:
            included = True
          if len(layer.include) > 0 and len(layer.exclude) > 0:
           raise ValueError('layer ' + layer.name + ' has both include '
                             'and exclude specified.')
          for layer_phase in layer.include:
            included = included or layer_phase.phase == phase
          for layer_phase in layer.exclude:
           included = included and not layer_phase.phase == phase
          if not included:
            continue
	if str(layer.type) == "Input":
		print "data";
		dim_ = [1,2,3,4];
		dims = str(layer.input_param.shape).splitlines()
		cnt = 0;
		for i in range(0,len(dims)):
			#print dims[i]
			if "dim:" in dims[i]:
				
				dd = dims[i].find(":")
				buf = dims[i];
				dim_[cnt] = int(buf[dd + 1:len(buf)]);
				cnt = cnt +1;
#		print "before"
#		print dimensions
		dimensions.append([dim_,"input"])
#		print "after:"
#		print dimensions
		dim_cnt = dim_cnt +1;
	elif dim_cnt == -1:
		print "not found"
		cnt = 0;
		dim_ = [1,2,3,4];
		buf = str(caffe_net.input_shape).splitlines()
		input_buf = caffe_net.input_dim
		if len(input_buf) != 0:
			dimensions.append([caffe_net.input_dim,"input"])
			dim_cnt = dim_cnt +1;	
		else:
			for i in range(0,len(buf)):
				if "dim:" in buf[i] or "input_dim:" in buf[i]:
					dd = buf[i].find(":");
					buf2 = buf[i];
					print buf2[dd + 1:len(buf2)]
					dim_[cnt] = int(buf2[dd +1:len(buf2)])
					cnt = cnt +1;
			if cnt != 0:
				dimensions.append([dim_,"input"])
				dim_cnt = dim_cnt +1;
			else:
				var = raw_input("No dimensions specified please enter the used image sizes, as following: Dimensions Width height\n");
				dim_ = var.split()
				if len(dim_) == 3:
					dim_buf = [1,2,3,4];
					for i in range(0,len(dim_)):
						dim_buf[i+1] = int(dim_[i]);
					dimensions.append([dim_buf,"input"]);
					dim_cnt = dim_cnt +1;
					
				else:
					print "not enough specified"
        #Calculating dimensions
        if layer.type == 'Convolution':
	        conv_cnt = conv_cnt +1;	

		if dim_cnt == -1:
			print "INPUT SIZE NOT DEFINED!"
			return -1;
		
		P = 1;
		S = 1;
		K = int(layer.convolution_param.num_output);
		F = int(layer.convolution_param.kernel_size[0]);

		try:
			S = int(layer.convolution_param.stride[0]);
		except IndexError:
			try:
				S = int(layer.convolution_param.stride)
			except TypeError:
				S = 1


		try:
                	P = int(layer.convolution_param.pad[0]);
		except IndexError:
			try:
				P = int(layer.convolution_param.pad)
			except TypeError:
				P = 0
	#	print layer.bottom
	#	print dimensions[dim_cnt][1]

		found = False
		if dim_cnt == 0:
			dim_buf = dimensions[0][0];
			found = True
		else:
			found = False
			for i in range(0,dim_cnt +1):
				
	#		print "searching for: " + str(layer.bottom[0]) 
	#			print "but got:       " + str(dimensions[dim_cnt -i][1]);
	#			print layer.bottom
				if str(layer.bottom[0]) == dimensions[dim_cnt - i][1]:
					dim_buf = dimensions[dim_cnt -1][0]
					print '\033[93m' + "found match" + '\033[0m'
					found = True
					break;
				else:
					print '\033[91m' + "still looking" + '\033[0m'
			if not found:
                        	print '\033[95m' + "no match!!!" + "\033[0m"
                        	print "dims are:" + str(dim_cnt)




		if found:
			weight_buf = [1,2,3];
			weight_buf[0] = K;
			weight_buf[1] = F;
			weight_buf[2] = F;
			weights.append(weight_buf);

			W = 1 + ((dim_buf[2] - F + 2*P)/S)
			H = 1 + ((dim_buf[3] - F + 2*P)/S);
			D = K
			
			#print str(K) + "x" + str(F) + "x" + str(F) + " P: " + str(P) + " S: " + str(S) 	

			O_buf = K*((dim_buf[1]*(dim_buf[2]+P)*dim_buf[3]+P)*F*F)/S
			O.append(O_buf);
			n_dim_buf = [1,2,3,4]
			n_dim_buf[1] = D;
			n_dim_buf[2] = W;
			n_dim_buf[3] = H;
			dim_cnt = dim_cnt +1;
			dimensions.append([n_dim_buf,layer.name]);
	if layer.type == "SoftmaxWithLoss":
		O_buf = max(dim_buf[1],dim_buf[2],dim_buf[3])
		O.append(O_buf)

	if layer.type == "lrn" or layer.type == "LRN":
		local_size = int(layer.lrn_param.local_size)
		dim_buf = dimensions[dim_cnt][0];
		O_buf = local_size*dim_buf[1]*dim_buf[2]*dim_buf[3];
 		O.append(O_buf);
		dimensions.append([dimensions[dim_cnt][0],layer.name])
		dim_cnt = dim_cnt +1
	if layer.type == "Concat":
		bottom_buf = layer.bottom
		dim_buf = dimensions[dim_cnt][0]

                found = False

		for i in range(0,len(bottom_buf)):
			bottom_buf1 = bottom_buf[i];
                        for i in range(0,dim_cnt+2):
                               	if str(bottom_buf1) == dimensions[dim_cnt - i][1]:
                    	          	dim_buf = dimensions[dim_cnt -1][0]
                                       	print '\033[93m' + "found match" + '\033[0m'
                                       	found = True
					break;
                               	else:
                        		print dimensions[dim_cnt -i][1]      
			         	print '\033[91m' + "still looking" + '\033[0m'

			if not found:
				print '\033[95m' + "no match!!!" + "\033[0m"

		if not found:
			print '\033[95m' + "no match!!!" + "\033[0m"
			print "dims are:" + str(dim_cnt)

	
		dimensions.append([dimensions[dim_cnt][0],layer.name]);
		dim_cnt = dim_cnt +1;
		
	if layer.type == 'ReLU':
		if len(str(layer.relu_param)) == 0:
			O_buf = 1;
		else:
			O_buf = dim_buf[1] * dim_buf[2] * dim_buf[3]
			O.append(O_buf);
		dimensions.append([dimensions[dim_cnt][0],layer.name])
		dim_cnt = dim_cnt +1
	if layer.type == 'Scale':
		O_buf = dim_buf[1] + dim_buf[2] + dim_buf[3]
		O.append(O_buf);
                bottom_buf = layer.bottom[0]
                dim_buf = dimensions[dim_cnt][0]

                found = False

                for i in range(0,dim_cnt):
                        if str(bottom_buf1) == dimensions[dim_cnt - i][1]:
        	                dim_buf = dimensions[dim_cnt -1][0]
                                print '\033[93m' + "found match" + '\033[0m'
                                found = True
                                break;
                        else:
                                print dimensions[dim_cnt -i][1]
                                print '\033[91m' + "still looking" + '\033[0m'


                if not found:
                        print '\033[95m' + "no match!!!" + "\033[0m"
                        print "dims are:" + str(dim_cnt)

		dimensions.append([dim_buf],layer.name)


	if layer.type == 'BatchNorm':
		dimensions.append([dimensions[dim_cnt][0],layer.name])
		dim_cnt = dim_cnt +1
	if layer.type == 'Pooling':
		pool_cnt = pool_cnt +1;
		dim_buf = dimensions[dim_cnt][0];
		if bool(layer.pooling_param.global_pooling):
			print layer.pooling_param.pool
			#I do not know
			O_buf = m.square(dim_buf[1]*dim_buf[2]*dim_buf[3])
		else:
			S = 1;	
			F = int(layer.pooling_param.kernel_size);
	                S = int(layer.pooling_param.stride);
			W = 1 + ((dim_buf[2] - F)/S)
			H = 1 + ((dim_buf[3] - F)/S)
	                found = False
                found = False
		if dim_cnt == 0:
			dim_buf = dimensions[0][0]
			found = True;
		for i in range(0,dim_cnt+1):
                        print layer.bottom
                        if str(layer.bottom[0]) == dimensions[dim_cnt - i][1]:
                        	dim_buf = dimensions[dim_cnt -1][0]
                                print '\033[93m' + "found match" + '\033[0m'
                                found = True
                                break;
                        else:
                                print '\033[91m' + "still looking" + '\033[0m'

                if not found:
                        print '\033[95m' + "no match!!!" + "\033[0m"
                        print "dims are:" + str(dim_cnt)


		#print str(W) + "=" + "1 +" + "((" + str(dim_buf[2]) + " - " + str(F) + ")/" + str(S) + ")";
		#print str(W) + "=" + "1 +" + "((" + str(dim_buf[3]) + " - " + str(F) + ")/" + str(S) + ")";

	
		ty =  layer.pooling_param.pool

		if ty == 0:
			O_buf = K*((dim_buf[1]*(dim_buf[2])*dim_buf[3]))/S
		elif ty == 1:
			O_buf =  K*((dim_buf[1]*(dim_buf[2])*dim_buf[3])*F*F)/S
		elif ty == 2:	
			O_buf =  K*((dim_buf[1]*(dim_buf[2])*dim_buf[3])*F*F)/S

		dim_buf[2] = W;
		dim_buf[3] = H;
		dimensions.append([dim_buf,layer.name]) 
		dim_cnt = dim_cnt +1;
		O.append(O_buf)
	if layer.type == 'InnerProduct':
		fc_cnt = fc_cnt +1;
		O_buf = dim_buf[1]*dim_buf[2]*dim_buf[3]*int(layer.inner_product_param.num_output)
		weight_buf = [1,2,3];
		weight_buf[0] = O_buf;
		weight_buf[1] = 1;
		weight_buf[2] = 1;
		weights.append(weight_buf)
		dim_buf = [1,int(layer.inner_product_param.num_output),1,1]
		dimensions.append([dim_buf,layer.name]);
		dim_cnt = dim_cnt +1;
		O.append(O_buf)

 #       if dim_cnt != -1:
#		print dimensions[dim_cnt][0]
#		print dim_cnt

#                       label=edge['label']))
    plt.figure(0)
    plt.plot(O);
    plt.savefig("complex.png")
    memory_dim = [];
    memory_w = [];
#    print "dimensions:"
    for i in range(0,len(dimensions)):
	memo_buf = dimensions[i][0]
	print dimensions[i]
#	print memo_buf
    	memory_dim.append(memo_buf[1]*memo_buf[2]*memo_buf[3])

#    print "Complexities:"
#    for i in range(0,len(O)):
#	print O[i];

#    print "Memore in weights"
    for i in range(0,len(weights)):
	memory_buf = weights[i]
#	print memory_buf
	memory_w.append(memory_buf[0]*memory_buf[1]*memory_buf[2])

    print "O: " + str(sum(O)/1000000000.)
    print "M(f): " + str(sum(memory_dim)/1000000000.)
    print "M(W): "+ str(sum(memory_w)/1000000000.)
    print "Conv-Layers: " + str(conv_cnt) + " Pooling-Layers: " + str(pool_cnt) +  " Fully-Connected: " + str(fc_cnt)

    plt.figure(1)
    plt.plot(memory_dim)

    plt.savefig("dims.png");
    return found

def parse_args():
    """Parse input arguments
    """

    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('input_net_proto_file',
                        help='Input network prototxt file')
    parser.add_argument('--rankdir',
                        help=('One of TB (top-bottom, i.e., vertical), '
                              'RL (right-left, i.e., horizontal), or another '
                              'valid dot option; see '
                              'http://www.graphviz.org/doc/info/'
                              'attrs.html#k:rankdir'),
                        default='LR')
    parser.add_argument('--phase',
                        help=('Which network phase to calculate: can be TRAIN, '
                              'TEST, or ALL.  If ALL, then all layers are calculated '
                              'regardless of phase. This option is not implemented at the moment'),
                        default="ALL")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    net = caffe_pb2.NetParameter()
    text_format.Merge(open(args.input_net_proto_file).read(), net)
 #   print('Drawing net to %s' % args.output_image_file)
    phase=None;
    if args.phase == "TRAIN":
        phase = caffe.TRAIN
    elif args.phase == "TEST":
        phase = caffe.TEST
    elif args.phase != "ALL":
        raise ValueError("Unknown phase: " + args.phase)
    if not get_pydot_graph(net, args.rankdir, phase):
	print "fatal error!"
    else:
	print "Calculation varified"
if __name__ == '__main__':
    main()

