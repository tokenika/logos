import re
import sys

import eosfactory.core.logger as logger
import eosfactory.core.interface as interface


def validate_command_result(omittable):
    """Throw exception if validation fails.
    """
    err_msg = omittable.err_msg
    if not err_msg:
        return

    if "unknown key" in err_msg:
        raise AccountDoesNotExistError(omittable)
    elif "Error 3080001: Account using more than allotted RAM" in err_msg \
                                or "has insufficient ram; needs" in err_msg:
        needs = int(re.search(r'needs\s(.*)\sbytes\shas', err_msg).group(1))
        has = int(re.search(r'bytes\shas\s(.*)\sbytes', err_msg).group(1))
        raise LowRamError(needs, needs - has)
    elif "transaction executed locally, but may not be" in err_msg:
        pass
    elif "Wallet already exists" in err_msg:
        raise WalletAlreadyExistsError(omittable)
    elif "Error 3120002: Nonexistent wallet" in err_msg:
        raise WalletDoesNotExistError(omittable)
    elif "Invalid wallet password" in err_msg:
        raise InvalidPasswordError(omittable)
    elif "ontract is already running this version of code" in err_msg:
        raise ContractRunningError()
    elif "Missing required authority" in err_msg \
                                        or "missing authority of" in err_msg:
        raise MissingRequiredAuthorityError(err_msg)
    elif "Duplicate transaction" in err_msg:
        raise DuplicateTransactionError(err_msg)
    elif "is nodeos running?" in err_msg \
            or "reason: connect ECONNREFUSED" in err_msg:
        raise IsNodeRunning()
    
    #######################################################################
    # NOT ERRORS
    #######################################################################
    
    elif "Error 3120008: Key already exists" in err_msg:
        pass                
    else:
        raise Error(err_msg)


def excepthook(exc_type, value, traceback):
    print(value)


class Error(Exception):
    """Base class for exceptions in EOSFactory.
    """
    def __init__(
            self, message, translate=True):
        if not message:
            message = "no message"
        self.message = logger.error(message, translate)
        Exception.__init__(self, self.message)


class UserError(Error):
    """User error as a missing argument, for example.
    """
    def __init__(self, message):
        Error.__init__(self, message)


class InterfaceError(UserError):
    def __init__(self, message):
        UserError.__init__(self, message)


class ArgumentNotSet(UserError):
    """Missing argument error.
    """
    def __init__(
            self, argument_name=None, argument_definition=None, message=None):

        message = message if message else """
The argument ``{}``,
which is {}, has to be set.
        """.format(argument_name, argument_definition)
        UserError.__init__(self, message) if argument_definition else """
The argument ``{}`` has to be set.
        """.format(argument_name)
        UserError.__init__(self, message)


class TypeError(UserError):
    """Wrong type error.
    """
    def __init__(self, argument_name, argument_type, expected_type):
         UserError.__init__(self, """
The type of argument ``{}`` is ``{}`` 
while it is expected to be ``{}``.
         """.format(argument_name, argument_type, expected_type))


class IsNodeRunning(Error):
    def __init__(self):
        Error.__init__(self, "Node does not response.", False)

class AccountDoesNotExistError(Error):
    """Account does not exist.

    Attributes:
        account: account argument: an ``Account`` object or account name.
    """
    def __init__(self, account):
        self.account = account
        Error.__init__(
            self, 
            "Account ``{}`` does not exist in the blockchain."
            .format(interface.account_arg(account)), 
            True)


class WalletDoesNotExistError(Error):
    def __init__(self, wallet):
        Error.__init__(
            self, 
            "Wallet ``{}`` does not exist."
            .format(interface.wallet_arg(wallet)), 
            True)


class WalletAlreadyExistsError(Error):
    def __init__(self, wallet):
        Error.__init__(
            self, 
            "Wallet ``{}`` already exists."
            .format(interface.wallet_arg(wallet)), 
            True)


class InvalidPasswordError(Error):
    def __init__(self, wallet):
        Error.__init__(
            self, 
            "Invalid password for wallet {}"
            .format(interface.wallet_arg(wallet)),
            True)


class ContractRunningError(Error):
    def __init__(self):
        Error.__init__(
            self, 
            "Contract is already running this version of code", 
            True)


class LowRamError(Error):
    def __init__(self, needs_byte, deficiency_byte):
        self.needs_kbyte =  needs_byte// 1024 + 1
        self.deficiency_kbyte = deficiency_byte // 1024 + 1
        Error.__init__(
            self, 
            "RAM needed is {}kB, deficiency is {}kB."
            .format(self.needs_kbyte, self.deficiency_kbyte), 
            True)   


class MissingRequiredAuthorityError(Error):
    def __init__(self, message):
        Error.__init__(
            self, message, True)


class DuplicateTransactionError(Error):
    def __init__(self, message):
        Error.__init__(
            self, message, True)