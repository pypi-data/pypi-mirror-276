import argparse
import os

def init_project():
    """Creates the initial Zenaura project structure."""
    project_name = input("Enter project name: ")
    os.makedirs(project_name, exist_ok=True)

    # Create public directory and files
    public_dir = os.path.join(project_name, "public")
    os.makedirs(public_dir, exist_ok=True)
    files = ["__init__.py", "components.py", "main.py", "index.html", "presentational.py"]
    for file in files:
        with open(os.path.join(public_dir, file), "w") as f:
            pass

    build_file = os.path.join(project_name, "build.py")
    index_file = os.path.join(project_name, "index.py")
    with open(build_file, "w") as f:
        pass
    with open(index_file, "w") as f:
        pass

    print("Zenaura project initialized successfully!")

def build_project():
    """Runs the build.py script."""
    os.system("python build.py")  # Adjust if build.py is elsewhere

def run_project():
    """Runs the index.py script."""
    os.system("python index.py")  # Adjust if index.py is elsewhere

def main():
    parser = argparse.ArgumentParser(description="Zenaura CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Create a new project")
    build_parser = subparsers.add_parser("build", help="Build the project")
    run_parser = subparsers.add_parser("run", help="Run the project")

    args = parser.parse_args()

    if args.command == "init":
        init_project()
    elif args.command == "build":
        build_project()
    elif args.command == "run":
        run_project()
    else:
        parser.print_help()