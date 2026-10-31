import os
import subprocess
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

VERSION = os.environ.get('APP_VERSION', 'dev')


def get_numbers():
    data = request.get_json()
    a = float(data['a'])
    b = float(data['b'])
    return a, b


@app.route('/')
def index():
    return render_template('index.html', version=VERSION)


@app.route('/version')
def version():
    return jsonify({'version': VERSION})


@app.route('/add', methods=['POST'])
def add():
    try:
        a, b = get_numbers()
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'некорректные числа'}), 400
    return jsonify({'result': a + b})


@app.route('/subtract', methods=['POST'])
def subtract():
    try:
        a, b = get_numbers()
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'некорректные числа'}), 400
    return jsonify({'result': a - b})


@app.route('/multiply', methods=['POST'])
def multiply():
    try:
        a, b = get_numbers()
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'некорректные числа'}), 400
    return jsonify({'result': a * b})


@app.route('/divide', methods=['POST'])
def divide():
    try:
        a, b = get_numbers()
    except (KeyError, ValueError, TypeError):
        return jsonify({'error': 'некорректные числа'}), 400
    if b == 0:
        return jsonify({'error': 'на ноль делить нельзя'}), 400
    return jsonify({'result': a / b})


@app.route('/api/resolve', methods=['POST'])
def resolve_host():
    data = request.get_json() or {}
    host = data.get('host', '')
    try:
        output = subprocess.check_output(f"getent hosts {host}", shell=True, text=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'output': output})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
