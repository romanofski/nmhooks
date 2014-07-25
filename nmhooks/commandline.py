#!/usr/bin/env python
import notmuch
import re
import logging
import argparse
import ConfigParser
import time
import nmhooks


logging.basicConfig(level=logging.DEBUG)


def parse_rules(fp):
    parser = ConfigParser.ConfigParser()
    parser.readfp(fp)
    return parser


def construct_query(db, query):
    return notmuch.Query(db, query)


def construct_tag_mapping(tags):
    """
    Returns a list of tuples in order to apply the tags:

        tag, method

    This allows to apply all tags by calling the provided Message
    method, which is either 'add_tag' or 'remove_tag'.

    At the moment, the api does not provide any merge operations of
    tags.
    """
    mapping = {'+': 'add_tag',
               '-': 'remove_tag'}
    tags = [(t[1:], mapping.get(t[0])) for t in tags.split(' ')]
    return filter(lambda x: x[1] is not None, tags)


def apply_rules(cparser, db):
    """
    Applies rules defined by the configfile parsed by cparser to the
    messages in the db.

    Returns the amount of messages which have been changed.
    """
    counter = 0
    for section in cparser.sections():
        query = construct_query(db, cparser.get(section, 'query'))
        hcontents = re.compile(cparser.get(section, 'match'))
        tag_mapping = construct_tag_mapping(cparser.get(section, 'apply'))
        logging.info("Found {0} mails for query: {1}".format(
            query.count_messages(), cparser.get(section, 'query')))

        for msg in query.search_messages():
            header = msg.get_header(cparser.get(section, 'header'))
            if not header:
                logging.debug('Header `{header}` not found on: {msg}'.format(
                    header=cparser.get(section, 'header'), msg=msg))
                continue

            if hcontents.search(header):
                msg.freeze()
                [getattr(msg, attr)(tag) for tag, attr in tag_mapping]
                logging.info('Applied {0} on {1}'.format(
                    cparser.get(section, 'apply'), msg))
                msg.thaw()
                counter += 1
            else:
                logging.debug('{header} did not match re: {re}'.format(
                    header=header, re=hcontents.re.pattern))
    return counter


def _setup_commandline_arguments():
    """ Helper method to setup arguments and argument parser. """
    parser = argparse.ArgumentParser(
        description='{name} {version} -- {description}'.format(
            name=nmhooks.__name__, version=nmhooks.__version__,
            description=nmhooks.__description__))
    parser.add_argument(
        "configfile",
        help='Path to configuration file',
        type=str)
    parser.add_argument(
        "-v",
        "--verbose",
        dest='verbose',
        help=("Increase logging verbosity to DEBUG"),
        action="store_true")
    parser.add_argument(
        "--version",
        action="version",
        version="{name} {version}".format(
            name=nmhooks.__name__, version=nmhooks.__version__),)
    return parser.parse_args()


def postnew():
    options = _setup_commandline_arguments()
    start = time.time()
    db = notmuch.Database(mode=notmuch.Database.MODE.READ_WRITE)
    with open(options.configfile, 'r') as f:
        cparser = parse_rules(f)
    msg_count = apply_rules(cparser, db)
    end = time.time()
    logging.info('Changed {msgcount} in {proctime} seconds'.format(
        msgcount=msg_count, proctime=end - start))
