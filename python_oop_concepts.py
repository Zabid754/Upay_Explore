"""
Internship Task: Python OOP & Advanced Concepts
"""

# 1. Classes & Inheritance
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def work(self):
        return f"{self.name} is working."

class Developer(Employee): # Inheritance
    def __init__(self, name, salary, language):
        super().__init__(name, salary)
        self.language = language

    def work(self): # Method Overriding
        return f"{self.name} is coding in {self.language}."

# 2. Dunder (Magic) Methods
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self): # Returns human-readable string
        return f"'{self.title}' ({self.pages} pages)"

    def __len__(self): # Allows use of len() function
        return self.pages

# 3. Decorators
def simple_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@simple_logger
def greet(name):
    return f"Hello, {name}!"

# 4. Generators
def fibonacci_generator(limit):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# --- Testing the code ---
if __name__ == "__main__":
    dev = Developer("Zabid", 50000, "Python")
    print(dev.work())

    book = Book("Django Internals", 350)
    print(f"Book info: {book}, Length: {len(book)}")

    print(greet("Intern"))

    print("Fibonacci sequence:", list(fibonacci_generator(5)))