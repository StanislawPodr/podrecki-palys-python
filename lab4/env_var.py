import os
import sys

def main():
    filters = [arg.lower() for arg in sys.argv[1:]]
    env_vars = os.environ.items()

    if filters:
        env_vars = [
            (name, value)
            for name, value in env_vars
            if any(f in name.lower() for f in filters)
        ]
    else:
        env_vars = list(env_vars)

    for name, value in sorted(env_vars, key=lambda x: x[0].lower()):
        print(f"{name}={value}")

if __name__ == "__main__":
    main()