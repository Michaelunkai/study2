from brian2 import *

# Define model parameters
tau = 10*ms
v_rest = -70*mV
v_reset = -65*mV
threshold = -50*mV
refractory_period = 5*ms

# Set up neuron group
eqs = '''
dv/dt = (v_rest - v) / tau : volt
'''
neurons = NeuronGroup(1, eqs, threshold='v > threshold', reset='v = v_reset', refractory=refractory_period)
neurons.v = v_rest

# Set up a monitor
monitor = StateMonitor(neurons, 'v', record=True)

# Run the simulation
run(100*ms)

# Plot the results
plot(monitor.t/ms, monitor.v[0]/mV)
xlabel('Time (ms)')
ylabel('Voltage (mV)')
show()
