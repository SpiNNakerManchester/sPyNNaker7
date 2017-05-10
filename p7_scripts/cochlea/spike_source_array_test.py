import spynnaker7.pyNN as p
import sys
from _collections import defaultdict
import math
import numpy
import struct

numpy.set_printoptions(threshold=numpy.nan, suppress=True, precision=3)
fileName = "en_un_lugar_de_la_mancha_.aedat"

def createSpikeSourceArray(aedat):
    listaResultado = [[] for i in range(256)]
    for i in range(0, len(aedat)):
        listaResultado[aedat[i][0]].append(aedat[i][1]/1000)
    return listaResultado

def loadAedat(path):
    f = open(path, "rb")
    pos = 0
    evt = 0
    timestamp = 0
    rowID = 0
    aedatFile = []
    minTimestamp = None
    try:
        while True:
            lec = f.read(1)
            if lec == "":
                break
            evt = struct.unpack("<B", lec)
            pos += 8
            evt = evt[0] << 8
            evt = evt | struct.unpack("<B", f.read(1))[0]
            pos += 8
            evt = struct.unpack("<B", f.read(1))[0]
            pos += 8
            evt = evt << 8
            evt = evt | struct.unpack("<B", f.read(1))[0]
            evt = 0x000000FF & evt
            pos += 8

            timestamp = f.read(1)
            timestamp = struct.unpack("<B", timestamp)

            pos += 8
            timestamp = timestamp[0] << 8
            timestamp = timestamp | struct.unpack("<B", f.read(1))[0]
            pos += 8
            timestamp = timestamp << 8
            timestamp = timestamp | struct.unpack("<B", f.read(1))[0]
            pos += 8
            timestamp = timestamp << 8
            timestamp = timestamp | struct.unpack("<B", f.read(1))[0]
            pos += 8

            if rowID == 0:
                minTimestamp = timestamp

            row = numpy.array([evt, timestamp - minTimestamp])
            aedatFile.append(row)
            rowID += 1
    finally:
        f.close()
    return aedatFile

cell_params_lif = {'cm'        : 0.25, # nF
                     'i_offset'  : 0.0,
                     'tau_m'     : 20.0,
                     'tau_refrac': 0.0,
                     'tau_syn_E' : 1.0,
                     'tau_syn_I' : 1.0,
                     'v_reset'   : -70.0,
                     'v_rest'    : -65.0,
                     'v_thresh'  : -50.0
                     }

input_size = 28
dur_test = 1000 #1000 #ms
silence = 200 #ms
SUM_rate = 2000.

p.setup(timestep=1.0, min_delay=1.0, max_delay=3.0)

spike_source_data = createSpikeSourceArray(loadAedat(fileName))
max_time = 0
input_spikes = list()
neuron_id = 0
for neuron_data in spike_source_data:
    if len(neuron_data) > 0:
        max_time = max((max_time, max(neuron_data)))
    for spike_time in neuron_data:
        input_spikes.append(numpy.array([neuron_id, math.ceil(spike_time)]))
    neuron_id += 1
max_time = int(max_time) + 100

input_spikes = numpy.array(input_spikes)
input_spikes = input_spikes[numpy.lexsort((input_spikes[:,0], input_spikes[:,1]))]

pop_input = p.Population(256, p.SpikeSourceArray,
                           {'spike_times': spike_source_data})
pop_input.record()

pop_output = p.Population(256, p.IF_curr_exp, cell_params_lif)
#pop_output.record()

p.Projection(pop_input, pop_output, p.OneToOneConnector(weights=5.0))

print "Running for {}ms".format(max_time)
p.run(max_time)

#spikes = pop_output.getSpikes()
spikes = pop_input.getSpikes()
spikes = spikes[numpy.lexsort((spikes[:,0], spikes[:,1]))]



i = 0
j = 0
print len(input_spikes), len(spikes)
while i < len(input_spikes) or j < len(spikes):

    if i < len(input_spikes) and j < len(spikes):
        if input_spikes[i][1] == spikes[j][1]:
            if input_spikes[i][0] == spikes[j][0]:
                #print "{:10.3f} {:7d} {:7d}".format(
                #    input_spikes[i][1], int(input_spikes[i][0]),
                #    int(spikes[j][0]))
                i += 1
                j += 1
            elif input_spikes[i][0] < spikes[j][0]:
                print "{:10.3f} {:7d}       _".format(
                    input_spikes[i][1], int(input_spikes[i][0]))
                i += 1
            else:
                print "{:10.3f}       _ {:7d}".format(
                    spikes[j][1], int(spikes[j][0]))
                j += 1
        elif input_spikes[i][1] < spikes[j][1]:
            print "{:10.3f} {:7d}       _".format(
                input_spikes[i][1], int(input_spikes[i][0]))
            i += 1
        else:
            print "{:10.3f}       _ {:7d}".format(
                spikes[j][1], int(spikes[j][0]))
            j += 1
    elif i < len(input_spikes):
        print "{:10.3f} {:7d}       _".format(
            input_spikes[i][1], int(input_spikes[i][0]))
        i += 1
    else:
        print "{:10.3f}       _ {:7d}".format(
            spikes[j][1], int(spikes[j][0]))
        j += 1
