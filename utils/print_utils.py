from utils.b_colors import BColors


def progressBar(
            iterable,
            prefix = '',
            suffix = '',
            decimals = 1,
            bar_length = 50,
            fill = f'{BColors.OKGREEN}█{BColors.ENDC}',
            printEnd = "\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : iterable object (Iterable)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        total = len(iterable)
        # Progress bar printing function
        def printProgressBar(iteration):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(bar_length * iteration //total)

            bar = fill * filledLength + '-' * (bar_length - filledLength)
            print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        
        # initial call:
        printProgressBar(0)

        # update ProgressBar
        for i, item in enumerate(iterable):
            yield i, item
            printProgressBar(i+1)
        # print newline on Complete
        print(flush=True)