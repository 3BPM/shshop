import paramiko
from io import StringIO

class SSHProxy(object):

    def __init__(self, hostname, port, username, private_key_string):
        self.hostname = hostname
        self.port = port
        self.username = username

        self.private_key = paramiko.RSAKey(file_obj=StringIO(private_key_string))

        self.transport = None

    def open(self):
        self.transport = paramiko.Transport((self.hostname, self.port))
        self.transport.connect(username=self.username, pkey=self.private_key)

    def close(self):
        self.transport.close()

    def command(self, cmd):
        ssh = paramiko.SSHClient()
        ssh._transport = self.transport
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        # ssh.close()
        return result

    def upload(self, local_path, remote_path):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.put(local_path, remote_path)
        sftp.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    with SSHProxy('10.211.55.25', 22, 'root', 'asdasdfasdfasdfasdfasdf') as proxy:
        proxy.upload('xx','xx')
        proxy.command('ifconfig')
        proxy.command('ifconfig')
        proxy.upload('xx', 'xx')
    with SSHProxy('10.211.55.26', 22, 'root', 'aasdfasdfa') as proxy:
        proxy.upload('xx','xx')
        proxy.command('ifconfig')
        proxy.command('ifconfig')
        proxy.upload('xx', 'xx')