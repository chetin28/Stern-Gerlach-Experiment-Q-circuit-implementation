#Q3: Stern-Gerlach experiment. cetin ilhan kaya

from qiskit import *
from qiskit.tools import job_monitor
from qiskit.visualization import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
from random import randrange

#generating random angle for defining directions of silver atoms
r=0
def randomangle():
    x = np.random.normal(0,1)
    y = np.random.normal(0,1)
    z = np.random.normal(0,1)
    x=x*(-1)*np.random.random()
    y=y*(-1)*np.random.random()
    z=z*(-1)*np.random.random()
    r = sqrt(x**2+y**2+z**2)
    a = atan(y/x)
    b = acos(z/r)
    return [a,b]

#defining state as angular position
def position(A):
    a=A[0]
    b=A[1]
    x = sin(b)*cos(a)
    y = sin(b)*sin(a)
    z = cos(b)
    return [x,y,z]
#defining spin in z direction
def spins(s):
    return np.dot([0,0,1],s)

#constructing Stern-Gerlach experiment
def classic_SG(n):
    atom = [position(randomangle()) for _ in range(n)]
    spin = [spins(s) for s in atom]
    return atom, spin

atom, spin = classic_SG(1000)
plt.figure(figsize=(16,12),dpi=80)
plt.hist(spin,bins=1000)
plt.title("Classical expectation of SG experiment")
plt.xlabel("spin-z values")
plt.ylabel("number of atoms")
plt.savefig("classicalSG.jpg")

q = QuantumRegister(1,"q")
c = ClassicalRegister(1,"c")
qc = QuantumCircuit(q,c)

qc.h(q[0])
qc.p(pi/2,q[0])
qc.h(q[0])
qc.measure(q,c)
qcd=qc.draw("mpl")
qcd.savefig("SG_circuit.jpg",dpi=180)
qcd

job = execute(qc,Aer.get_backend("qasm_simulator"))
results=job.result().get_counts()
hist= plot_histogram(results)
hist.savefig("SG_hist.jpg")
hist


IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q-education', group='mid-east-tech-un-1', project='2300343-Intro-Computational-Methods')
backend = provider.get_backend("ibmq_manila")
trans = transpile(qc, backend, optimization_level=2)
job2 = backend.run(trans)
job_monitor(job2,interval=2)
results = job2.result()
final = results.get_counts()
real_hist = plot_histogram(final)
real_hist.savefig("real_qubit_hist.jpg")


