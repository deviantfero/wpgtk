import logging

log = logging.getLogger("wpgtk")
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(name)s][%(levelname)s] %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)
