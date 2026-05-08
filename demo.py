import argparse

class Demo:
    def __init__(self, name: str):
        self.name = name

    def greet(self) -> str:
        return f"Hello, {self.name}! This is a demo."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs="?", default="World", help="Name to greet")
    args = parser.parse_args()

    d = Demo(args.name)
    print(d.greet())


if __name__ == "__main__":
    main()
