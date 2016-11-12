from ConfigParser import SafeConfigParser

def parse_ini():
    parser = SafeConfigParser()
    parser.read('model.ini')
    pass