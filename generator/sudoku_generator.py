import sys

class Meggie:
    def __init__(self) -> None:
        self.attribute = "cutest"
        self.name = "Meggie"
        self.age = 30

    def introduce(self):
        print(f"Hello! My name is {self.name} and I am {self.age} years old, and I am the {self.attribute}.")

    def attack(self):
        print("Sometimes I attack")

def main():
    m = Meggie()
    m.introduce()
    m.attack()

if __name__ == "__main__":
    sys.exit(main())
