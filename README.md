# Class Recognition Solver

Given a graph class that can be characterized by the existence of a linear order on the vertices of the graphs forbidding certain patterns, this project solves the class recognition problem for any graph using Answer Set Programming (ASP). You can input a graph and specify a set of forbidden patterns (represented by existing and non-existing edges in the linear order of the vertices) or use a predefined class (e.g., interval, chordal graphs). The program will then check if the graph belongs to the specified class.

## Requirements

- Python 3.x
- Clingo
- NetworkX
- JSON

## Usage 

You can run the program from the terminal.

Example using a predefined graph class:
```bash
python main.py --graph_file graph.lp --predefined_class chordal.lp
```

Example using a list of forbidden patterns:
```bash
python main.py --graph_file graph.lp --constraints constraints.json
```
Arguments

    --graph_file: Path to the file containing the graph.
    --constraints: (Optional) Path to the constraints file (in JSON format) specifying edges and non-edges.
    --predefined_class: (Optional) A predefined graph class such as interval.lp, chordal.lp.

An example of the format of --graph_file is provided in file "app/graph.txt" and an example of the format of --constraints is provided in the file "app/constraints.json". On the other hand, --predefined_class only admits as arguments interval.lp, chordal.lp or unit2interval.lp

