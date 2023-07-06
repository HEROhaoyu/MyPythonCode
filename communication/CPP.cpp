#include <iostream>
#include <unistd.h>
#include <cstdlib>
#include <sys/wait.h>

// 执行 Python 程序的逻辑
void executePythonProgram(int pipe_fd) {
    // 将子进程的标准输出重定向到管道
    dup2(pipe_fd, STDOUT_FILENO);

    // 设置环境变量 PIPE_FD
    std::string pipe_fd_str = std::to_string(pipe_fd);
    setenv("PIPE_FD", pipe_fd_str.c_str(), 1);

    // 执行 Python 程序
    execlp("python", "python", "Py.py", nullptr);
    exit(1);
}

// 从管道读取数据
std::string readFromPipe(int pipe_fd) {
    char buffer[256];
    ssize_t bytes_read = read(pipe_fd, buffer, sizeof(buffer) - 1);
    if (bytes_read == -1) {
        std::cerr << "Error reading from pipe" << std::endl;
        exit(1);
    }

    buffer[bytes_read] = '\0';
    return buffer;
}

int main() {
    int pipe_fds[2];

    // 创建管道
    if (pipe(pipe_fds) == -1) {
        std::cerr << "Error creating pipe" << std::endl;
        return 1;
    }

    // 创建子进程
    pid_t pid = fork();
    if (pid == -1) {
        std::cerr << "Error forking process" << std::endl;
        return 1;
    }

    if (pid == 0) {
        // 子进程中执行 Python 程序
        close(pipe_fds[0]);  // 关闭读取端
        executePythonProgram(pipe_fds[1]);
    } else {
        // 父进程中等待子进程退出
        waitpid(pid, nullptr, 0);

        // 关闭管道的写入端
        close(pipe_fds[1]);

        // 读取子进程输出
        std::string pythonOutput = readFromPipe(pipe_fds[0]);
        std::cout << "Received data from Python: " << pythonOutput << std::endl;
    }

    return 0;
}
