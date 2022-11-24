import argparse
import json
import logging

def config_parser(config_path):
    with open(config_path, 'r') as config_file:
        config = dict()
        lines = config_file.readlines()
        for line in lines:
            line = line.rstrip()
            k, v = line.split(' = ')
            config[k] = v
        return config


def get_config_args():
    logging.info("start parsering config file")
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, dest='config')
    args = parser.parse_args()
    config = config_parser(args.config)
    logging.info("config file parsed successfully")
    return config

