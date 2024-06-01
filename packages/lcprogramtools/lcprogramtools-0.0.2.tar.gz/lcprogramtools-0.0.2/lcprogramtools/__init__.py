import importlib.metadata

def greet():
    author = "God"
    try:
        metadata = importlib.metadata.metadata("lcprogramtools")
        author = metadata.get('Author', 'God')
    except importlib.metadata.PackageNotFoundError:
        pass
    
    return f"{author} says hi."
