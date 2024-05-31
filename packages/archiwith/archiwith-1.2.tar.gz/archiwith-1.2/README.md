# Archiwith
Class that gives you the mini help to avoid to write `open(file_path,'r')` or `open(file_path,'w')` every time ypu want to work with some text file.


## Installation

You can easily install `archiwith` using pip:

```bash
pip install archiwith
```
or via git:

```bash
git clone https://github.com/niCodeLine/archiwith.git
```
or just copy-paste it into your code.

## Usage

To use the mini helper simply import the class and call it stating the file path of the text file you want to open. Then use it with the `with` method. Here's a simple example:

### Reading
```python
from archiwith import Archiwith

# Stating the file path
reader = Archiwith('path/to/your/file').abrir()

# Using the with method
with reader as file:
    # Do something with the file
```

Another way and opening a binari:


```python
# Stating the file path
reader = Archiwith('path/to/your/file')

# Reading as binari file
with reader.abrir(binari=True) as file:
    # Do something with the file
```

If the file is text-readeable you can just:

```python
# Stating the file path
reader = Archiwith('path/to/your/file')

text = reader.leer()
```

or shorter:

```python
# Stating the file path
text = Archiwith('path/to/your/file').leer()
```


### Writing

```python
# Stating the file path
writer = Archiwith('path/to/your/file').escribir()

# Using the with method
with writer as file:
    # Write the file
```

## ObjetiFiles 

This implementation speeds up file handling by allowing access to file names as attributes, eliminating the need to manually write them out one by one. For example, lets say your folder has a structure like this:

```css
your_folder/
│
├── firstcode.py
├── another_folder/
├── outputs.txt
├── tests.txt
└── my programs.py

```
You can access to the names via:

```python
from archiwith import ObjectiFiles

path = 'path/to/your_folder'
files = ObjectiFiles(path)

```
This will create the `files` object with the valid files as attributes and nameing them with a `f_file_name__ext` form. So:

```python
>>> files.f_tests__txt
'tests.txt'
>>> files.f_my_programs__py
'my programs.py'
```
If you have suggestions enabled in your code editor (command I in VS Code), you will get the names when typing `files.f`. The `f` prefix comes from File and is to get a clearer view of what are the files in the autocomplete suggestions.

## Features
That would be it.
## Contributions

Contributions are welcome! If you have improvements or fixes, please send a pull request or open an issue in the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

Nico Spok - nicospok@hotmail.com
GitHub: niCodeLine
