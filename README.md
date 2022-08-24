# INITIAL MODEL
Structure: 1 convulation layer, 1 maxpooling layer, Conv2D using 32 filters and 3x3 kernel, 1 hidden layer with 400 units using ReLU activation with 0.5 dropout, output layer using softmax activation

I started with a model similar to the one showed in the lecture, only changing the input shape and the output shape to reflect the specification of this problem. I left the global variables as they were. That way the training accuracy was 0.0569 and testing accuracy was 0.0554. However, in training, the model seemed not to improve with each epoch.

# MODEL VERSION 2
Structure: 2 convulation layers, 2 maxpooling layers, Conv2D using 32 filters and 3x3 kernel, 1 hidden layer with 400 units using ReLU activation with 0.5 dropout, output layer using softmax activation

Improvement number one was adding a second convulation layer and a second max-pooling layer both identical to the first ones. This time the model seemed to improve with each epoch. Final training accuracy was 0.7074 and testing accuracy was 0.8487. This is a great improvement over the initial model.

# MODEL VERSION 3
Structure: 3 convulation layers, 3 maxpooling layers, Conv2D using 32 filters and 3x3 kernel, 1 hidden layer with 400 units using ReLU activation with 0.5 dropout, output layer using softmax activation

As adding layers seemed to work, next improvement was to add a third convulation layer with a third maxpooling layer. This model improved with each epoch. Final training accuracy was 0.8940 and testing accuracy was 0.9336 which is an improvement over the 2-layer model.

# MODEL VERSION 4
Structure: 3 convulation layers, 3 maxpooling layers, Conv2D using 100 filters and 3x3 kernel, 1 hidden layer with 400 units using ReLU activation with 0.5 dropout, output layer using softmax activation

Next I tried increasing the number of filters that convulation layers were using. I increased the number of filters from 32 to 100. This resulted in training accuracy of 0.9543 and testing accuracy of 0.9764. The model also improved well with each epoch, more at the beginning, less in the end as expected. Therefore, 100 filters gave better results than 32 filters.

# MODEL VERSION 5
Structure: 3 convulation layers, 3 maxpooling layers, Conv2D using 200 filters and 3x3 kernel, 1 hidden layer with 400 units using ReLU activation with 0.5 dropout, output layer using softmax activation

As adding of filters seemed to improve the accuracy last time, I doubled the number of filters (100 to 200). Final training accuracy was 0.0564 and training accuracy was 0.0562. Seems like this move was a mistake. The model was not improving with each epoch, underfitting the data. Additionally, doubling of the number of filters made training process of the model significantly slower. Therefore, I concluded that 100 filters was a better choice.

# MODEL VERSION 6
Structure: 3 convulation layers, 3 maxpooling layers, Conv2D using 100 filters and 3x3 kernel, 2 hidden layers with 400 units both using ReLU activation with 0.5 dropout, output layer using softmax activation

I tried adding a second hidden layer with 0.5 dropout. However, this hindered the model's performance significantly. The training accuracy was 0.0594 and the testing accuracy was 0.0540. It seemed the model was not learning which each epoch and underfitting.

# MODEL VERSION 7
Structure: 3 convulation layers, 3 maxpooling layers, Conv2D using 100 filters and 3x3 kernel, 2 hidden layers with 400 units both using ReLU activation with 0.2 dropout, output layer using softmax activation

I tried lowering the dropout rate of the 2 hidden layers from 0.5 to 0.2. This resulted in training accuracy of 0.9633 and testing accuracy of 0.9748. As testing accuracy is similar to training accuracy, the model is not overfit, thus with 2 hidden layers dropout rate of 0.2 is suitable. This model is about as good as model version 3 that had 1 hidden layer with 0.5 dropout. The gain in training accuracy is +0.009, testing accuracy is a bit worse (-0.0016). Therefore, adding an additional hidden layer and lowering the drop-out rates did not give a significant improvement.

# MODEL VERSION 8
Structure: 3 convulation layers, 3 maxpooling layers, Conv2D using 100 filters and 3x3 kernel, 3 hidden layers with 400 units both using ReLU activation with 0.2 dropout, output layer using softmax activation

As a step further I tried adding a third hidden layer, also with 0.2 dropout rate. This model's training accuracy was 0.9640 and testing accuracy was 0.9825, the best yet, although not by much.

# MODEL VERSION 9
Structure: 3 convulation layers, 3 maxpooling layers, Conv2D using 100 filters and 3x3 kernel, 3 hidden layers with 400 units both using ReLU activation with 0.15 dropout, output layer using softmax activation

Lowering the 3 hidden layers' dropout rate from 0.2 to 0.15 resulted in a slightly worse performance. The model's training accuracy was 0.9628 and testing accuracy was 0.9774.

# SUMMARY
The best model was model version 8: with training accuracy of 0.9640 and testing accuracy of 0.9825. It has 3 convulation layers, 3 maxpooling layers, Conv2D using 100 filters and 3x3 kernel, 3 hidden layers with 400 units both using ReLU activation with 0.2 dropout, output layer using softmax activation.

Experimentation showed that 100 Conv2D filters were better than 32 but 200 was too much, the model was not able to learn. Similar thing happened with increasing the kernel size: the model was not improving with epochs. However, incresing the number of conculation layers with maxpooling layers, as well as adding hidden layers and decreasing the dropout rate, helped to increase the model's performance.

Note that all the model versions, including the final one, convulation layers and maxpooling layers were use one after the other (so conv layer, maxpooling layer, conv layer, maxpooling layer etc).