"""
Utils file for helper function.
"""
import logging
import csv
# Get an instance of a logger
logger = logging.getLogger(__name__)


def flat_tree_from_csv(file_name):
    """ Generates a flat tree <list> of the provided csv path. """
    try:
        with open(file_name) as file:
            spamreader = csv.reader(file, delimiter='"', quotechar='|')
            tree = []
            for row in spamreader:
                columns = row[0].split(',')
                for col in columns:
                    # In case the csv file has many columns, finds out the index of
                    # Category
                    if col == 'Category':
                        category_index = columns.index(col)
                        break
                tree.append(columns[category_index].split(' / '))
            return tree
    except Exception as e:
        print(e)
        logger.error(e)


def is_in(path, tree):
    """ Given  args:
        path<list>: ['Category 2', 'Category 3']
        tree<list>: [
            ['Category 1', 'Category 2', 'Category 3'],
            ['Category 4', 'Category 5', 'Category 6'],
        ]
        This function will check if the given path is inside the given tree.
    """
    for row in tree:
        step = len(path)
        this_range = reversed(range(0, len(row)))
        for i in this_range:
            slice = row[i:i+step]
            if ','.join(path) in ','.join(slice):
                return True
    return False


def try_catch_index(listinstance, indexes, default=None):
    for i in indexes:
        try:
            listinstance = listinstance.copy()[i]
        except Exception as e:
            return default
    return listinstance
