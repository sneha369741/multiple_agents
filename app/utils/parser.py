def classify_log(log):
    if "ERROR" in log:
        return "error"
    elif "WARN" in log:
        return "warning"
    else:
        return "info"
