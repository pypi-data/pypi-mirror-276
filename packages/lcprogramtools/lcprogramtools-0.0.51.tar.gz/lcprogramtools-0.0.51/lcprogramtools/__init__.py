import importlib.metadata

def get_package_author(package_name):
    try:
        metadata = importlib.metadata.metadata(package_name)
        author = metadata.get('Author', 'Unknown')
        return author
    except importlib.metadata.PackageNotFoundError:
        return None

def greet(pkgname="lcprogramtools"):
    author = get_package_author(pkgname)
    if author:
        return f"{author} of {pkgname} says hi."
    return f"{pkgname} was not found in your system. Install it first"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Greet someone with the author's name of a given package.")
    parser.add_argument("pkgname", type=str, help="The name of the package")
    args = parser.parse_args()
    if args:
        print(greet(args.pkgname))
    else:
        print(greet())
