from pathlib import Path
import shutil

def clear_directory(path):
    p = Path(path)

    # Create the directory if it does not exist
    if not p.exists():
        p.mkdir(parents=True, exist_ok=True)
        print(f"Directory '{p}' did not exist, so it was created.")
        return

    # If it exists but is not a directory, raise an error
    if not p.is_dir():
        raise NotADirectoryError(f"'{p}' exists but is not a directory.")
    
    # Remove everything inside 'p', but not 'p' itself
    for item in p.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()
    
    print(f"All contents of '{p}' have been removed, but the directory is kept.")
