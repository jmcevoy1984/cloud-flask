import subprocess
from flask import Flask, jsonify


def run_command(command):
    process = subprocess.run(command, capture_output=True)
    try:
        process.check_returncode()
    except subprocess.CalledProcessError:
        print('DEBUG:', 'cmd:', process.args, 'result:', process.stderr.decode())
        return 'Error - Command Failed'
    output = process.stdout.decode()
    print('DEBUG:', 'cmd:', process.args, 'result:', output)
    return output.rstrip()

def get_hostname():
    command = ["hostname"]
    return run_command(command)

def get_ip():
    command = ["hostname", "-I"]
    return run_command(command)

def get_cpu_count():
    command = ["egrep", "-c", "^processor", "/proc/cpuinfo"]
    return run_command(command)

def get_memory_size():
    free_process = subprocess.Popen(["free", "-h", "-t"], stdout=subprocess.PIPE)
    grep_process = subprocess.Popen(["grep", "Total:"], stdin=free_process.stdout, stdout=subprocess.PIPE)
    awk_process = subprocess.Popen(["awk", "{print $2}"], stdin=grep_process.stdout, stdout=subprocess.PIPE)
    output = awk_process.communicate()[0]
    decoded_output = output.decode().rstrip()
    print('DEBUG:', decoded_output)
    return decoded_output + 'B'

def get_json_ouput():
    json_output = {
        "hostname": get_hostname(),
        "ip_address": get_ip(),
        "cpus": get_cpu_count(),
        "memory": get_memory_size()
    }
    return json_output

app = Flask(__name__)

@app.route('/status')
def get_status():
    return jsonify(get_json_output), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')