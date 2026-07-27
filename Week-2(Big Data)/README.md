# MapReduce Movie Genre Counter

## 📌 Project Overview

This project demonstrates the basic **MapReduce programming model** using Python. It processes a text file containing movie genres and calculates the total number of occurrences of each genre.

The project is divided into three main stages:

1. **Mapper** – Reads each genre and generates a key-value pair in the form `(genre, 1)`.
2. **Partitioner** – Groups all values belonging to the same genre.
3. **Reducer** – Adds the values for each genre to calculate the final count.

The main program coordinates these three stages and displays the final results.

---

## 📂 Project Structure

```text
MapReduce-Genre-Counter/
│
├── main.py
├── mapper.py
├── partitioner.py
├── reducer.py
├── input.txt
└── README.md
```

### File Description

| File             | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `main.py`        | Main program that executes the MapReduce workflow      |
| `mapper.py`      | Converts each genre into a `(genre, 1)` key-value pair |
| `partitioner.py` | Groups values based on their genre                     |
| `reducer.py`     | Calculates the total count for each genre              |
| `input.txt`      | Input file containing movie genres                     |
| `README.md`      | Project documentation                                  |

---

## ⚙️ How It Works

### 1. Input

The `input.txt` file contains movie genres, with each genre appearing as a separate entry.

Example:

```text
Action
Comedy
Action
Drama
Comedy
Action
Romance
Drama
```

---

### 2. Map Phase

The Mapper reads each line and generates a key-value pair:

```text
Action  →  (Action, 1)
Comedy  →  (Comedy, 1)
Action  →  (Action, 1)
Drama   →  (Drama, 1)
```

The mapper implementation creates a list of `(genre, 1)` pairs for non-empty input lines.

---

### 3. Partition Phase

The Partitioner groups values having the same key:

```text
Action  →  [1, 1, 1]
Comedy  →  [1, 1]
Drama   →  [1]
```

This allows the reducer to process all occurrences of the same genre together.

---

### 4. Reduce Phase

The Reducer adds all values associated with each genre:

```text
Action  →  3
Comedy  →  2
Drama   →  1
```

The reducer uses the `sum()` function to calculate the total for each genre.

---

## 🔄 MapReduce Workflow

```text
             input.txt
                 │
                 ▼
           ┌───────────┐
           │   MAPPER  │
           └───────────┘
                 │
                 ▼
        (Genre, 1) pairs
                 │
                 ▼
        ┌────────────────┐
        │   PARTITIONER  │
        └────────────────┘
                 │
                 ▼
       Genre → [1, 1, 1, ...]
                 │
                 ▼
           ┌───────────┐
           │  REDUCER  │
           └───────────┘
                 │
                 ▼
       Genre → Total Count
                 │
                 ▼
          Final Output
```

---

## ▶️ How to Run

### Step 1: Install Python

Make sure Python 3 is installed on your computer.

Check the Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

### Step 2: Place All Files in One Folder

Make sure the following files are in the same directory:

```text
main.py
mapper.py
partitioner.py
reducer.py
input.txt
```

### Step 3: Run the Program

Open the terminal in the project directory and execute:

```bash
python main.py
```

The `main.py` program reads `input.txt`, calls the mapper, partitioner, and reducer sequentially, and prints the final MapReduce result.

---

## 📊 Example Output

For the given input data, the output will be similar to:

```text
Final MapReduce Result
----------------------
Action: 7
Comedy: 5
Drama: 3
Romance: 3
Horror: 2
```

> The exact counts depend on the contents of `input.txt`.

---

## 🛠️ Technologies Used

* **Python 3**
* **MapReduce Programming Model**
* **File Handling**
* **Dictionaries**
* **Lists**
* **Functions**

---

## 🎯 Learning Objectives

This project helps understand:

* The concept of MapReduce
* Mapping input data into key-value pairs
* Partitioning and grouping data
* Reducing grouped data to produce final results
* Modular programming in Python
* Basic data processing using lists and dictionaries

---

## 🚀 Future Improvements

The project can be extended to:

* Process large datasets
* Read CSV files containing movie information
* Count multiple attributes such as genre, year, and rating
* Implement sorting before the reduce phase
* Add a command-line interface
* Handle multiple input files
* Implement parallel processing using Python multiprocessing

---

## 👨‍💻 Author

**Sivarama Krishnan A**

---

## 📄 License

This project is created for educational and academic purposes.

