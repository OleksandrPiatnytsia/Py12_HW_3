import logging
from time import time
from multiprocessing import Pool, cpu_count


def get_entree_division(num):
    result = []

    for k in range(1, num):
        if num % k == 0:
            result.append(k)
            # logging.debug(f" number: {k}")
    # logging.debug(f" number: {i}")
    result.append(num)

    return result


def single_process_performing(lst):
    timestamp = time()

    result = []

    for i in lst:
        result.append(get_entree_division(i))

    logging.debug(f'Single process performing time:  {time() - timestamp}')

    return result


def callback(result):
    logging.debug(f" result: {result}")


def multi_processіng_performing(lst):

    timestamp = time()

    with Pool(cpu_count()) as pool:
        result = pool.map(get_entree_division, lst)
        pool.close()

    logging.debug(f'Multi processing performing time:  {time() - timestamp}')

    return result


def main():
    num_lst = [128, 255, 99999, 10651060]
    print(single_process_performing(num_lst))
    print("\n")
    print(multi_processіng_performing(num_lst))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    main()
    # print(f"CPU: {multiprocessing.cpu_count()}")
