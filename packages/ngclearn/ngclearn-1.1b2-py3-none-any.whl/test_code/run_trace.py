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

## create seeding keys (JAX-style)
dkey = random.PRNGKey(231)
dkey, *subkeys = random.split(dkey, 2)

dt = 1. # ms # integration time constant
T = 200 ## number time steps to simulate

with Context("Model") as model:
    cell = PoissonCell("z0", n_units=1, max_freq=63.75, key=subkeys[0])
    trace = VarTrace("tr0", n_units=1, tau_tr=30., a_delta=0.5) # 0.

    ## wire up cell z0 to trace tr0
    trace.inputs << cell.outputs

    reset_cmd, reset_args = model.compile_command_key(cell, trace, compile_key="reset")
    advance_cmd, advance_args = model.compile_command_key(cell, trace, compile_key="advance_state")

    model.add_command(wrap_command(jit(model.reset)), name="reset")
    model.add_command(wrap_command(jit(model.advance_state)), name="advance")

    @Context.dynamicCommand
    def clamp(x):
        cell.inputs.set(x)

probs = jnp.asarray([[0.35]],dtype=jnp.float32)
time_span = []
spikes = []
traceVals = []
model.reset()
for ts in range(T):
    model.clamp(probs)
    model.advance(ts*1., dt)

    print("{}  {}".format(cell.outputs.value, trace.trace.value))
    spikes.append( cell.outputs.value )
    traceVals.append( trace.trace.value )
    time_span.append(ts * dt)
spikes = jnp.concatenate(spikes,axis=0)
traceVals = jnp.concatenate(traceVals,axis=0)


import matplotlib #.pyplot as plt
matplotlib.use('Agg')
import matplotlib.pyplot as plt
cmap = plt.cm.jet

fig, ax = plt.subplots()

zTr = ax.plot(time_span, traceVals, '-.', color='tab:red')
# spk = ax.plot(time_span, spikes, color='C1') #, alpha=.5)
# ax[1].plot(mem, c="tab:red")
stat = jnp.where(spikes > 0.)
indx = (stat[0] * 1. - 1.).tolist()
spk = ax.vlines(x=indx, ymin=0.985, ymax=1.05, colors='black', ls='-', lw=5)

ax.set(xlabel='Time (ms)', ylabel='Trace Output',
      title='Variable Trace of Poisson Spikes')
#ax.legend([zTr[0],spk[0]],['z','phi(z)'])
ax.grid()
fig.savefig("poisson_trace.jpg")
