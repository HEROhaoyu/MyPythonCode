#include <iostream>
#include <sstream>
#include <unistd.h>
#include <cstdlib>
#include <sys/wait.h>
#include <fcntl.h>
#include <fstream>
#include <string>


std::string read_data_from_pipe(int pipe_fd) {
    std::stringstream ss;

    char buffer[1024];
    ssize_t bytes_read;

    while (true) {
        // 设置管道为非阻塞模式
        int flags = fcntl(pipe_fd, F_GETFL);
        fcntl(pipe_fd, F_SETFL, flags | O_NONBLOCK);

        // 尝试读取管道数据
        bytes_read = read(pipe_fd, buffer, sizeof(buffer));

        if (bytes_read == -1) {
            if (errno == EWOULDBLOCK || errno == EAGAIN) {
                // 管道没有数据可读，跳出循环
                break;
            } else {
                // 其他读取错误
                std::cerr << "Error reading from pipe" << std::endl;
                exit(1);
            }
        } else if (bytes_read == 0) {
            // 读取到管道末尾，结束读取
            break;
        }

        // 将读取到的数据写入字符串流
        ss.write(buffer, bytes_read);
    }

    return ss.str();
}

void write_dict_to_file(const std::string& filename, const std::string& jsonData) {
    std::ofstream file(filename);
    if (!file) {
        std::cerr << "Error opening file: " << filename << std::endl;
        exit(1);
    }

    file << jsonData;

    file.close();
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

        // 设置环境变量 PIPE_FD
        std::string pipe_fd_str = std::to_string(pipe_fds[1]);
        setenv("PIPE_FD", pipe_fd_str.c_str(), 1);

        // 执行 Python 程序
        execlp("python3", "python", "PY.py", nullptr);
        exit(1);
    } else {
        // 关闭管道写入端
        close(pipe_fds[1]);

        // 读取数据长度和分块长度
        char length_buffer[16];
        ssize_t bytes_read = read(pipe_fds[0], length_buffer, sizeof(length_buffer));
        if (bytes_read == -1) {
            std::cerr << "Error reading from pipe" << std::endl;
            return 1;
        }
        length_buffer[bytes_read] = '\0';
        int data_length = std::stoi(length_buffer);
        std::cout << data_length << std::endl;
        // std::cout << length_buffer << std::endl;

        char chunk_size_buffer[16];
        bytes_read = read(pipe_fds[0], chunk_size_buffer, sizeof(chunk_size_buffer));
        if (bytes_read == -1) {
            std::cerr << "Error reading from pipe" << std::endl;
            return 1;
        }
        chunk_size_buffer[bytes_read] = '\0';
        int chunk_size = std::stoi(chunk_size_buffer);
        std::cout << chunk_size << std::endl;
        // std::cout << chunk_size_buffer << std::endl;
        // 读取数据
        std::string data;
        char data_buffer[chunk_size];
        while (data.length() < data_length) {
            bytes_read = read(pipe_fds[0], data_buffer, sizeof(data_buffer));
            if (bytes_read == -1) {
                std::cerr << "Error reading from pipe" << std::endl;
                return 1;
            }
            data.append(data_buffer, bytes_read);
        }

        // 关闭管道读取端
        close(pipe_fds[0]);

        // 等待子进程退出
        waitpid(pid, nullptr, 0);

        // 输出接收到的数据
        // std::cout << data << std::endl;

        // 将接收到的数据写入文件
        write_dict_to_file("output.txt", data);

        return 0;
    }
}
