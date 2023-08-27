import numpy as np
import math
from qiskit.circuit import Parameter
from qiskit import *
from math import pi,cos,sin,tan,atan
import os

from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from qiskit.providers.aer import QasmSimulator
def execute_circuit_sv(quantum_circuit):
    statevector_simulator = Aer.get_backend('statevector_simulator')
    result = execute(quantum_circuit, statevector_simulator).result()
    statevector_results = result.get_statevector(quantum_circuit)
    circuit_diagram = quantum_circuit.draw('mpl')
    b_sphere = plot_bloch_multivector(statevector_results)
    
    return statevector_results, circuit_diagram, b_sphere


def everything(no_qubits, gate_1, gate_2, angle_multiplier):
    
    param_theta = Parameter('θ')
    n = int(no_qubits)
    bell = QuantumCircuit(n, name='entanglement')

    rot = int(gate_1)
    if rot==1:
        bell.rx(param_theta,0)
    elif rot==2:
        bell.ry(param_theta,0)

    control = int(gate_2)
    if control==1:
        for i in range (0,n-1):
            bell.cx(i,i+1)
    elif control==2:
        for j in range(0,n-1):
            bell.cy(j,j+1)

    import numpy as np
    from math import pi,cos,sin,tan,atan
    x = float(angle_multiplier)

    bell = bell.bind_parameters({param_theta:  (x * np.pi)})

    result, img, bsphere = execute_circuit_sv(bell)
    img.savefig('static/img/img.png')
    bsphere.savefig('static/img/bsphere.png')

    from qiskit.quantum_info import DensityMatrix, partial_trace
    D = DensityMatrix(bell)

    r = x / 0.5
    if x % 0.5 == 0 and r % 2 != 0:
        final_op = "maximal"
    else:
        final_op = "partial"

    return final_op



















from flask import Flask, render_template, request

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'img')

app.config['UPLOAD_FOLDER'] = IMG_FOLDER


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        no_qubits_form = request.form['no_qubits']
        gate_1_form = request.form['gate_1']
        gate_2_form = request.form['gate_2']
        angle_multiplier_form = request.form['angle_multiplier']
        res0 = everything(no_qubits_form, gate_1_form, gate_2_form, angle_multiplier_form)
        print(res0)

        return render_template('index.html', res = res0)
    else:
        return render_template('index.html',  prediction="Something went wrong")


if __name__ == '__main__':
    app.run(debug=True)