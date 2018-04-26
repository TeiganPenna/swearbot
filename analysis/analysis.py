import re
import matplotlib.pyplot as plt
import numpy as np
import time
import os

def plot(names, swearcounts, filename):
	plt.rcdefaults()
	fig, ax = plt.subplots()
	y_pos = np.arange(len(names))
	ax.barh(y_pos, swearcounts, align='center', color='#5DADE2')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(names)
	ax.invert_yaxis()
	ax.set_xlabel('Swear count')
	ax.set_title('Swearbot log')

	plt.savefig(filename, bbox_inches='tight')


log = {}
pattern = '^INFO:root:Reprimanded (.+?) in channel.*$'

with open('swearbot.log') as f:
	for line in f:
		match = re.match(pattern, line.strip())
		if match and match.group(1):
			name = match.group(1)
			if name in log:
				log[name] += 1
			else:
				log[name] = 1

filename = 'figure_{0}.png'.format(time.time())
names, swearcounts = zip(*log.items())
plot(names, swearcounts, filename)
os.system("start " + filename)
