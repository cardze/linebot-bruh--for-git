from .conf import Conf


con = Conf('confs/conf_line_bot_init.json')


def check_pas(input):
    if input == con['password']:
        return True
    else:
        return False


if __name__ == "__main__":
    print(check_pas('cardze is the best'))