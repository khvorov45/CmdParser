# Command line parsing

 Reads command line input of the form:

 ~~~
python path/to/script.py args -o option1 -i option2
 ~~~

and returns a dictionary of options and a list of non-options.

Should be initialised with command line arguments (list of strings) and 
an option dictionary of the form 
`{option_indicator: [option_name, option_fun]}`. See `generaltest.py` for
an example.
