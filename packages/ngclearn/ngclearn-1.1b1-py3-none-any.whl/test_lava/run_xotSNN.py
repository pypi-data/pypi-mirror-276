from jax import numpy as jnp, random, jit
import time

from ngcsimlib.context import Context
from ngcsimlib.commands import Command
from ngcsimlib.compilers import compile_command, wrap_command
from ngclearn.utils.viz.raster import create_raster_plot
from ngclearn.utils.viz.synapse_plot import visualize
from ngclearn.utils.io_utils import makedir
## import model-specific mechanisms
from ngcsimlib.operations import summation
## import Lava-specific components
from ngclearn.components.lava.neurons.LIFCell import LIFCell
#from ngclearn.components.lava.synapses.hebbianSynapse import HebbianSynapse
from ngclearn.components.lava.synapses.staticSynapse import StaticSynapse
from ngclearn.components.lava.synapses.traceSTDPSynapse import TraceSTDPSynapse
from ngclearn.components.lava.traces.gatedTrace import GatedTrace

def get_synapse_stats(W):
    """
    Print basic statistics of component W to string

    Returns:
        string containing min, max, mean, and L2 norm of W1
    """
    _W = W.weights.value
    msg = "W1:\n  min {} ;  max {} \n  mu {} ;  norm {}".format(jnp.amin(_W),
                                                                jnp.amax(_W),
                                                                jnp.mean(_W),
                                                                jnp.linalg.norm(_W))
    return msg


_X = jnp.load("xot/trainX.npy")
_Y = jnp.load("xot/trainY.npy")
n_batches = _X.shape[0]
mb_size = 1
n_in = _X.shape[1]

## create seeding keys (JAX-style)
dkey = random.PRNGKey(231)
dkey, *subkeys = random.split(dkey, 10)

exp_dir = "exp"
makedir(exp_dir)
makedir("{}/filters".format(exp_dir))
makedir("{}/raster".format(exp_dir))

n_hid = 25 # 64 #100
dt = 1. # ms # integration time constant
T = 200 ## number time steps to simulate
n_iter = 20

thr0 = jnp.zeros((1, n_in))
thr1e = random.uniform(subkeys[1], (1, n_hid), minval=-2., maxval=2.)
thr1i = random.uniform(subkeys[2], (1, n_hid), minval=-2., maxval=2)
_W1 = random.uniform(subkeys[3], (n_in, n_hid), minval=0., maxval=0.3)
_W1ie = (1. - jnp.eye(n_hid)) * 120.
_W1ei = jnp.eye(n_hid) * 22.5

with Context("Model") as model:
    ## set up cells
    z0 = LIFCell("z0", n_units=n_in, thr_theta0=thr0, dt=dt, tau_m=50., R_m=1.,
                 thr=-52., v_rest=-65., v_reset=-60., v_decay=0., tau_theta=500.,
                 theta_plus=0.05, refract_T=0.) ## IF cell
    z1e = LIFCell("z1e", n_units=n_hid, thr_theta0=thr1e, dt=dt, tau_m=100.,
                  R_m=1., thr=-52., v_rest=-65., v_reset=-60., tau_theta=500.,
                  theta_plus=0.05, refract_T=5.) ## LIF cell
    z1i = LIFCell("z1i", n_units=n_hid, thr_theta0=thr1i, dt=dt, tau_m=100.,
                  R_m=1., thr=-40., v_rest=-60., v_reset=-45., tau_theta=1e7,
                  theta_plus=0., refract_T=5.) ## LIF cell
    tr0 = GatedTrace("tr0", n_units=n_in, dt=dt, tau_tr=20., key=subkeys[6])
    tr1 = GatedTrace("tr1", n_units=n_hid, dt=dt, tau_tr=20., key=subkeys[7])
    ## set up synapses
    W1 = TraceSTDPSynapse("W1", weights=_W1, dt=dt, Rscale=1., Aplus=0.0055,
                          Aminus=0.00055, preTrace_target=0.055, w_decay=0.,
                          w_bound=1.)
    W1ie = StaticSynapse("W1ie", weights=_W1ie, dt=dt, Rscale=1.)
    W1ei = StaticSynapse("W1ei", weights=_W1ei, dt=dt, Rscale=1.)

    ## wire z0 to z1e via W1 and z1i to z1e via W1ie
    W1.inputs << z0.s
    W1ie.inputs << z1i.s
    #z1e.j << summation(W1.outputs, W1ie.outputs)
    z1e.j_exc << W1.outputs
    z1e.j_inh << W1ie.outputs
    # wire z1e to z1i via W1ie
    W1ei.inputs << z1e.s
    z1i.j_exc << W1ei.outputs
    # wire cells z0 and z1e to their respective traces
    tr0.inputs << z0.s
    tr1.inputs << z1e.s
    # wire relevant compartment statistics to synaptic cable W1 (for STDP update)
    W1.x_pre << tr0.trace
    W1.pre << z0.s
    W1.x_post << tr1.trace
    W1.post << z1e.s

    reset_cmd, reset_args = model.compile_command_key(
                                    z0, z1e, z1i,
                                    tr0, tr1,
                                    W1, W1ie, W1ei,
                                compile_key="reset")
    advance_cmd, advance_args = model.compile_command_key(
                                        W1, W1ie, W1ei,
                                        z0, z1e, z1i,
                                        tr0, tr1,
                                    compile_key="advance_state")
    #print(advance_args)
    #evolve_cmd, evolve_args = model.compile_command_key(W1, compile_key="evolve")

    model.add_command(wrap_command(jit(model.reset)), name="reset")
    model.add_command(wrap_command(jit(model.advance_state)), name="advance")
    #model.add_command(wrap_command(jit(model.evolve)), name="evolve")

    @Context.dynamicCommand
    def clamp(x):
        z0.j_exc.set(x)

    @Context.dynamicCommand
    def clamp_eta(eta):
        W1.eta.set(eta)

################################################################################

model.save_to_disk()
print(get_synapse_stats(W1))

for i in range(n_iter):
    dkey, *subkeys = random.split(dkey, 2)
    ptrs = random.permutation(subkeys[0],_X.shape[0])
    X = _X[ptrs,:]

    tstart = time.time()
    n_samps_seen = 0
    #### start of training pass
    for j in range(n_batches):
        idx = j
        Xb = X[idx: idx + mb_size,:]

        t = 0.
        model.reset()
        cnt0 = 0.
        cnt1 = 0.
        for ts in range(T):
            x_t = Xb
            model.clamp(x_t)
            model.advance()
            #model.evolve()

            cnt0 = z0.s.value + cnt0
            cnt1 = z1e.s.value + cnt1
            t = t + dt

        n_samps_seen += Xb.shape[0]
        print("\r Seen {} images...".format(n_samps_seen), end="")
    #### end of training pass
    tend = time.time()
    print()
    print(" -> Time = {} s".format(tend - tstart))
    tstart = tend + 0.
    print(get_synapse_stats(W1))
    _W1 = W1.weights.value
    visualize([_W1], [(8,8)], "exp/filters/W1_fields")
    model.save_to_disk(params_only=True) # save final state of synapses to disk
print()

## generate a test-time raster plot
Xb = _X[None, 0, :] # get 1st data point
t = 0.
model.reset()
_S = []
model.clamp(0.) ## disable STDP-learning
for ts in range(T):
    x_t = Xb
    model.clamp(x_t)
    model.advance()
    t = t + dt
    _S.append(z1e.s.value)
_S = jnp.concatenate(_S, axis=0)
create_raster_plot(_S, tag="{}".format(0),
                   plot_fname="{}/raster/z1e_raster.jpg".format(exp_dir))
