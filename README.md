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
