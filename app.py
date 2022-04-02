from flask import Flask, render_template
from flask_socketio import SocketIO
import secrets
import subprocess as sub
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
socketio = SocketIO(app)

@app.route('/')
def main():
	return render_template('index.html')

def testOut(data):
	socketio.emit('send data', data)

def tcpLoop():
	p = sub.Popen(['sudo', '/usr/sbin/tcpdump', '-nn', '(icmp[0] == 8) || (icmp6 && ip6[40] == 0x80)', '-U', '-l', '-t'], stdout=sub.PIPE)
	for line in iter(p.stdout.readline, b''):
		line = line.decode('utf-8').split()
		if (line[4] == 'ICMP6,'):
			line[4] = 'ICMP6'
		data = '{"ip":"' + line[1] + '", "type":"' + line[4] + '", "id":"' + line[8][:-1] + '", "seq":"' + line[10][:-1] + '", "len":"' + line[12] + '"}'
		testOut(data)
		
eventlet.spawn(tcpLoop)

if __name__ == '__main__':
	socketio.run(app, host = '0.0.0.0', port = 8080)