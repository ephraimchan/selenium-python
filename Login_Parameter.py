# test_data.py

LOGIN_SCENARIOS = [
    {"username": "tomsmith", "password": "SuperSecretPassword!", "expected": "success", "desc": "Valid Login"},
    {"username": "wronguser", "password": "SuperSecretPassword!", "expected": "fail", "desc": "Invalid Username"},
    {"username": "tomsmith", "password": "WrongPassword!", "expected": "fail", "desc": "Invalid Password"},
    {"username": "", "password": "SuperSecretPassword!", "expected": "fail", "desc": "Empty Username"},
    {"username": "tomsmith", "password": "", "expected": "fail", "desc": "Empty Password"},
    {"username": "admin", "password": "admin", "expected": "fail", "desc": "Admin Defaults"},
    {"username": "tomsmith ", "password": "SuperSecretPassword!", "expected": "fail", "desc": "Trailing Space User"},
    {"username": "TOMSMITH", "password": "SuperSecretPassword!", "expected": "fail", "desc": "Case Sensitivity"},
    {"username": "!@#$%^", "password": "SuperSecretPassword!", "expected": "fail", "desc": "Special Characters"},
    {"username": "tomsmith", "password": " SuperSecretPassword!", "expected": "fail", "desc": "Leading Space Pass"}
]