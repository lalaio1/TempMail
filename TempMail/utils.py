def log_error(message, log_errors):
    if log_errors:
        with open("error_log.txt", 'a') as file:
            file.write(message + "\n")
    print(message)
