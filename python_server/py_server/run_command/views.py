import json
import asyncio
import os
import signal
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer
import threading
from concurrent.futures import ThreadPoolExecutor
from django.http import HttpResponse
import psutil
import subprocess
from threading import Timer
# executor = ThreadPoolExecutor(max_workers=1)

def saveCode(request):
    if request.method == 'POST':
        code = json.loads(request.body).get('code')
        if not code:
            return HttpResponse(status=400)
        # 写入文件
        with open('code_test.py', 'w') as f:
            f.write(code)
            return HttpResponse(status=200)
    else:
        # 返回方法不允许
        return HttpResponse(status=405)




import json
import asyncio
import os
import signal
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer
import threading
from concurrent.futures import ThreadPoolExecutor
from django.http import HttpResponse
import psutil

# executor = ThreadPoolExecutor(max_workers=1)

def saveCode(request):
    if request.method == 'POST':
        code = json.loads(request.body).get('code')
        if not code:
            return HttpResponse(status=400)
        # 写入文件
        with open('code_test.py', 'w') as f:
            f.write(code)
            return HttpResponse(status=200)
    else:
        # 返回方法不允许
        return HttpResponse(status=405)
    

def getCode(request):
    if request.method == 'GET':
        with open('code_test.py', 'r') as f:
            code = f.read()
            return HttpResponse(code)
    else:
        return HttpResponse(status=405)

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process = None  # 用于存储当前正在执行的进程
        self.is_connected = True
        self.thread = None  # 新增：用于存储执行命令的线程

    async def connect(self):
        await self.accept()
        self.is_connected = True

    async def disconnect(self, close_code):
        # 确保进程被终止
        if self.process and self.process.poll() is None:
            self.kill(self.process.pid)
        self.is_connected = False
        print("Disconnected")

        # 新增：如果有正在运行的线程，等待其结束
        if self.thread and self.thread.is_alive():
            self.thread.join()

    async def receive(self, text_data):
        if text_data == "kill":
            # 如果收到终止命令，终止当前进程
            if self.process and self.process.poll() is None:
                self.kill(self.process.pid)
                await self.send_message("killed")
                print("Process killed")
            return

        # 如果不是终止命令，则执行收到的命令
        command = text_data
        print(f"Received command: {command}")

        # 开始一个新的线程来执行命令
        self.thread = threading.Thread(target=self._execute_command, args=(command,))
        self.thread.start()

    def kill(self, proc_pid):
        """Kill a process and its children."""
        parent_proc = psutil.Process(proc_pid)
        for child_proc in parent_proc.children(recursive=True):
            child_proc.kill()
        parent_proc.kill()

    def _execute_command(self, command):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        # 发送开始消息
        new_loop.run_until_complete(self.send_message(f"start_{command}"))

        self.process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        try:
            # 实时读取输出
            for stdout_line in iter(self.process.stdout.readline, ''):
                if not self.is_connected:
                    break
                if stdout_line:
                    new_loop.run_until_complete(self.send_message(stdout_line))

            for stderr_line in iter(self.process.stderr.readline, ''):
                if not self.is_connected:
                    break
                if stderr_line:
                    new_loop.run_until_complete(self.send_message(stderr_line))

        except KeyboardInterrupt:
            new_loop.run_until_complete(self.send_message("命令已被强制终止"))
        except Exception as e:
            new_loop.run_until_complete(self.send_message(f"命令执行时出错: {str(e)}"))

        finally:
            if self.process:
                # for stdout_line in iter(self.process.stdout.readline, ''):
                #     if stdout_line:
                #         new_loop.run_until_complete(self.send_message(stdout_line))

                # for stderr_line in iter(self.process.stderr.readline, ''):
                #     if stderr_line:
                #         new_loop.run_until_complete(self.send_message(stderr_line))
                self.process.stdout.close()
                self.process.stderr.close()
                self.process.wait()
                print("Process terminated")

                # 在等待进程结束后发送结束消息
                if  self.is_connected:
                    new_loop.run_until_complete(self.send_message(f"end_{command}"))

            # 新增：清理事件循环
            new_loop.close()

    async def send_message(self, message):
        await self.send(text_data=message)

# executor = ThreadPoolExecutor(max_workers=1)

def saveCode(request):
    if request.method == 'POST':
        code = json.loads(request.body).get('code')
        if not code:
            return HttpResponse(status=400)
        # 写入文件
        with open('code_test.py', 'w') as f:
            f.write(code)
            return HttpResponse(status=200)
    else:
        # 返回方法不允许
        return HttpResponse(status=405)

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process = None  # 用于存储当前正在执行的进程
        self.is_connected = True
        self.thread = None  # 新增：用于存储执行命令的线程
        self.is_kill = False

    async def connect(self):
        await self.accept()
        self.is_connected = True

    async def disconnect(self, close_code):
        # 确保进程被终止
        if self.process and self.process.poll() is None:
            self.kill(self.process.pid)
        self.is_connected = False
        print("Disconnected")

        # 新增：如果有正在运行的线程，等待其结束
        if self.thread and self.thread.is_alive():
            self.thread.join()

    async def receive(self, text_data):
        if text_data == "kill":
            # 如果收到终止命令，终止当前进程
            if self.process and self.process.poll() is None:
                # self.process.kill()
                self.kill(self.process.pid)
                await self.send_message("killed")
                print("Process killed")
            return

        # 如果不是终止命令，则执行收到的命令
        command = text_data
        print(f"Received command: {command}")

        # 开始一个新的线程来执行命令
        self.thread = threading.Thread(target=self._execute_command, args=(command,))
        self.thread.start()

    def kill(self, proc_pid):
        """Kill a process and its children."""
        parent_proc = psutil.Process(proc_pid)
        for child_proc in parent_proc.children(recursive=True):
            child_proc.kill()
        parent_proc.kill()

    def _execute_command(self, command):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)

        # 发送开始消息
        new_loop.run_until_complete(self.send_message(f"start_{command}"))

        self.process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        try:
            # 实时读取输出
            for stdout_line in iter(self.process.stdout.readline, ''):
                print(self.thread.is_alive())
                if (not self.is_connected) or (not self.thread.is_alive()):
                    break
                if stdout_line:
                    new_loop.run_until_complete(self.send_message(stdout_line))

            for stderr_line in iter(self.process.stderr.readline, ''):
                print(self.thread.is_alive())
                if (not self.is_connected) or (not self.thread.is_alive()):
                    break
                if stderr_line:
                    new_loop.run_until_complete(self.send_message(stderr_line))

        except KeyboardInterrupt:
            new_loop.run_until_complete(self.send_message("命令已被强制终止"))
        except Exception as e:
            new_loop.run_until_complete(self.send_message(f"命令执行时出错: {str(e)}"))

        finally:
            if self.process:
                # for stdout_line in iter(self.process.stdout.readline, ''):
                #     if stdout_line:
                #         new_loop.run_until_complete(self.send_message(stdout_line))

                # for stderr_line in iter(self.process.stderr.readline, ''):
                #     if stderr_line:
                #         new_loop.run_until_complete(self.send_message(stderr_line))
                self.process.stdout.close()
                self.process.stderr.close()
                self.process.wait()
                print("Process terminated")

                # 在等待进程结束后发送结束消息
                if  self.is_connected:
                    new_loop.run_until_complete(self.send_message(f"end_{command}"))

            # 新增：清理事件循环
            new_loop.close()

    async def send_message(self, message):
        await self.send(text_data=message)














# class ChatConsumer(AsyncWebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.process = None  # 用于存储当前正在执行的进程
#         self.is_connected = True
#     async def connect(self):
#         await self.accept()
#         self.is_connected = True

#     async def disconnect(self, close_code):
#         # 确保进程被终止
#         if self.process and self.process.poll() is None:
#             self.kill(self.process.pid)
#         self.is_connected = False
#         print("Disconnected")

#     async def receive(self, text_data):
  
#             if text_data == "kill":
#                 # 如果收到终止命令，终止当前进程
#                 if self.process and self.process.poll() is None:
#                     self.kill(self.process.pid)
#                     await self.send_message("killed")
#                     print("Process killed")
#                 return

#             # 如果不是终止命令，则执行收到的命令
#             command = text_data
#             print(f"Received command: {command}")

#             # 开始一个新的线程来执行命令
#             thread = threading.Thread(target=self._execute_command, args=(command,))
#             thread.start()
   

#     def kill(self, proc_pid):
#         """Kill a process and its children."""
#         parent_proc = psutil.Process(proc_pid)
#         for child_proc in parent_proc.children(recursive=True):
#             child_proc.kill()
#         parent_proc.kill()

#     def _execute_command(self, command):
#         new_loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(new_loop)

#         # 发送开始消息
#         new_loop.run_until_complete(self.send_message(f"start_{command}"))

#         self.process = subprocess.Popen(
#             command,
#             shell=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             universal_newlines=True,
#         )

#         try:
#             # 实时读取输出
#             for stdout_line in iter(self.process.stdout.readline, ''):
#                 if not self.is_connected:
#                     break
#                 if stdout_line:
#                     new_loop.run_until_complete(self.send_message(stdout_line))

#             for stderr_line in iter(self.process.stderr.readline, ''):
#                 if not self.is_connected:
#                     break
#                 if stderr_line:
#                     new_loop.run_until_complete(self.send_message(stderr_line))

#         except KeyboardInterrupt:
#             new_loop.run_until_complete(self.send_message("命令已被强制终止"))
#         except Exception as e:
#             new_loop.run_until_complete(self.send_message(f"命令执行时出错: {str(e)}"))

#         finally:
#             if self.process:
#                 # for stdout_line in iter(self.process.stdout.readline, ''):
#                 #     if stdout_line:
#                 #         new_loop.run_until_complete(self.send_message(stdout_line))

#                 # for stderr_line in iter(self.process.stderr.readline, ''):
#                 #     if stderr_line:
#                 #         new_loop.run_until_complete(self.send_message(stderr_line))
#                 self.process.stdout.close()
#                 self.process.stderr.close()
#                 self.process.wait()
#                 print("Process terminated")

#                 # 在等待进程结束后发送结束消息
#                 if  self.is_connected:
#                     new_loop.run_until_complete(self.send_message(f"end_{command}"))

#     async def send_message(self, message):
#         await self.send(text_data=message)


