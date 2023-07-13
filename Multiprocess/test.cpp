#include <iostream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    int pipefd[2]; // 管道文件描述符数组
    char message[] = "Hello from child process!"; // 子进程要传递的字符流
    int number = 123; // 子进程要传递的变量

    // 创建管道
    if (pipe(pipefd) == -1) {
        perror("pipe");
        return 1;
    }

    pid_t pid = fork(); // 创建子进程

    if (pid == -1) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // 子进程代码
        close(pipefd[0]); // 关闭子进程的读取端

        // 写入字符流到管道
        write(pipefd[1], message, sizeof(message));
        // 写入变量到管道
        write(pipefd[1], &number, sizeof(number));

        close(pipefd[1]); // 关闭写入端
        return 0;
    } else {
        // 父进程代码
        close(pipefd[1]); // 关闭父进程的写入端

        // 读取子进程传递的字符流
        char receivedMessage[100];
        read(pipefd[0], receivedMessage, sizeof(receivedMessage));
        std::cout << "Received message from child: " << receivedMessage << std::endl;

        // 读取子进程传递的变量
        int receivedNumber;
        read(pipefd[0], &receivedNumber, sizeof(receivedNumber));
        std::cout << "Received number from child: " << receivedNumber << std::endl;

        close(pipefd[0]); // 关闭读取端

        // 等待子进程结束
        int status;
        waitpid(pid, &status, 0);
        return 0;
    }
}
