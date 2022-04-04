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

def tcpEmit(data):
	# if (arr[2] == 'ICMP6,'):
	# 	arr[2] = 'ICMP6'
	# data = '{"ttl":"' + arr[0] + '", "ip":"' + arr[1] + '", "type":"' + arr[2] + '", "id":"' + arr[3] + '", "seq":"' + arr[4] + '", "len":"' + arr[5] + '"}'
	# print(data)
	socketio.emit('send data', data)

def tcpLoop():
	# flag = False
	# tempArr = []
	p = sub.Popen(['tcpdump', '-nn', '(icmp[0] == 8) || (icmp6 && ip6[40] == 0x80)', '-U', '-l', '-t'], stdout=sub.PIPE)
	for line in iter(p.stdout.readline, b''):
		line = line.decode('utf-8').split()
		# print(line)
		# if (flag == False):
		# 	tempArr.append(line[4][:-1])
		# else:
		# 	# print(line)
		# 	if (line[0] == 'IP6'):
		# 		print('hehe')
		# 	else:
		# 		tempArr.append(line[0])
		# 		tempArr.append(line[3])
		# 		tempArr.append(line[7][:-1])
		# 		tempArr.append(line[9][:-1])
		# 		tempArr.append(line[11])
		# 	tcpEmit(tempArr)
		# 	tempArr = []
		# flag = not flag
		# print(line[16])
		if (line[4] == 'ICMP6,'):
			line[4] = 'ICMP6'
		data = '{"ip":"' + line[1] + '", "type":"' + line[4] + '", "id":"' + line[8][:-1] + '", "seq":"' + line[10][:-1] + '", "len":"' + line[12] + '"}'
		tcpEmit(data)
		
eventlet.spawn(tcpLoop)

if __name__ == '__main__':
	socketio.run(app, host = '0.0.0.0', port = 8080)
