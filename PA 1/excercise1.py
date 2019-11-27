#programming excercise 1
import sys
import copy
def read_polyhedron(polyhedron):
    A, b = [], []
    poly_flag = None
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
                A.append([float(i) for i in line.strip("\n").split(" ")])
            else:#vektor b
                b =[float(i) for i in line.strip("\n").split(" ")]
    return A, b


def read_matrix(matrix):
    M = []
    poly_flag = False
    with open(matrix) as file:
        for line in file:
            if line[0] == "#":
                poly_flag = False
                continue
            elif line[0] == "M" or line[0] == "X":  #only needed for test_instances.zip
                poly_flag == True
                continue
            else:
                poly_flag = True
                
            if poly_flag:
                M.append([float(i) for i in line.strip("\n").split(" ")])
    return M


def read_image_inst(project_instances):
    dim = 0
    matrix = []
    vector = []
    with open(project_instances) as file:
        for line in file:
            if line[0] == "#":
                continue
            if line[0] == 'k':
                dim = float(line[2])
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
    return matrix, vector, dim


def project(A, b, k, E):   #returns projected A,b and elimination matrix E
    if len(A) == 0:
        return [],[],[]
    assert 1<=k<=len(A[0])
    if k == len(A[0]):
        return A[:], b[:], E
    E_temp = []
    new_A = []
    new_b = []
    positive = [i for i in range(len(A)) if A[i][-1] > 0]   #positive coef of xn
    negative = [i for i in range(len(A)) if A[i][-1] < 0]   #negative coef of xn
    zero = [i for i in range(len(A)) if A[i][-1] == 0]      #zero coef of xn

    for i in positive:
        for j in negative:  # sum(ai'-aj') >= bi'-bj'
            new_A.append([A[i][l]/A[i][-1] - A[j][l]/A[j][-1] for l in range(len(A[0])-1)])
            new_b.append(b[i]/A[i][-1] - b[j]/A[j][-1])
            #elimnation saves the operation above
            elimination = [0 for l in range(len(A))]
            elimination[i] , elimination[j] = 1/A[i][-1] , -1/A[j][-1]
            E_temp.append(elimination)

    for i in zero:
        new_A.append(A[i][:-1])
        new_b.append(b[i])
        #ensure row won't change(saves the operation above)
        elimination = [0 for l in range(len(A))]
        elimination[i] = 1
        E_temp.append(elimination)

    E.append(E_temp)
    return project(new_A, new_b, k, E)


def compute_x_or_y(A,b):
    matrices = [project(A,b,i,[]) for i in range(1,len(A[0])+1)]  #compute dimension from 1,...n
    matrices_copy = copy.deepcopy(matrices)
    x= []
    for (A, b, E) in matrices:
        if len(A) == 0: #no bounds
            x.append(0)
            continue
        else:
            smallest_bigger = -float("inf")
            smallest_smaller = float("inf")
            for i in range(len(A)): #for every row
                for j in range(len(x)): #calculate b-x1*a-x2*b....
                    b[i] -= A[i][j] * x[j]
                if A[i][-1] > 0:   #divide by coefficient of last last variable
                    b[i] /= A[i][-1]
                    if b[i] > smallest_bigger:
                        smallest_bigger = b[i]
                if A[i][-1] < 0:
                    b[i] /= A[i][-1]
                    if b[i] < smallest_smaller:
                        smallest_smaller = b[i]
                if b[i] > 0: #xn = 0 and b_new != 0 => no solution
                    if A[i][-1] == 0:
                        return False, farkas_lemma(matrices_copy)
            if smallest_smaller + 1e-08< smallest_bigger:
                return False, farkas_lemma(matrices_copy)
            if smallest_bigger != -float("inf"): #unnecessary but gives output closer to solution
                x.append(smallest_bigger)
            else:
                x.append(smallest_smaller)
    return True, x


def farkas_lemma(matrices): #projects 1.....n we are solving the induction start by compute_x_or_y of
                            # A.T*y >= 0, -A.T*y >= 0, b_T*y >=0.1, In*y >= 0

    A, b, E = matrices[0]
    #induction start
    new_A = [[A[x][0] for x in range(len(A))], [-A[x][0] for x in range(len(A))], [b[i] for i in range(len(b))]]
    for i in range(len(b)):
        temp = [0 for j in range(len(b))]
        temp[i] = 1
        new_A.append(temp)
    new_b = [0]*2
    new_b += [0.1]  #error prone
    new_b += [0 for i in range(len(b))]
    y = compute_x_or_y(new_A,new_b)[1]
    for matrix in E:    #inductionstep
        matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))] #tranpose
        y = matrix_vektor(matrix,y)
    return y


def matrix_vektor(E,y):#multiplication
    out = []
    for row in E:
        res = 0
        for entry in range(len(row)):
            res += row[entry]*y[entry]
        out.append(res)
    return out


def image(M, A, b):
    row_dim = len(M)
    col_dim = len(M[0])
    b_new = [0 for i in range(row_dim*2)] + b
    matrix = []
    upper = []
    lower = []

    for line in A:  #lower matrix
        lower.append([0 for k in range(row_dim)] + line)

    for i in range(row_dim):    #1.part upper matrix
        temp = [0 for k in range(row_dim)]
        temp[i] = float(1)
        for j in range(col_dim):
            M[i][j] *= -1
        upper.append(temp + M[i])

    for i in range(row_dim):    #2.part upper matrix
        temp = [0 for k in range(row_dim)]
        temp[i] = float(-1)
        for j in range(col_dim):
            M[i][j] *= -1
        upper.append(temp + M[i])

    matrix = upper + lower

    return project(matrix, b_new, row_dim, [])[:-1]


def H_representation(X):
    k = len(X)
    P = [[float(1) for i in range(k)]]+[[-float(1) for i in range(k)]]
    b = [1]+[-1]
    return image(X, P, b)


def poly_writer(A,b ,file):
    with open(file, "w+") as file:
        file.write("A\n")
        for row in A:
            file.write(" ".join(str(e) for e in row) + "\n")
        file.write("b\n")
        file.write(" ".join(str(e) for e in b) + "\n")


#main
if sys.argv[1] == 'project':
    A, b = read_polyhedron(sys.argv[2])
    k = int(sys.argv[3])
    A, b, E = project(A,b,k,[])
    poly_writer(A,b,sys.argv[4])    #overwritting output_file

elif sys.argv[1] == 'image':
    A, b = read_polyhedron(sys.argv[2])
    M = read_matrix(sys.argv[3])
    A, b = image(M, A, b)
    poly_writer(A, b, sys.argv[4])  #overwritting output_file

elif sys.argv[1] == 'H_representation':
    X = read_matrix(sys.argv[2])
    A, b = H_representation(X)
    poly_writer(A, b, sys.argv[3])  #overwritting output_file

elif sys.argv[1] == 'compute_x_or_y':
    A, b = read_polyhedron(sys.argv[2])
    print(compute_x_or_y(A, b))
