import matplotlib.pyplot as plt
import re
import sys

# open file for reading
if (len(sys.argv) > 1):
    filein = open(sys.argv[1], 'r')
else:
    raise Exception("Please provide an input log file")

regex = re.compile(r'\[Queue:(\d*)\]')
queueSize = list()

# get increasing queue size
for line in filein:
    m = re.search(regex, line)
    if m is not None:
        queueSize.append(m.group(1))

# close file
filein.close()

plt.figure(0)
plt.plot(list(range(0, len(queueSize))), queueSize)
plt.title("Queue Size of Subreddits Linking to Other Subreddits BFS")
plt.xlabel("Subreddits searched")
plt.ylabel("Queue Size")
plt.show()
