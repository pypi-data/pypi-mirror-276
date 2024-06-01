import importlib.metadata

def get_package_author(package_name):
    try:
        metadata = importlib.metadata.metadata(package_name)
        author = metadata.get('Author', 'Unknown')
        return author
    except importlib.metadata.PackageNotFoundError:
        return 'Unknown'

def greet():
    author = get_package_author("lcprogramtools")
    return f"{author} says hi"

def main():
    # import argparse
    # parser = argparse.ArgumentParser(description="Greet someone with the author's name of a given package.")
    # parser.add_argument("name", type=str, help="The name of the person to greet.")
    # args = parser.parse_args()
    # print(greet(args.name))

    print(greet())
