import subprocess
import threading

class CMDProcess(threading.Thread):
    '''
        执行CMD命令行的 进程
    '''
    def __init__(self, args,callback):
        threading.Thread.__init__(self)
        self.args = args
        self.callback=callback
        
    def run(self):
        self.proc = subprocess.Popen(
            self.args,
            bufsize=0,
            shell = False,
            stdout=subprocess.PIPE
        )
        
        while self.proc.poll() is None:
            line = self.proc.stdout.readline()
            line = line.decode("utf8") 
            if(self.callback):
                self.callback(line)


def getSubInfo(text):
    print("子进程测试代码实时输出内容=>" + text)

def main():

    cmd = [
            'python',
            '-u', # 注意，这里必须带上-u
            'code_test.py'
            ]
    print("子进程测试代码的运行命令：", ' '.join(cmd))
    testProcess = CMDProcess(cmd,getSubInfo )
    testProcess.start()

main()
