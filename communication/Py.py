import os

# 从环境变量 PIPE_FD 中获取管道的写入端文件描述符
pipe_fd = int(os.getenv("PIPE_FD"))

# 向管道写入数据
data = "Hello, C++!"
os.write(pipe_fd, data.encode())
