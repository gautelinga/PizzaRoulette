import random
import csv
import sys
import cPickle as pickle
import time


class PizzaMenu:
    def __init__(self, filename):
        self.pizzas = dict()
        with open(filename) as pizza_menu_file:
            reader = csv.DictReader(pizza_menu_file, delimiter='\t')
            for row in reader:
                self.pizzas[int(row['id'])] = dict(name=row['name'],
                                                   price=row['price'])

    def list_untested_pizzas(self, eaten):
        return list(set(self.pizzas.keys()) - eaten)

    def choose_random_pizza(self, eaten):
        untested_pizzas = self.list_untested_pizzas(eaten)
        pizza = random.choice(untested_pizzas)
        return pizza

    def query_add(self, eaten, pizza, have_a_choice=False):
        if not have_a_choice or \
           query_yes_no("Do you want to eat this pizza?") == "yes":
            eaten.add(pizza)
            return True
        return False


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": "yes", "y": "yes", "ye": "yes",
             "no": "no", "n": "no"}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def list2str(myList):
    return ", ".join(str(p) for p in sorted(myList))


def main():
    pizza_menu_file = "pizza_menu.dat"
    eaten_file = "eaten.dat"

    pizza_menu = PizzaMenu(pizza_menu_file)
    eaten = set(pickle.load(file(eaten_file, "r")))

    print "Welcome to Pizza Roulette!\n"
    print "You have tried these pizzas:", list2str(eaten)

    print "\nBefore you start, call Pizzeria Cavallino at tel. 35 35 14 15.\n"
    keep_eating = (query_yes_no("Ready to roll?") == "yes")

    while keep_eating:
        time.sleep(1)
        pizza = pizza_menu.choose_random_pizza(eaten)
        print "\nYou got pizza no.", pizza
        time.sleep(1)
        pizza_info = pizza_menu.pizzas[pizza]
        print "\nThis pizza is called '" + str(pizza_info['name']) + \
            "' and it costs DKK " + str(pizza_info['price'])

        if pizza_menu.query_add(eaten, pizza):
            question = "Eat another one?"
            keep_eating = (query_yes_no(question) == "yes")

    print "\nThanks for playing Pizza Roulette!\n"
    print "You have now eaten these pizzas:", list2str(eaten)
            
    pickle.dump(list(eaten), file(eaten_file, "w"))

if __name__ == "__main__":
    main()
