import os
import a2dl.core.diagram as dig
import a2dl.core.library as librarian

def update_all_diagrams_in_directory(base_dir: str = './test') -> None:
    """
    Update all diagrams in the specified directory and its subfolders.

    Args:
    base_dir (str): The base directory to search for diagram files.


    """
    # Create a library
    DL = librarian.Diaglibrary()
    DL.from_folder('./data/examples/docs')
    DL.write('./test/test-generated-library.xml')

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.drawio'):
                file_path = os.path.join(root, file)
                print(f"Updating diagram: {file_path}")

                # Update the diagram
                DG = dig.Diagdiagram()
                DG.from_file(file_path)
                DG.update(libraries=[DL])

                print(f"Diagram updated: {file_path}")


if __name__ == "__main__":
    base_directory = './test'
    update_all_diagrams_in_directory(base_directory)
