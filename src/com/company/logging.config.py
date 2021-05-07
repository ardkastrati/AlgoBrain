import logging
logging.basicConfig(filename = 'logging.config', level = logging.INFO, format='%')
logger = logging.getLogger('Organism_Evolution')
loger.setLevel(logging.DEBUG)

#console Handler:
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

#create formatter:
formatter =
