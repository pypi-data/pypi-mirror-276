from jax import numpy as jnp
from ngclearn.utils.metric_utils import measure_fanoFactor, measure_firingRate

spikes = jnp.asarray([[0., 0., 0.],
                      [0., 0., 1.],
                      [0., 1., 0.],
                      [1., 0., 1.],
                      [0., 0., 0.],
                      [0., 0., 1.],
                      [1., 0., 0.],
                      [0., 0., 1.],
                      [0., 1., 0.],
                      [0., 0., 1.],
                      [0., 0., 0.],
                      [0., 0., 0.],
                      [0., 1., 0.],
                      [0., 0., 1.],
                      [0., 0., 0.],
                      [0., 0., 1.],
                      [0., 1., 0.],
                      [0., 0., 1.]], dtype=jnp.float32)

fr = measure_firingRate(spikes, preserve_batch=True)
fano = measure_fanoFactor(spikes, preserve_batch=True)

print(" > Firing Rates = {}".format(fr))
print(" > Fano Factor  = {}".format(fano))
