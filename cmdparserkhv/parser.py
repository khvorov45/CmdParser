"""Parsing command line input"""

from colorama import init, Fore

init(autoreset=True)

class CmdParser:
    """Parses command line input. Expects it unmodified.

    Arguments:
        system_arguments: a list of strings. Expected to be unmodified
            command line input
        opt_dic: a dictionary of options of the structure:
            indicator : [name, Cmdend(name, allowed)]
            Where name is the option name and allowed is a list, a range or
            None. If None, option is assumed to be boolean.
    """
    # pylint: disable=attribute-defined-outside-init
    # I'm using setters/getters here, those attributes in init would look messy
    def __init__(self, args, opt_dic):
        self.args = args
        self.opt_dic = opt_dic
        self._unprocessed = args[1:] # 0 is script name
        self._parsed = {}
        self._is_parsed = False

    @property
    def args(self):
        """Unmodified command line arguments"""
        self._is_parsed = False
        return self._args

    @args.setter
    def args(self, new_args):
        if not isinstance(new_args, list):
            raise TypeError
        self._args = new_args

    @property
    def opt_dic(self):
        """Options dictionary"""
        self._is_parsed = False
        return self._opt_dic

    @opt_dic.setter
    def opt_dic(self, new_dic):
        if not isinstance(new_dic, dict):
            raise TypeError
        self._opt_dic = new_dic

    def parse(self):
        """Parses the unprocessed options according to the dictionary"""

        opd = self.opt_dic
        args = self._unprocessed
        new_unprocessed = []
        skip_next = False
        for i, arg in enumerate(args):
            if skip_next:
                skip_next = False
                continue
            if arg in opd.keys():
                opt = opd[arg]
                if opt.is_bool():
                    self._parsed.update({opt.name: True})
                    continue
                try:
                    next_arg = args[i + 1]
                    if next_arg in opd.keys():
                        raise IndexError
                except IndexError:
                    raise Exception("expected option after " + arg)
                skip_next = True
                self._parsed.update({opt.name: opt.process(next_arg)})
            else:
                new_unprocessed.append(arg)
        self._unprocessed = new_unprocessed
        self._is_parsed = True

    def get_all_options(self):
        """Returns all options as per the dictionary"""
        if not self._is_parsed:
            self.parse()
        all_opts = self._parsed
        for opt in self.opt_dic.values():
            if opt.name in self._parsed.keys():
                continue
            if opt.is_bool():
                all_opts.update({opt.name: False})
                continue
            all_opts.update({opt.name: opt.get_def()})
        return all_opts

    def get_unrecognised(self):
        """Returns everything that's not recognised as an option"""
        if not self._is_parsed:
            self.parse()
        return self._unprocessed

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

    @property
    def name(self):
        """Option name"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def allowed(self):
        """Allowed choices"""
        return self._allowed

    @allowed.setter
    def allowed(self, allowed):
        is_none = allowed is None
        is_list = isinstance(allowed, list)
        is_range = isinstance(allowed, range)
        if not is_none | is_list | is_range:
            raise Exception("allowed should be a list, range or None")
        self._allowed = allowed

    def is_bool(self):
        """Returns boolean status"""
        return self.allowed is None

    def get_def(self):
        """Returns the default value"""
        if self.is_bool():
            return False
        return self.allowed[0]

    def process(self, arg):
        """Processes the argument"""
        arg = self._pre_process(arg)
        if arg not in self.allowed:
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
