from jax import numpy as jnp, random
from ngclearn.utils.viz.dim_reduce import extract_tsne_latents, plot_latents

dkey = random.PRNGKey(1234)

def gen_data(dkey, N):
    mu1 = jnp.asarray([[2.1, 3.2, 0.6, -4., -2.]])    
    cov1 = jnp.eye(5) * 0.78
    mu2 = jnp.asarray([[-1.8, 0.2, -0.1, 1.99, 1.56]])
    cov2 = jnp.eye(5) * 0.52
    mu3 = jnp.asarray([[0.3, -1.2, -0.56, -4., 3.6]])
    cov3 = jnp.eye(5) * 1.2

    dkey, *subkeys = random.split(dkey, 7)
    samp1 = random.multivariate_normal(subkeys[0], mu1, cov1, shape=(N,))
    samp2 = random.multivariate_normal(subkeys[0], mu2, cov2, shape=(N,))
    samp3 = random.multivariate_normal(subkeys[0], mu3, cov3, shape=(N,))
    X = jnp.concatenate((samp1, samp2, samp3), axis=0)
    y1 = jnp.ones((N, 3)) * jnp.asarray([[1., 0., 0.]])
    y2 = jnp.ones((N, 3)) * jnp.asarray([[0., 1., 0.]])
    y3 = jnp.ones((N, 3)) * jnp.asarray([[0., 0., 1.]])
    lab = jnp.concatenate((y1, y2, y3), axis=0) ## one-hot codes
    return X, lab

data, lab = gen_data(dkey, 400)

## visualize via the t-SNE algorithm
print("data.shape = ",data.shape)
codes = extract_tsne_latents(data)
print("code.shape = ",codes.shape)
plot_latents(codes, lab, plot_fname="codes.jpg")
