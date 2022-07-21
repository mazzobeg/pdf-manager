class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def progressBar(progress, total) :
    percent = int(100 * (progress/float(total)))
    bar = bcolors.OKGREEN + '<' + '-' * percent + '>' +  bcolors.ENDC + '-' * (100-int(percent))
    print(f'\rIn translation … {bar} {bcolors.OKGREEN}{percent:.2f}%{bcolors.ENDC}', end = '')