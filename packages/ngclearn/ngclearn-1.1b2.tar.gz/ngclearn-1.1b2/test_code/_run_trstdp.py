from jax import numpy as jnp, random, jit
import time

from ngcsimlib.context import Context
from ngcsimlib.commands import Command
from ngcsimlib.compilers import compile_command, wrap_command
from ngclearn.utils.viz.raster import create_raster_plot
## import model-specific mechanisms
from ngcsimlib.operations import summation
from ngclearn.components.input_encoders.poissonCell import PoissonCell
from ngclearn.components.other.varTrace import VarTrace
from ngclearn.components.synapses.hebbian.traceSTDPSynapse import TraceSTDPSynapse

## create seeding keys (JAX-style)
dkey = random.PRNGKey(231)
dkey, *subkeys = random.split(dkey, 2)

dt = 1. # ms # integration time constant
T_max = 200 ## number time steps to simulate
Aplus = 1. #0.0055
Aminus = 1. #0.00055
with Context("Model") as model:
    tr0 = VarTrace("tr0", n_units=1, tau_tr=10., a_delta=1.) # 0.
    tr1 = VarTrace("tr1", n_units=1, tau_tr=10., a_delta=1.) # 0.
    W = TraceSTDPSynapse("W1", shape=(1, 1), eta=1.,
                          Aplus=Aplus, Aminus=Aminus, wInit=("uniform", 0.0, 0.3),
                          preTrace_target=0., key=subkeys[0])

    # wire relevant compartment statistics to synaptic cable W1
    W.preTrace << tr0.trace
    #self.W1.preSpike << self.z0.outputs
    W.postTrace << tr1.trace
    #self.W1.postSpike << self.z1e.s

    reset_cmd, reset_args = model.compile_command_key(tr0, tr1, W, compile_key="reset")
    adv_tr_cmd, _ = model.compile_command_key(tr0, tr1, compile_key="advance_state", name="advance_traces")
    adv_stdp_cmd, _ = model.compile_command_key(W, compile_key="advance_state", name="advance_stdp")

    model.add_command(wrap_command(jit(model.reset)), name="reset")
    model.add_command(wrap_command(jit(model.advance_traces)), name="advance_traces")
    model.add_command(wrap_command(jit(model.advance_stdp)), name="advance_stdp")

    @Context.dynamicCommand
    def clamp_synapse(pre_spk, post_spk):
        W.preSpike.set(pre_spk)
        W.postSpike.set(post_spk)

    @Context.dynamicCommand
    def clamp_traces(spk):
        tr0.inputs.set(spk)
        tr1.inputs.set(spk)


t_values = []
trace_0 = []
trace_1 = []
## run traces for T_max
for i in range(T_max):
    if i == 0:
        model.clamp_traces(jnp.ones((1,1)))
    else:
        model.clamp_traces(jnp.zeros((1,1)))
    model.advance_traces(dt * i, dt)
    t_values.append(dt * i)
    trace_0.append( tr0.trace.value)
    trace_1.append( tr1.trace.value)
trace_0 = jnp.squeeze(jnp.asarray(trace_0))
trace_1 = jnp.squeeze(jnp.asarray(trace_1))

import matplotlib #.pyplot as plt
matplotlib.use('Agg')
import matplotlib.pyplot as plt
cmap = plt.cm.jet

fig, ax = plt.subplots()

_tr0 = ax.plot(t_values, trace_0, '-.', color='C0')
_tr1 = ax.plot(t_values, trace_1, color='C1') #, alpha=.5)

ax.set(xlabel='time (ms)', ylabel='Dynamics Output',
      title='Integration of:  dz/dt = $-\gamma z + x$')
ax.legend([_tr0[0],_tr1[0]],['tr(0)','tr(1)'])
ax.grid()
fig.savefig("stdp_traces.jpg")
