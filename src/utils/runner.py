import importlib
import sys
import subprocess
import logging


def import_class_from_string(class_string):
    """
    Import (and return) a class from its name

    Arguments keywords:
    class_string -- name of class to import
    """
    module_name, class_name = class_string.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def run_command(command, encoding=sys.stdout.encoding):
    """
    Execute the given command in a shell

    Argument keywords
    command -- command to execute
    encoding -- encoding to use

    Return
    False if error
    True if OK but no output from command
    Command output if there is one
    """
    try:
        # encode command properly for subprocess
        command_bytes = command.encode(encoding)
        # run command and log output
        proc = subprocess.run(command_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
        logging.debug("{} => {}".format(command, proc.stdout))
        # return output if got any, True otherwise
        if proc.stdout:
            # Second parameter "ignore" has been added because some plugins have 'strange' characters in their
            # name so 'decode' is failing and exits the script. Adding "ignore" as parameter prevent script from
            # exiting.
            text = proc.stdout.decode(encoding, "ignore")
            # get rid of final spaces, line return
            logging.debug(text.strip())
            return text.strip()
        return True

    except subprocess.CalledProcessError as err:
        # log error with content of stderr
        logging.error("command failed (code {}) with error <{}> => {}".format(
                        err.returncode,
                        err,
                        err.stderr))
        return False
