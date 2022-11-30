from subprocess import *
import getopt, sys, os, signal, time
subtask = [[] for i in range(5)]
subtask[1] = [[3, 4, 5, -1], [2, 10, 18, -1], [4, 1, 13, -1], [1, 7, 24, -1], [100, 3, 13, -1]]
subtask[2] = [[3, 1, 17, -1], [2, 14, 64, -1], [4, 19, 24, -1], [1, 12, 13, -1], [100, 9, 33, -1]]
subtask[3] = [[3, 9, 7, 12], [2, 10, 18, 9], [4, -1, 2, 15], [1, 17, -1, 11], [100, 7, 14, 8]]

options = ["main.c", "scheduler.c", "threads.c", "threadtools.h"]

def rnd(x, up) :
    x = (x + 2.473) * 5.678
    x = x - (x // up * up)
    return x

def nxt(n) :
    if n % 3 == 0:
        n = -n
    n = n * 2473 + 5678
    if n < 0:
        n = n % -1000
    else:
        n = n % 1000
    return n

def tostr(n) :
    str_n = str(n)
    str_n = " " * (4 - len(str_n)) + str_n + "\n"
    return str_n

def single_task(subtask_num, idx, task) :
    task_arg = " ".join(map(str, task))
    command = "./main " + task_arg
    output_path = "test_result/{}-{}.out".format(subtask_num, idx)
    answer_path = os.path.abspath(os.path.dirname(__file__)) + "/test_result/{}-{}.ans".format(subtask_num, idx)
    os.system("cp " + answer_path + " test_result")
    f = open(output_path, "w+")
    process = Popen(command, shell = True, stdout = f)
    
    if subtask_num == 3:
        try:
            os.mkfifo("2_max_subarray")
        except:
            pass
        fifo = open("2_max_subarray", "w")
    
    fifo_num = task[-1]
    if fifo_num < 0:
        fifo_num = 0
    n = task[0] * 5 - task[1] * 3 - task[2] * 4 + task[3] * -6
    
    if subtask_num >= 2:
        x = subtask_num * 6 + idx
        while process.poll() is None:
            x = rnd(x, 1)
            if x > 0.5:
                time.sleep(x)
                process.send_signal(signal.SIGTSTP)
            x = rnd(x, 2)
            time.sleep(x)
            if fifo_num > 0:
                fifo_num -= 1
                n = nxt(n)
                str_n = tostr(n)
                fifo.write(str_n)
                fifo.flush()
                
    process.wait()
    print("Test {}-{} : ".format(subtask_num, idx), end = '')
    diff_process = Popen("diff {} {}".format(output_path, answer_path), shell = True)
    code = diff_process.wait()
    if subtask_num == 3:
        fifo.close()
    if code == 0:
        print("Accepted")
    else:
        print("Wrong Answer")

def run_subtask(x):
    print("Running Subtask {}".format(x))
    for idx, task in enumerate(subtask[x]):
        single_task(x, idx + 1, task)

def compile_replace_file(x):
    gen = Popen("python " + os.system(os.path.abspath(os.path.dirname(__file__)) + "/compile.py {}".format(x)))

try:
    optlist, args = getopt.getopt(sys.argv[1:], '-t')
    args = [int(i) for i in args]
except:
    print("see README.md in the same directory for usage")
    exit(0)

for i, j in optlist:
    if i == '-t':
        if j not in options:
            print("Please specify which file to replace.")
            exit(0)
        compile_replace_file(j)

os.system("rm -rf test_result")
os.system("mkdir test_result")

for i in range(1, 4):
    if i in args:
        run_subtask(i)

if len(args) == 0:
    print("see README.md in the same directory for usage")

