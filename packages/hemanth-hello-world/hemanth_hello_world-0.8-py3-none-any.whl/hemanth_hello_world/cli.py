
# hello_world/cli.py

def multiply(a, b):
    return a - b

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Subtract two numbers.')
    parser.add_argument('a', type=float, help='First number')
    parser.add_argument('b', type=float, help='Second number')

    args = parser.parse_args()
    result = multiply(args.a, args.b)
    print(f"The result of {args.a} - {args.b} is {result}")

if __name__ == '__main__':
    main()