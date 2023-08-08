import subprocess
import os, sys
import re
import time


def run(filename):
    pwd = os.path.dirname(os.path.realpath(__file__)) + '/codepath/'
    codepath = pwd + '/' + filename
    execpath = pwd + '/bin/' + filename + '.out'
    input_filepath = pwd + '/in'
    output_filepath = pwd + '/out'
    tl = 100

    input_file = open(input_filepath, "r")
    output_file = open(output_filepath, "w")

    if re.search("\.java$", filename):
        # 正则表达式，表示以.java结尾的字符串
        classname = re.sub(r'\.java$', '', filename)
        # Compile the java file
        T1 = time.time()
        a = subprocess.call(['javac', codepath, '-d', pwd + '/bin/'])
        if a != 0:
            output_file.write('java编译失败' + str(a))
            sys.exit(-1)
        T2 = time.time()
        # Run the java file and capture the output
        try:
            output = subprocess.check_output(
                ['java', '-classpath', pwd + '/bin', classname])
            T3 = time.time()
        except subprocess.CalledProcessError:
            sys.exit(-1)

    elif re.search("\.c$", filename):
        T1 = time.time()
        a = subprocess.call(['cc', codepath, '-o', execpath], cwd=pwd)
        if a != 0:
            output_file.write('C编译失败' + str(a))
            sys.exit(-1)
        T2 = time.time()
        # Run the java file and capture the output
        output = subprocess.check_output(execpath, stdin=input_file, cwd=pwd)
        T3 = time.time()
    # Decode the output to a normal string
    output = output.decode('utf-8')

    # print(output)
    output_file.write(output)
    print('编译时间 %s毫秒' % ((T2 - T1) * 1000))
    print('程序运行时间 %s毫秒' % ((T3 - T2) * 1000))

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    run('Hello.c')
