from parsehh import *
from graph import *
from dbmigrations import *
import logging
import os.path

def check_image(vacancy):
    if os.path.exists(f'images/{vacancy}.png') :
        logging.info("there is a photo")
    else:
        logging.info("there is no photo")


def final_test(vacancy):
    if check_vacancy(vacancy):
        logging.warning("we already have data in bd, just making graph")
        listof_avg_vacancy = get_vacancy_salary(vacancy)
        create_graph(listof_avg_vacancy, vacancy)
    else:
        logging.warning("its time to parse")
        parsehh(vacancy)
        logging.warning("we parsed, now make graph")
        listof_avg_vacancy = get_vacancy_salary(vacancy)
        create_graph(listof_avg_vacancy,vacancy)