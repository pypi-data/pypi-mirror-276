from jax import numpy as jnp
from ngclearn.utils.metric_utils import measure_ACC, measure_MSE, measure_CatNLL, measure_fanoFactor, measure_firingRate
from ngclearn.utils.model_utils import softmax

Y_scores = jnp.asarray([[5., -6., 12.],
                        [-11, 8., -2.],
                        [2., -1., 9.],
                        [15., 2.1, -32.],
                        [4., -11.2, -0.2]], dtype=jnp.float32)

Y_labels = jnp.asarray([[0., 0., 1.],
                        [0., 0., 1.],
                        [0., 1., 0.],
                        [1., 0., 0.],
                        [1., 0., 0.]], dtype=jnp.float32)

acc = measure_ACC(Y_scores, Y_labels)
mse = measure_MSE(Y_scores, Y_labels)
cnll = measure_CatNLL(softmax(Y_scores), Y_labels)

print(" > Accuracy = {:.3f}".format(acc))
print(" >      MSE = {:.3f}".format(mse))
print(" >  Cat-NLL = {:.3f}".format(cnll))
