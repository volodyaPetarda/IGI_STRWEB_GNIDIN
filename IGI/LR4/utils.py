def input_str(message: str):
    while True:
        try:
            value = input(message)
            if not value.strip():
                raise ValueError("Input cannot be empty.")
            return value
        except ValueError as e:
            print(e)

def input_int(message: str):
    while True:
        try:
            value = int(input(message))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def input_float(message: str):
    while True:
        try:
            value = float(input(message))
            return value
        except ValueError:
            print("Invalid input. Please enter a float.")