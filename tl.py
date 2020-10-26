import logging, sys


a_logger = logging.getLogger()

a_logger.setLevel(logging.DEBUG)


output_file_handler = logging.FileHandler("output.log")

stdout_handler = logging.StreamHandler(sys.stdout)


a_logger.addHandler(output_file_handler)

a_logger.addHandler(stdout_handler)



for i in range(1, 4):

    a_logger.debug("This is line " + str(i))
