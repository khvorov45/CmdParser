"""Parsing command line input"""

from colorama import init, Fore

init(autoreset=True)

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
        self._fill_def()

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
                opt = opd[arg]
                opt_name = opt.get_name()
                if opt.is_bool():
                    self.add_opt(opt_name, True)
                    continue
                try:
                    next_arg = opts[i + 1]
                    if next_arg in opd.keys():
                        raise IndexError
                except IndexError:
                    raise Exception("expected option after " + arg)
                skip_next = True
                self.add_opt(opt_name, opt.process(next_arg))
            else:
                new_unprocessed.append(arg)

    def _fill_def(self):
        """Fills in missing defaults"""
        opd = self.get_opt_dic()
        opt_pres = self.get_opts()

        for opt in opd.values():
            opt_name = opt.get_name()
            if opt_name in opt_pres.keys():
                continue
            if opt.is_bool():
                self.add_opt(opt_name, False)
                continue
            self.add_opt(opt_name, opt.get_def())

class Cmdent:
    """Represents one value in the option dictionary

    Arguments:
        name: proper option name.
        allowed: a list with allowed arguments. If None, option is assumed to
            be boolean.
    """
    # pylint: disable=attribute-defined-outside-init
    # I'm using setters/getters here, those attributes in init would look messy
    def __init__(self, name, allowed=None):
        self.name = name
        self.allowed = allowed

    def set_name(self, name):
        """Sets the name"""
        self._name = name

    def get_name(self):
        """Returns the name"""
        return self._name

    name = property(get_name, set_name)

    def set_allowed(self, allowed):
        """Sets allowed values"""
        is_none = allowed is None
        is_list = isinstance(allowed, list)
        is_range = isinstance(allowed, range)
        if not is_none | is_list | is_range:
            raise Exception("allowed should be a list, range or None")
        self._allowed = allowed

    def get_allowed(self):
        """Returns the allowed values"""
        return self._allowed

    allowed = property(get_allowed, set_allowed)

    def is_bool(self):
        """Returns boolean status"""
        return self._allowed is None

    def get_def(self):
        """Returns the default value"""
        if self.is_bool():
            return False
        return self._allowed[0]

    def process(self, arg):
        """Processes the argument"""
        arg = self._pre_process(arg)
        if arg not in self.get_allowed():
            print_yellow("option " + arg + " not recognised, using default")
            return self.get_def()
        return arg

    def _pre_process(self, arg):
        """Converts the argument to the appropriate type"""
        if isinstance(self.allowed, range):
            arg = int(arg)
        return arg

def print_yellow(string):
    """Prints string in yellow"""
    print(Fore.YELLOW + string)
