from jax import numpy as jnp, random, jit
import time

from ngcsimlib.context import Context
from ngcsimlib.commands import Command
from ngcsimlib.compilers import compile_command, wrap_command
## import model-specific mechanisms
from ngclearn.components.other.varTrace import VarTrace
from ngclearn.components.synapses.hebbian.traceSTDPSynapse import TraceSTDPSynapse

## create seeding keys (JAX-style)
dkey = random.PRNGKey(231)
dkey, *subkeys = random.split(dkey, 2)

dt = 1. # ms # integration time constant
T_max = 100 ## number time steps to simulate

with Context("Model") as model:
    tr0 = VarTrace("tr0", n_units=1, tau_tr=8., a_delta=1.)
    tr1 = VarTrace("tr1", n_units=1, tau_tr=8., a_delta=1.)
    W = TraceSTDPSynapse("W1", shape=(1, 1), eta=0., Aplus=1., Aminus=0.8,
                         wInit=("uniform", 0.0, 0.3), key=subkeys[0])

    # wire only relevant compartments to synaptic cable W for demo purposes
    W.preTrace << tr0.trace
    #self.W1.preSpike << self.z0.outputs
    W.postTrace << tr1.trace
    #self.W1.postSpike << self.z1e.s

    reset_cmd, reset_args = model.compile_command_key(tr0, tr1, W, compile_key="reset")
    adv_tr_cmd, _ = model.compile_command_key(tr0, tr1, compile_key="advance_state", name="advance_traces")
    evolve_cmd, evolve_args = model.compile_command_key(W, compile_key="evolve") ## M-step

    model.add_command(wrap_command(jit(model.reset)), name="reset")
    model.add_command(wrap_command(jit(model.advance_traces)), name="advance_traces")
    model.add_command(wrap_command(jit(model.evolve)), name="evolve")

    @Context.dynamicCommand
    def clamp_synapse(pre_spk, post_spk):
        W.preSpike.set(pre_spk)
        W.postSpike.set(post_spk)

    @Context.dynamicCommand
    def clamp_traces(pre_spk, post_spk):
        tr0.inputs.set(pre_spk)
        tr1.inputs.set(post_spk)


t_values = []
dW_vals = []
## run traces for T_max
_pre_trig = jnp.zeros((1,1))
_post_trig = jnp.zeros((1,1))
ts = -int(T_max/2) * 1.
for i in range(T_max+1):
    pre_spk = jnp.zeros((1,1))
    post_spk = jnp.zeros((1,1))
    if i == int(T_max/2): ## switch to post-spike case
        pre_spk = jnp.ones((1,1))
        post_spk = jnp.zeros((1,1))
        _pre_trig = jnp.zeros((1,1))
        _post_trig = jnp.ones((1,1))
        ts = 0.
    elif i == 0: ## switch to pre-spike case
        pre_spk = jnp.zeros((1,1))
        post_spk = jnp.ones((1,1))
        _pre_trig = jnp.ones((1,1))
        _post_trig = jnp.zeros((1,1))
        ts = 0.
    model.clamp_traces(pre_spk, post_spk)
    model.advance_traces(dt * i, dt)

    ## get STDP update
    W.preSpike.set(_pre_trig)
    W.postSpike.set(_post_trig)
    W.preTrace.set(tr0.trace.value)
    W.postTrace.set(tr1.trace.value)
    model.evolve(dt * i, dt)
    dW = W.dWeights.value
    dW_vals.append(dW)
    if i >= int(T_max/2):
        t_values.append(ts)
        ts += dt
    else:
        t_values.append(ts)
        ts -= dt
dW_vals = jnp.squeeze(jnp.asarray(dW_vals))

import matplotlib #.pyplot as plt
matplotlib.use('Agg')
import matplotlib.pyplot as plt
cmap = plt.cm.jet

fig, ax = plt.subplots()

_tr0 = ax.plot(t_values, dW_vals, 'o', color='tab:red')

ax.set(xlabel='$t_{post} - t_{pre}$ (ms)', ylabel='Change in Synaptic Efficacy',
      title='trace-STDP over Time (ms)')
ax.grid()
fig.savefig("stdp_curve.jpg")
