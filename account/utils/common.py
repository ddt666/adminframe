import random


def get_random_int(digits=6):
    random_num = []
    for i in range(digits):
        random_num.append(str(random.randint(0, 9)))

    return "".join(random_num)


if __name__ == '__main__':
    print(get_random_int())
