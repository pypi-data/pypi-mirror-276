#from ngcsimlib.controller import Controller
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

## F-N cell hyperparameters
alpha = 0.3 ## recovery variable shift factor
beta = 1.4 ## recovery variable scale factor
gamma = 1. ## membrane potential power term denominator
tau_w = 20. ## recovery variable time constant
v0 = -0.63605838 ## initial membrane potential (for reset condition)
w0 = -0.16983366 ## initial recovery value (for reset condition)

################################################################################
# model setup
################################################################################
from ngcsimlib.compartment import All_compartments
from ngcsimlib.context import Context
from ngcsimlib.commands import Command
from fitzhughNagumoCell import FitzhughNagumoCell

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

with Context("Context") as context:
    a = FitzhughNagumoCell("a1", n_units=1, tau_w=tau_w, alpha=alpha, beta=beta,
                           gamma=gamma, v0=v0, w0=w0, integration_type="euler")
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

i_app = 0.23 ## electrical current to inject into F-N cell
data = jnp.asarray([[i_app]], dtype=jnp.float32)

T = 1500 ## number of simulation steps to run
time_span = np.linspace(0, 200, num=T)

## compute integration time constant
dt = time_span[1] - time_span[0] # ~ 0.13342228152101404 ms


#wrapped_reset_cmd()  #model.reset(do_reset=True)
t = 0.
for ts in range(T):
    x_t = data
    a.j.set(x_t)
    wrapped_advance_cmd(t, dt) ## pass in t and dt and run step forward of simulation
    t = t + dt

    ## naively extract simple statistics at time ts and print them to I/O
    v = a.v.value # model.components["a"].voltage
    w = a.w.value #model.components["a"].recovery
    s = a.s.value # model.components["a"].outputCompartment
    curr_in.append(x_t)
    mem_rec.append(v)
    recov_rec.append(w)
    spk_rec.append(s)
    ## print stats to I/O (overriding previous print-outs to reduce clutter)
    print("\r {}: s {} ; v {} ; w {}".format(ts, s, v, w), end="")
    # print(f"---[ Step {i} ]---")
    # print(f"[a] j: {a.j.value}, v: {a.v.value}, w: {a.w.value}, s: {a.s.value}, " \
    #       f"tols: {a.tols.value}")
print()

## Post-process statistics and create plot
curr_in = np.squeeze(np.asarray(curr_in))
mem_rec = np.squeeze(np.asarray(mem_rec))
recov_rec = np.squeeze(np.asarray(recov_rec))
spk_rec = np.squeeze(np.asarray(spk_rec))

# Plot the F-N cell trajectory
n_plots = 1
fig, ax = plt.subplots(1, n_plots, figsize=(5*n_plots,5))

ax_ptr = ax
ax_ptr.set(xlabel='Time', ylabel='voltage (v), recovery (w)',
           title='Fitzhugh-Nagumo Voltage/Recovery Dynamics')

v = ax_ptr.plot(time_span, mem_rec, color='C0')
w = ax_ptr.plot(time_span, recov_rec, color='C1', alpha=.5)
ax_ptr.legend([v[0],w[0]],['v','w'])

plt.tight_layout()
plt.savefig("{0}".format("fncell_plot.png"))
