from jax import numpy as jnp

#@jit
def calc_interspikeIntervals(spikes, dt):#, T):
    lenT = spikes.shape[0]
    time_span = jnp.expand_dims(jnp.arange(0., spikes.shape[0] * dt, dt), 1) # absolute times
    times = spikes * time_span
    ISI = [] # interspike intervals
    ignore_jm1 = jnp.zeros((1,spikes.shape[1]), dtype=jnp.float32)
    time_jm1 = times[0:1,:]
    for j in range(1, lenT):
        time_j = times[j:j+1,:]
        mask = (time_j > 0.).astype(jnp.float32)
        isi_j = (time_j - time_jm1) * mask * ignore_jm1
        time_jm1 = time_j * mask + time_jm1 * (1. - mask)
        ISI.append(isi_j)
        jmask = (time_jm1 > 0.).astype(jnp.float32)
        ignore_jm1 = ((jmask + ignore_jm1) > 0.).astype(jnp.float32)
    ISI = jnp.concatenate(ISI, axis=0)
    return ISI

spikes = jnp.asarray([[0., 0., 0.],
                      [0., 0., 0.],
                      [1., 0., 0.],
                      [0., 0., 1.],
                      [0., 1., 0.],
                      [1., 0., 1.],
                      [0., 0., 0.],

                      [0., 1., 0.],
                      [1., 0., 1.]])
print(spikes)
print("...")
print(calc_interspikeIntervals(spikes, dt=0.1))
