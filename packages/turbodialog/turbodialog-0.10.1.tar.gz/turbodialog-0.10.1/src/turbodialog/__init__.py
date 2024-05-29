import turboconf


class TurboDialogMinimal:


    def __init__(self, conf) -> None:
        self._conf = conf


    def box(self, m) -> str:
        """Draw a box around some text.
        """
        res = ""
        lines = m.split("\n")
        lmax = 0
        for l in lines:
            if len(l) > lmax:
                lmax = len(l)
        w = lmax+4
        res+="\n"
        
        res+=" " + "-"*w
        res+="\n"
        
        l: str
        for l in lines:
            res+="|  %s  |" % l.ljust(lmax)
            res+="\n"
        res+=" " + "-"*w
        res+="\n"
        res+="\n"
        return res


    def msg(self, m, t=None):
        # lines = m.split("\n")
        # lmax = 0
        # for l in lines:
        #     if len(l) > lmax:
        #         lmax = len(l)
        # w = lmax+4
        # print()
        # print(" " + "-"*w)
        # l: str
        # for l in lines:
        #     print("|  %s  |" % l.ljust(lmax))
        # print(" " + "-"*w)
        # print()
        print(self.box(m), end=None)
        self._input()


    def _input(self, info=''):
        if info != '':
            return input(info)
        return input("PRESS RETURN TO CONTINUE OR CTRL-C TO ABORT")


    def msg64(self, m:str, t=None):
        return None


    def yes_no(self, q, t=None):
        return None


    def one_of(self, opts:dict, t=None, callback_f:callable=None, repeat_selection:bool=False) -> str|None:
        sorted_keys = sorted(opts.keys())
        lines = [ "[%d:%s]  %s" % (sorted_keys.index(x)+1, x, opts[x]) for x in sorted_keys]
        sel=0
        while True:
            print("\n"*10)
            print(self.box("Please select:"))
            for i in range(0, len(lines)):
                marker_string1 = "    "
                marker_string2 = "    "
                if sel == i:
                    marker_string1 = " >> "
                    marker_string2 = " << "
                print("  %s%s%s" % (marker_string1, lines[i], marker_string2))
            print()
            in_ = self._input("RETURN=select-next  s=select-and-proceed  q=quit-selection ")
            if in_ == '':
                sel = (sel + 1) % len(lines)
            if in_ == 's' or in_ == ' ':
                if callback_f != None:
                    callback_f(sorted_keys[sel])
                if repeat_selection == False:
                    return sorted_keys[sel]
            if in_ == 'q':
                return None


    def index_of(self, lines:list, t=None) -> int:
        #sorted_keys = sorted(opts.keys())
        #lines = [ "[%d:%s]  %s" % (sorted_keys.index(x)+1, x, opts[x]) for x in sorted_keys]
        sel=0
        while True:
            print("\n"*10)
            print(self.box("Please select:"))
            for i in range(0, len(lines)):
                marker_string1 = "    "
                marker_string2 = "    "
                if sel == i:
                    marker_string1 = " >> "
                    marker_string2 = " << "
                print("  %s%s%s" % (marker_string1, lines[i], marker_string2))
            print()
            in_ = self._input("RETURN=select-next  s=select-and-proceed  q=quit-selection ")
            if in_ == '':
                sel = (sel + 1) % len(lines)
            if in_ == 's' or in_ == ' ':
                return sel
            if in_ == 'q':
                return -1


class TurboDialogDialog(TurboDialogMinimal):


    def __init__(self, conf) -> None:
        super().__init__(conf=conf)


def TurboDialog():
    conf = turboconf.load_conf(None)
    if conf['os'] in 'lm':
        return TurboDialogMinimal(conf)
    if conf['os'] == 'w':
        return TurboDialogMinimal(conf)
    if conf['os'] == 'unknown':
        return TurboDialogMinimal(conf)
