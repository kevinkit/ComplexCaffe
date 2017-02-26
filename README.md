# ComplexCaffe
Calculates the complexity of a caffe network

## Usage

Simply clone the directory. Make sure that Caffe is linked. Network must be specified in a .prototxt. Mean-Files will be ignored. Prototxt can either be in deploy or in train / vailidiation format. If there is no input dimension defined, the program will ask you to give the dimensions like: Channel Height Width. 

The Batch size is ignored.


The program can be startet like this:

    python Compelixity.py architecture.prototxt


## Supported Layers

* Input
* Convolution
* SoftmaxWithLoss
* LRN
* Concat
* ReLU
* Scale
* BatchNorm
* Pooling 
* InnerProduct
* Eltwise


## Testing

This program worked with GoogLeNEt, ResNet, AlexNet. Note that all prototxt files must be converted to the new standard format of cafffe. A python tool for this is available under [Converter] (https://github.com/kevinkit/ColdCoffeToHotCoffe). However there is also a c++ program implemented in caffe for this task.


## What's happening?

The program loads the prototxt and continues to search trough to the layers. Once a layer is found it will try to find it inputs. And then calculate the following three values:

* Nedded complexity
* Needed memory for weights
* Needed memory for feature maps

Note that these values are relying on the underlying implementation of the used framework. This is ignored in this program, and only gives a simplified result. Thus the result could be used for any framework, not only for Caffe as long as the network is describend in a .prototxt in the Caffe-layout. 


## Errors

The program will not work if...:

* Caffe is not found
* Python is not installed
* The network structure is wrong, e.g. an undefined input is used
* The architecture is described like in the old caffe version











