import subprocess


# 控制台实时输出
def consoleOutput_dec(func):
    def temp(*args, **kwargs):
        command = func(*args, **kwargs)
        assert type(command) is str, f'{consoleOutput_dec.__name__} 方法返回为字符串命令!'
        print('command:', command)
        # 使用 subprocess 模块执行命令，并实时获取输出
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # 实时获取输出
        for line in process.stdout:
            print(line, end='')  # 实时打印输出
        # 等待命令执行完成
        process.wait()

    return temp
