from ngcsimlib.controller import Controller
from jax import numpy as jnp, random, nn, jit
import numpy as np

import matplotlib #.pyplot as plt
matplotlib.use('Agg')
import matplotlib.pyplot as plt
cmap = plt.cm.jet
import matplotlib.patches as mpatches #used to write custom legends

## create seeding keys (JAX-style)
dkey = random.PRNGKey(1234)
dkey, *subkeys = random.split(dkey, 6)

T = 20000 ## number of simulation steps to run
dt = 0.01 # ms ## compute integration time constant

## Izh cell hyperparameters
v0 = -65. ## initial membrane potential (for reset condition)
w0 = -14. ## initial recovery value (for reset condition)

## regular-spiking cells
cell_tag = "RS"
tau_w = 50.
v_reset = -65.
w_reset = 8.
coupling_factor=0.2

## fast-spiking cells
#cell_tag = "FS"
#tau_w = 10.
#v_reset = -65.
#w_reset = 8.
#coupling_factor=0.2

## Chattering neurons: ``v_reset = -50, w_reset=2``
#cell_tag = "CH"
#tau_w = 50.
#v_reset = -50.
#w_reset = 2.
#coupling_factor=0.2

# Intrinsically bursting neurons: ``v_reset=-55, w_reset = 4``
#cell_tag = "IB"
#tau_w = 50.
#v_reset = -55.
#w_reset = 4.
#coupling_factor=0.2

## Low-threshold spiking neurons: ``coupling_factor = 0.25, w_reset = 2``
# cell_tag = "LTS"
# tau_w = 50.
# v_reset = -65.
# w_reset = 2.
# coupling_factor = 0.25

## Resonator neurons: ``tau_w = 10, coupling_factor = 0.26``
# TODO: figure out why not working?
#cell_tag = "RZ"
#tau_w = 10.
#v_reset = -60. #-65.
#w_reset = -1. #8.
#coupling_factor = 0.26

#v0 = v_reset
#w0 = w_reset

################################################################################
# model setup
################################################################################
from ngcsimlib.compartment import All_compartments
from ngcsimlib.context import Context
from ngcsimlib.commands import Command
from izhikevichCell import IzhikevichCell

def wrapper(compiled_fn):
    def _wrapped(*args):
        # vals = jax.jit(compiled_fn)(*args, compartment_values={key: c.value for key, c in All_compartments.items()})
        vals = compiled_fn(*args, compartment_values={key: c.value for key, c in All_compartments.items()})
        for key, value in vals.items():
            All_compartments[str(key)].set(value)
        return vals
    return _wrapped

class AdvanceCommand(Command):
    compile_key = "advance"
    def __call__(self, t=None, dt=None, *args, **kwargs):
        for component in self.components:
            component.gather()
            component.advance(t=t, dt=dt)

class ResetCommand(Command):
    compile_key = "reset"
    def __call__(self, t=None, dt=None, *args, **kwargs):
        for component in self.components:
            component.reset(t=t, dt=dt)

## create 1-node system with IZH cell
with Context("Context") as context:
    a = IzhikevichCell("a", n_units=1, tau_w=tau_w, v_reset=v_reset,
                        w_reset=w_reset, coupling_factor=coupling_factor,
                        integration_type="euler", v0=v0, w0=w0, key=subkeys[0])
    advance_cmd = AdvanceCommand(components=[a], command_name="Advance")
    reset_cmd = ResetCommand(components=[a], command_name="Reset")

compiled_advance_cmd, _ = advance_cmd.compile()
wrapped_advance_cmd = wrapper(jit(compiled_advance_cmd))

compiled_reset_cmd, _ = reset_cmd.compile()
wrapped_reset_cmd = wrapper(jit(compiled_reset_cmd))

################################################################################
# simulation
################################################################################

curr_in = []
mem_rec = []
recov_rec = []
spk_rec = []

i_app = 10. # 0.23 ## electrical current to inject into F-N cell
data = jnp.asarray([[i_app]], dtype=jnp.float32)


time_span = []
#model.reset(do_reset=True)
wrapped_reset_cmd()
t = 0.
for ts in range(T):
    x_t = data
    #if ts <= 5000:
    #    x_t = data * 0
    a.j.set(x_t)
    wrapped_advance_cmd(t, dt) ## pass in t and dt and run step forward of simulation
    t = t + dt

    ## naively extract simple statistics at time ts and print them to I/O
    v = a.v.value # model.components["a"].voltage
    w = a.w.value #model.components["a"].recovery
    s = a.s.value # model.components["a"].outputCompartment
    curr_in.append(data)
    mem_rec.append(v)
    recov_rec.append(w)
    spk_rec.append(s)
    ## print stats to I/O (overriding previous print-outs to reduce clutter)
    print("\r {}: s {} ; v {} ; w {}".format(ts, s, v, w), end="")
    time_span.append((ts)*dt)
print()
time_span = np.asarray(time_span)

## Post-process statistics (convert to arrays) and create plot
curr_in = np.squeeze(np.asarray(curr_in))
mem_rec = np.squeeze(np.asarray(mem_rec))
recov_rec = np.squeeze(np.asarray(recov_rec))
spk_rec = np.squeeze(np.asarray(spk_rec))

# Plot the Izh cell trajectory
n_plots = 1
fig, ax = plt.subplots(1, n_plots, figsize=(5*n_plots,5))

ax_ptr = ax
ax_ptr.set(xlabel='Time', ylabel='voltage (v), recovery (w)',
           title="Izhikevich ({}) Voltage/Recovery Dynamics".format(cell_tag))

v = ax_ptr.plot(time_span, mem_rec, color='C0')
w = ax_ptr.plot(time_span, recov_rec, color='C1', alpha=.5)
ax_ptr.legend([v[0],w[0]],['v','w'])

plt.tight_layout()
plt.savefig("{0}".format("{}_izhcell_plot.png".format(cell_tag.lower())))
