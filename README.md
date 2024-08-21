# Cardlet

**Cardlet** is a Python-based project developed using the `tkinter` module. It is designed to create double-sided flashcards from a simple `.txt` file, which can be used for learning and study purposes. With this application, you can transform text files containing terms and their definitions into an interactive card system that enhances the learning process.

## Usage

To use **Cardlet**, please follow these steps:

1. **Download the files:**
   - Download all necessary files from the repository and save them in a directory on your local machine.

2. **Install Python:**
   - Ensure that Python is installed on your local machine. You can download the latest version of Python [here](https://www.python.org/downloads/). **Cardlet** uses the `tkinter` module, which is included by default in Python.

3. **Prepare the text files:**
   - To create your own flashcards, you need a `.txt` file that contains your terms and definitions in the following format:

     ```
     word:definition$next term
     ```

     **Example:**
     ```
     Cat:A small, typically furry, carnivorous mammal often kept as a pet$Dog:A domesticated descendant of the wolf, commonly kept as a pet and known for its loyalty
     ```

     The terms and their definitions should be separated by a colon (`:`), and each term-definition pair should be separated from the next by a dollar sign (`$`).

4. **Run Cardlet:**
   - Run the Python file to launch the user interface. In the application, you can load your prepared `.txt` file and flip through the double-sided flashcards.
   - **Navigate through cards:** Use the left and right arrow keys on your keyboard to switch between the cards. The left arrow key moves to the previous card, and the right arrow key moves to the next card.
