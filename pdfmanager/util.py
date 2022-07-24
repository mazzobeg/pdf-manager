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

class Progressor :
    def __init__(self, total:int, progress:int = 0) -> None:
        self.progress = progress
        self.total = total
    
    def increment(self, n = 1) :
        self.progress += n

    def display(self) :
        percent = int(100 * (self.progress/float(self.total)))
        bar = '🟩' * int(percent/10) + '⬜️' * int((100-int(percent))/10)
        print(f'\r[pdfmanager] {bar} {bcolors.OKGREEN}{percent:.2f}%{bcolors.ENDC}', end = '')

def lineReturnedString(longstring, charwidth, totalwidth) :
    intervall = int(totalwidth/charwidth)
    return '\n'.join([longstring[i*intervall:i*intervall+intervall] for i in range(len(longstring)%intervall)])

