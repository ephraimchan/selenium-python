import pytest


list_numbers  = [(2,3,6), (1,99,99), (0,100,0)] 



@pytest.mark.parametrize("num1, num2, expected", list_numbers)
def test_multiplication(num1, num2, expected):
    assert num1 * num2 == expected, f"Expected {num1} * {num2} to equal {expected}"


def test_check_numbers():
    number1 = 10 
    number2 = 20
    number3 = 40

    total = number1 + number2 + number3
    assert total == 70, "Total should be 70" 


