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
    return

def project_to_one_lower(A, b, k):
    if len(A) == 0:
        return [],[]
    assert 1 <= k <= len(A[0])
    if k == len(A[0]): 
        return A[:],b[:]    #copys
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
    return project_to_one_lower(new_A, new_b, k)

def compute_x_or_y(A,b):
    matrices = [project_to_one_lower(A,b,i) for i in range(len(A[0]),0,-1)]
    print(matrices)
    x= []
    for (A_new,b_new) in matrices[::-1]:
        if len(A_new) == 0:
            print("random----------------")
            x.append(0)
            continue
        else:          
            for i in range(len(A_new)):
                for j in range(len(x)):
                    print(A_new,x,b_new)
                    b_new[i] -= A_new[i][j] * x[j]
                if A_new[i][-1] != 0:
                    b_new[i] /= A_new[i][-1]
                if b[i] != 0: 
                    feas = [A[i][k] != 0 for k in range(len(A[i]))]
                    if sum(feas) == 0:
                        return False
            x.append(max(b_new))
    print("test {}".format(b))
    return True, x
        
#main
A,b = read_polyhedron('solution.txt')
print(A,b)
#print("Test Matrix aus Ex-Session 4 {}".format(project('polyhedron.txt',3)))
print(compute_x_or_y(A,b))