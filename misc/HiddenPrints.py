import os, sys

class HiddenPrints:
    '''
    Class to hide prints when debugging. Helps avoid clutter.

    Ex:
    with HiddenPrints():
        function_that_prints()
    '''
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout