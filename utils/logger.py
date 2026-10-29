def log_result(message, _pass = True, critical=False):
    """
    Logs the result of a test case.

    Args:
        message (str): The message to log.
        pass (bool): Whether the test case passed or failed. Defaults to True.
        critical (bool): Whether the log is critical. Defaults to False.
    """
    if _pass:
        print(f"[PASS] {message}")
    else:
        if critical:
            print(f"[CRITICAL] [FAIL] {message}")
        else:
            print(f"[FAIL] {message}")

def log_info(message):
    """
    Logs an informational message.

    Args:
        message (str): The message to log.
    """
    print(f"[INFO] {message}")

def log_warning(message):
    """
    Logs a warning message.

    Args:
        message (str): The message to log.
    """
    print(f"[WARNING] {message}")

def log_error(message):
    """
    Logs an error message.

    Args:
        message (str): The message to log.
    """
    print(f"[ERROR] {message}")