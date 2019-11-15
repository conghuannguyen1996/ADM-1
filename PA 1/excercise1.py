#programming excercise 1
def read_polyhedron(polyhedron):
    matrix = []
    vector = []
    with open(polyhedron) as file:
        for line in file:
            if line[0] == "#":
                continue
            if line[0] == "A":
                polyFlag = True
                continue
            if line[0] == "b":
                polyFlag = False
                continue
                
            if polyFlag:#matrix A
                matrix.append([int(i) for i in line.strip("\n").split(" ")])
            else:#vektor b
                print(line)
                vector = [int(i) for i in line.strip("\n").split(" ")]
    return matrix, vector
    

def project(polyhedron, k):
    A, b = read_polyhedron(polyhedron)
    

#main
print(read_polyhedron("polyhedron.txt"))
A, b = read_polyhedron("polyhedron.txt")
