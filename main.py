import getopt, sys, json
import logging

import multiple_downloader
import single_downloader

logging.basicConfig(filename='downloader.log',filemode='a', format='%(levelname)s : %(asctime)s : %(message)s',level=logging.DEBUG)

def usage():
    """ Print usage documentation
    """
    logging.info('Wrongly typed command')
    print("-----------------------------------------------------------------------")
    print("Wrongly typed command. Sample usage is given below")
    print("python ",sys.argv[0],"--config=<config file location>")
    print("-----------------------------------------------------------------------")

def getCommands(args):
    """ Get command line values from args

    Parameters:
    args -- command line arguments
    Returns:
    Object with key valur pairs
    """
    commands = {'config':''}
    try:
        optlist, args = getopt.getopt(args,'',['config='])
        for k, v in optlist:
            if k=='--config':
                commands['config'] = v
    except getopt.GetoptError:
        usage()
        #sys.exit(2)
    return commands

def getUrlSources(urlFile):
    """ Get iterable of urls

    Parameters:
    urlFile -- file path containing urls
    Returns:
    Iterable of urls
    """
    return [url for url in open(urlFile, "r")]

def main():
    """ Main method that starts multi downloading
    """
    commands = getCommands(sys.argv[1:])
    try:
        with open(commands['config'], "r") as f:
            config = json.load(f)
            multiple_downloader.download(getUrlSources(config["input"]), single_downloader.download, config["destination"])
    except Exception as e:
        logging.exception(e)

if __name__ == '__main__':
    main()
