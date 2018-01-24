import flowio
import flowutils
import numpy

fd = flowio.FlowData('test_data_2d_01.fcs')
events = numpy.reshape(fd.events, (-1, fd.channel_count))

fluoro_indices = [0, 1]

xform_events = flowutils.transforms.logicle(events, fluoro_indices)

print('asdf')
