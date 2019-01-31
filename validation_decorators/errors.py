def log_error(msg, func_name, logger):
    logger.log.error('error in %s: %s' % (func_name, msg))
    raise Exception('error in %s: %s' % (func_name, msg))

def raise_error(msg, func_name, logger):
    raise Exception('error in %s: %s' % (func_name, msg))

def ignore_error(msg, func_name, logger):
    pass
