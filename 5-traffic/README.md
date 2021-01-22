Experimentation process: first used the same model as in the class "handwriting" example, used the exact same setup with convolution (32 filters, 3x3 kernal, relu activation), pooling(max pool, 2x2 size), flattening, hidden(128 units, relu activation, 50% dropout), and output layer(softmax activation). initial results was ~5% acuracy, next tried an additional set of convolution and pooling layer right after the initial set, the accuracy immeadiately improved to 95%. increasing the units in the hidden layer from 128 to 256 allowed model to achieve high accuracy faster, but did not improve on the final accuracy. The remaining trials were: double number of filters in convolution layer (small improvement, but longer run time, reverted), add an additional hidden layer (no improvement, reverted), decrease dropout to 30% (no improvement, reverted), increase pooling size to 3x3, (no improvement, reverted).

so in conclusion, the final setup for the model that achieved 95% accuracy is as per follows: 

(x2)Convolution layer: 32 filters, 3x3 kernal, relu activation
(x2)Pooling layer: max pool, 2x2 size
Hidden layer: 256 units, relu activation, 50% dropout
Output layer: softmax activation

Thank you,

DZ