# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentation/input/joystick-api.txt

import os, struct, array, signal
from fcntl import ioctl

# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))

# We'll store the states here.
axis_states0 = {}
axis_states1 = {}
button_states0 = {}
button_states1 = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map0 = []
axis_map1 = []
button_map0 = []
button_map1 = []

# Open the joystick device.
fn0 = '/dev/input/js0'
fn1 = '/dev/input/js1'
print('Opening %s...' % fn0)
jsdev0 = open(fn0, 'rb')
jsdev1 = open(fn1, 'rb')

def getname(jsdev):
# Get the device name.
#buf = bytearray(63)
	buf = array.array('c', ['\0'] * 64)
	ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
	js_name = buf.tostring()
	print('Device name: %s' % js_name)
	return js_name
def getaxes(jsdev):
	# Get number of axes and buttons.
	buf = array.array('B', [0])
	ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
	num_axes = buf[0]
	buf = array.array('B', [0])
	ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
	num_buttons = buf[0]
	t_axes = (num_axes, num_buttons)
	return t_axes

def getaxismap(jsdev, num_axes):
# Get the axis map.
	buf = array.array('B', [0] * 0x40)
	ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP
	axis_map = []
	axis_states = {}

	for axis in buf[:num_axes]:
    		axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    		axis_map.append(axis_name)
    		axis_states[axis_name] = 0.0
		t_axismap=(axis_name, axis_map, axis_states)
	return t_axismap

def getbuttonmap(jsdev, num_buttons):
# Get the button map.
	buf = array.array('H', [0] * 200)
	ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP
	button_map = []
	button_states = {}

	for btn in buf[:num_buttons]:
    		btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    		button_map.append(btn_name)
    		button_states[btn_name] = 0
		t_btnmap = (btn_name, button_map, button_states)
	return t_btnmap


def eventloop(jsdev, button_map, button_states, axis_map, axis_states):
	evbuf = jsdev.read(8)

   	if evbuf:
        	time, value, type, number = struct.unpack('IhBB', evbuf)

        if type & 0x80:
             	print "(initial)",

        if type & 0x01:
		button = button_map[number]
            	if button:
                	button_states[button] = value
               		if value:
                   		print "%s pressed" % (button)
		    		os.system('killall omxplayer.bin')
                	else:
                    		print "%s released" % (button)

        	if type & 0x02:
            		axis = axis_map[number]
            		if axis:
                		fvalue = value / 32767.0
                		axis_states[axis] = fvalue
                		print "%s: %.3f" % (axis, fvalue)
# Main event loop
if __name__ == "__main__":
	js_name0 = getname(jsdev0)
	js_name1 = getname(jsdev1)
	num_axes0 = getaxes(jsdev0)[0]
	num_axes1 = getaxes(jsdev1)[0]
	num_buttons0 = getaxes(jsdev0)[1]
	num_buttons1 = getaxes(jsdev1)[1]
	axis_name0 = getaxismap(jsdev0, num_axes0)[0]
	axis_name1= getaxismap(jsdev1, num_axes1)[0]
	axis_map0 = getaxismap(jsdev0, num_axes0)[1]
	axis_map1= getaxismap(jsdev1,num_axes1)[1]
	axis_states0= getaxismap(jsdev0, num_axes0)[2]
	axis_states1= getaxismap(jsdev1, num_axes1)[2]
	button_name0= getbuttonmap(jsdev0, num_buttons0)[0]
	button_name1= getbuttonmap(jsdev1, num_buttons1)[0]
	button_map0=getbuttonmap(jsdev0, num_buttons0)[1]
	button_map1=getbuttonmap(jsdev1, num_buttons1)[1]	
	button_states0=getbuttonmap(jsdev0, num_buttons0)[2]
	button_states1=getbuttonmap(jsdev1, num_buttons1)[2]
while True:
	#eventloop(jsdev0, button_map0, button_states0, axis_map0, axis_states0)
	eventloop(jsdev1, button_map1, button_states1,axis_map1, axis_states1)  
