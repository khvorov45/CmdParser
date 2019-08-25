"""Parsing command line input"""

class CmdParser:
    """Parses command line input. Expects it unmodified.

    Arguments:
        system_arguments: a list of strings. Expected to be unmodified
            command line input
        opt_dic: a dictionary of options of the structure:
            indicator : [name, fun]
            Where fun is a function to get the next word. If fun = False,
            the option is assumed to be boolean.
    """
    def __init__(self, system_arguments, opt_dic):
        self._unproc = []
        self.add_unproc(system_arguments[1:]) # Ignore the first
        self._opt_dic = {}
        self.set_opt_dic(opt_dic)
        self._opts = {}
        self._read_opts()

    def get_opts(self):
        """Returns the parsed options"""
        return self._opts.copy()

    def add_opt(self, name, val):
        """Adds an option to the dictionary"""
        self._opts[name] = val

    def remove_opt(self, name):
        """Removes an entry from the optin dictionary"""
        del self._opts[name]

    def get_unproc(self):
        """Returns what's not been processed as an option"""
        return self._unproc.copy()

    def add_unproc(self, arg):
        """Adds an unparsed option"""
        if isinstance(arg, list):
            for onearg in arg:
                self._unproc.append(onearg)
        else:
            self._unproc.append(arg)

    def remove_unproc(self, ind):
        """Removes an unprocessed option by value"""
        self._unproc.remove(ind)

    def set_opt_dic(self, opt_dic):
        """Sets the option dictionary"""
        self._opt_dic = opt_dic

    def get_opt_dic(self):
        """Returns the option dictionary"""
        return self._opt_dic.copy()

    def _read_opts(self):
        """Attempts to read the unprocessed options"""

        opd = self.get_opt_dic()
        opts = self.get_unproc()

        # See what arguments have been provided
        new_unprocessed = []
        skip_next = False
        for i, arg in enumerate(opts):
            if skip_next:
                self.remove_unproc(arg)
                skip_next = False
                continue
            if arg in opd.keys():
                self.remove_unproc(arg)
                opt_name = opd[arg][0]
                opt_fun = opd[arg][1]
                if not opt_fun: # Boolean option
                    self.add_opt(opt_name, True)
                    continue
                # Non-boolean option
                skip_next = True
                self.add_opt(opt_name, opt_fun(opts[i + 1]))
            else:
                new_unprocessed.append(arg)
