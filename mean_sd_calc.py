import sys
import numpy as np

f = open(sys.argv[1], 'r')
newfile = "new_word.txt"

res = []
for line in f:
	stuff = line.strip().split()
	numpy_array = np.array(stuff[1:]).astype(np.integer)
	mean = round(np.mean(numpy_array), 2)
	sd = round(np.std(numpy_array), 5)
	tup = (stuff[0], str(float(mean)), str(float(sd)), '[%s]' % ', '.join(map(str, stuff[1:])))
	res.append(tup)

new_f = open(newfile, 'w')
for line in res:
	str_line = '\t'.join(line) + '\n'
	new_f.write(str_line)