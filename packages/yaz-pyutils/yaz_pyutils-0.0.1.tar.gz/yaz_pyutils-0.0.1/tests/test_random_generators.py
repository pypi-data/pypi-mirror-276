# tests/test_random_generators.py
from src.yaz_pyutils.randoms.generate import (
    random_number,
    random_numbers,
    random_alpha,
    random_alphanumeric,
    random_string
)

def test_random_number():
    num = random_number(1, 10)
    assert 1 <= num <= 10

def test_random_numbers():
    num_str = random_numbers(10)
    assert len(num_str) == 10
    assert num_str.isdigit()

def test_random_alpha():
    alpha_str = random_alpha(10)
    assert len(alpha_str) == 10
    assert alpha_str.isalpha()

def test_random_alphanumeric():
    alnum_str = random_alphanumeric(10)
    assert len(alnum_str) == 10
    assert all(c.isalnum() for c in alnum_str)

def test_random_string():
    rand_str = random_string(10)
    assert len(rand_str) == 10

