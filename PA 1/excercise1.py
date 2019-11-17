#programming excercise 1
def read_polyhedron(polyhedron):
    matrix = []
    vector = []
    with open(polyhedron) as file:
        for line in file:
            if line[0] == "#":
                continue
            if line[0] == "A":
                poly_flag = True
                continue
            if line[0] == "b":
                poly_flag = False
                continue
                
            if poly_flag:#matrix A
                matrix.append([float(i) for i in line.strip("\n").split(" ")])
            else:#vektor b
                vector = [float(i) for i in line.strip("\n").split(" ")]
    return matrix, vector
    

def project(polyhedron, k):
    A, b = read_polyhedron(polyhedron)
    assert 1 <= k <= len(A[0]), "k must fulfill 1 <= k <= n"
    print(len(A[0]))
    red = len(A[0])-k
    if red == 0:
        return A,b
    else:
        return project_to_one_lower(A,b,red)

def project_to_one_lower(A, b, red):
    new_A = []
    new_b = []
    for (row_first,b_first) in zip(A,b):
        if row_first[-1] > 0:
            for (row_second,b_second) in zip(A,b):
                if row_second[-1] < 0:
                    new_A.append([ai-aj for (ai,aj) in zip([i/row_first[-1] for i in row_first[:-1]],[i/row_second[-1] for i in row_second[:-1]])])
                    new_b.append(b_first/row_first[-1] - b_second/row_second[-1])
        elif row_first[-1] == 0:
            new_A.append(row_first[:-1])
            new_b.append(b_first)
    if red-1 == 0:
        return new_A, new_b
    else:
        return project_to_one_lower(new_A, new_b, red-1)

#main
print("Test Matrix aus Ex-Session 4 {}".format(project('polyhedron.txt',3)))
