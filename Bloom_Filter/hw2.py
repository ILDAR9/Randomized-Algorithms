import time
from random import randint
import math
import matplotlib.pyplot as plt

class Bits:
	def __init__(self, size):
		self.bits = [0] * size

	def test(self, index):
		return (self.bits[math.floor(index / 32)] >> (index % 32)) & 1

	def set(self, index):
		self.bits[math.floor(index / 32)] |= 1 << (index % 32)


def Hash():
	seed = randint(0, 31) + 32
	def inter_hash(string):
		result = 1
		for s in string:
			result = (seed * result + ord(s)) & 0xFFFFFFFF
		return result

	return inter_hash


class Bloom:

	# function of Hash
	def __init__(self, size, functions):
		self.size = size
		self.functions = functions
		self.bits = Bits(size)

	def add(self, string):
		for f in self.functions:
			self.bits.set(f(string) % self.size)

	def test(self, string):
		for f in self.functions:
			if not self.bits.test(f(string) % self.size):
				return False
		return True

def OptimalBloom(max_members, error_probability, count = None): 
	size = -(max_members * math.log(error_probability)) / (math.log(2) * math.log(2))

	size = round(size)
	if count:
		count = count
	else:
		count = round((size / max_members) * math.log(2))

	functions = []
	for i in range(count):
		functions.append(Hash())

	return Bloom(size, functions);

def study_filter(n=999999, err_p = 00.1):
	with open('urls1_train.txt', 'r') as f:
		lines = f.readlines()[:n]
		# urls = Bloom((8 * len(lines)), [Hash() for i in range(6)])
		urls = OptimalBloom(len(lines), error_probability=err_p)
		for l in lines:
			urls.add(l.strip())
	return urls

def test_urls(urls_bloom):
	err_n = 0
	with open('urls2.txt', 'r') as f:
		lines=f.readlines()
		for i, l in enumerate(lines,1):
			l = l.strip()
			if urls_bloom.test(l):
				# print("%d) %s" % (i, l))
				err_n = err_n+1

	# print("FP number = %d / %d" % (n, len(lines)))
	return float(err_n) / len(lines)


def performance_err_rate(err_p=0.01):
	ns = range(500, 10000, 500)
	errs = []
	for n in ns :
		urls = study_filter(n,err_p)
		err_rate = test_urls(urls)
		print('%d %f' % (n, err_rate))
		errs.append(err_rate)
	return errs

def performance_space(err_p=0.01):
	ns = range(500, 10000, 500)
	sps = []
	for n in ns :
		urls = study_filter(n, err_p)
		sps.append(urls.size)
		print('%d %d' % (n, urls.size))
	return sps

def plot_performace():
	
  	ns = list(range(500, 10000, 500))
  # ns = list(range(10000,100001,10000))
  	qs = performance_err_rate(err_p=0.01)
  	rqs = performance_err_rate(err_p=0.05)


  	plt.plot(ns, qs)
  	plt.plot(ns, rqs)

  	plt.legend(['a = 0.01', 'a = 0.05'], loc='upper left')
  	plt.ylabel('err_rate')
  	plt.xlabel('#n of set')

  	plt.show()

def plot_performace_space():
	
  	ns = list(range(500, 10000, 500))
  # ns = list(range(10000,100001,10000))
  	qs = performance_space(err_p=0.01)
  	rqs = performance_space(err_p=0.05)


  	plt.plot(ns, qs)
  	plt.plot(ns, rqs)

  	plt.legend(['a = 0.01', 'a = 0.05'], loc='upper left')
  	plt.ylabel('bits count')
  	plt.xlabel('#n of set')

  	plt.show()

# plot_performace()
plot_performace_space()



"""
space
500 4793
1000 9585
1500 14378
2000 19170
2500 23963
3000 28755
3500 33548
4000 38340
4500 43133
5000 47925
5500 52718
6000 57510
6500 62303
7000 67095
7500 71888
8000 76680
8500 81473
9000 86266
9500 91058
"""

"""
 err rate
 500 0.010000
1000 0.014000
1500 0.004000
2000 0.008000
2500 0.004000
3000 0.010000
3500 0.008000
4000 0.012000
4500 0.012000
5000 0.020000
5500 0.014000
6000 0.016000
6500 0.012000
7000 0.008000
7500 0.014000
8000 0.008000
8500 0.012000
9000 0.008000
9500 0.008000

 """

