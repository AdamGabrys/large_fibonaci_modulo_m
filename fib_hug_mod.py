# Uses python3
# Compute modulo m of n-th Fibonacci number
# Uses Pisano periods to find equivalent Fibonacci number for certain modulo
# time and memory efficient
# compute 10^5 modulo of 10^16 Fibonacci number in less than 1s

import math
import sys


def main():
    input_values = sys.stdin.read()
    fibonacci_number, mod = map(int, input_values.split())
    print(get_n_fibonacci_number_mod_m(fibonacci_number, mod))


def get_n_fibonacci_number_mod_m(n, m):
    pisano_periods_array = get_pisano_periods_array(m)
    equivalent_n = get_equivalent_n(n, m, pisano_periods_array)
    return get_n_fibonacci_number(equivalent_n) % m


def get_pisano_periods_array(m):
    pisano_periods_array = initialize_pisano_periods_array(m)
    fill_pisano_periods_array(pisano_periods_array)
    return pisano_periods_array


def initialize_pisano_periods_array(m):
    pisano_periods_array = [0]*(m+1)
    pisano_periods_array[0:2] = [1, 3, 8]
    return pisano_periods_array


def fill_pisano_periods_array(pisano_periods_array):
    insert_prime_based_periods(pisano_periods_array)
    insert_power_of_2_and_5_pisano_periods(pisano_periods_array)
    fill_rest_of_pisano_periods_array(pisano_periods_array)


def insert_prime_based_periods(pisano_periods_array):
    primes = get_prime_numbers(len(pisano_periods_array)+1)
    for prime_number in primes:
        insert_power_and_mod_based_period(pisano_periods_array, prime_number)
    return pisano_periods_array


def get_prime_numbers(n):
    sieve = [True] * n
    for i in range(3, int(n**0.5)+1, 2):
        sieve = check_if_sieve_and_fill(sieve, i, n)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


def check_if_sieve_and_fill(sieve, i, n):
    if sieve[i]:
        sieve[i*i::2*i] = [False]*int((n-i*i-1)/(2*i)+1)
    return sieve


def insert_power_and_mod_based_period(pisano_periods_array, prime):
    insert_mod_based_period(pisano_periods_array, prime)
    insert_power_prime_period(pisano_periods_array, prime)


def insert_mod_based_period(pisano_periods_array, prime):
    insert_period_which_prime_mod_10_eq_3_or_7(pisano_periods_array, prime)
    insert_period_which_prime_mod_10_eq_9_or_1(pisano_periods_array, prime)


def insert_period_which_prime_mod_10_eq_3_or_7(pisano_periods_array, prime):
    if prime % 10 == 3 or prime % 10 == 7:
        pisano_periods_array.insert(prime-1, 2*prime+2)
        pisano_periods_array.pop(prime)
    return pisano_periods_array


def insert_period_which_prime_mod_10_eq_9_or_1(pisano_periods_array, prime):
    if prime % 10 == 9 or prime % 10 == 1:
        pisano_periods_array.insert(prime-1, prime-1)
        pisano_periods_array.pop(prime)
    return pisano_periods_array


def insert_power_prime_period(pisano_periods_array, prime):
    power = 1
    power_prime = prime**power
    while power_prime <= len(pisano_periods_array):
        pisano_periods_array.insert(power_prime-1,  prime**(power-1)*pisano_periods_array[prime-1])
        pisano_periods_array.pop(power_prime)
        power += 1
        power_prime = prime**power
    return pisano_periods_array


def insert_power_of_2_and_5_pisano_periods(pisano_periods_array):
    for power in range(1, int(math.log(len(pisano_periods_array), 2)//1)+1):
        insert_power_of_2_pisano_periods(pisano_periods_array, power)
        insert_power_of_5_pisano_periods(pisano_periods_array, power)
    return pisano_periods_array


def insert_power_of_2_pisano_periods(pisano_periods_array, power):
    position = 2**power
    pisano_periods_array.insert(position-1, (3*position)//2)
    pisano_periods_array.pop(position)


def insert_power_of_5_pisano_periods(pisano_periods_array, power):
    position = 5**power
    if position <= len(pisano_periods_array):
        pisano_periods_array.insert(position-1, int(4*position))
        pisano_periods_array.pop(position)


def fill_rest_of_pisano_periods_array(pisano_period_array):
    for position in range(3, len(pisano_period_array)):
        check_if_hole_and_fill_pisano_periods(pisano_period_array, position)
    return pisano_period_array


def check_if_hole_and_fill_pisano_periods(pisano_period_array, position):
    if pisano_period_array[position] == 0:
        look_over_posible_values_and_fill_pisano_periods(pisano_period_array, position)
    return pisano_period_array


def look_over_posible_values_and_fill_pisano_periods(pisano_period_array, position):
    possible_value = 2
    while not check_if_correct_value_and_fill_pisano_periods(pisano_period_array, position, possible_value):
        possible_value += 1


def check_if_correct_value_and_fill_pisano_periods(pisano_period_array, position, possible_value):
    if (position+1) % possible_value == 0 and gcd(possible_value, (position+1)//possible_value) == 1:
        lcm_value = lcm(pisano_period_array[((position+1)//possible_value)-1], pisano_period_array[possible_value-1])
        pisano_period_array.insert(position, lcm_value)
        pisano_period_array.pop(position+1)
        return True
    else:
        return False


def gcd(a, b):
    current_gcd = min(a, b)
    while (a % b) != 0:
        current_gcd = a % b
        a = b
        b = current_gcd
    return current_gcd


def lcm(a, b):
    lcm_v = a*b
    cd = gcd(a, b)
    return lcm_v//cd


def get_equivalent_n(n, m, pisano_periods):
    return n % pisano_periods[m-1]


def get_n_fibonacci_number(n):
    fib = initialize_fibonacci_array()
    compute_n_fibonacci_number(fib, n)
    if n == 0:
        return fib[1]
    return fib[2]


def initialize_fibonacci_array():
    return [0, 0, 1]


def compute_n_fibonacci_number(fib, n):
    for i in range(2, n+1):
        rearrange_fibonacci_array(fib)
        fib.pop()
        fib.append(fib[1]+fib[0])
    return fib


def rearrange_fibonacci_array(fib):
    fib.insert(0, fib[1])
    fib.pop(1)
    fib.insert(1, fib[2])
    fib.pop(2)
    return fib


if __name__ == "__main__":
    main()
