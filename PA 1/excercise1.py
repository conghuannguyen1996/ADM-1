#programming excercise 1
import sys
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
    matrices = [project(A,b,i,[])[:-1] for i in range(1,len(A[0])+1)]  #compute dimension from 1,...n
    x= []
    
    for (A, b) in matrices:
        if len(A) == 0: #no bounds
            x.append(0)
            continue
        else:          
            for i in range(len(A)): #for every row
                for j in range(len(x)): #calculate b-x1*a-x2*b....
                    b[i] -= A[i][j] * x[j]
                if A[i][-1] != 0:   #divide by coefficient of last last variable
                    b[i] /= A[i][-1]
                if b[i] > 0: #xn = 0 and b_new != 0 => no solution
                    if A[i][-1] == 0:
                        return False,
            x.append(max(b))
    return True, x


def farkas_lemma(matrices): #projects 1.....n
    y = []
    return


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
    P = [[float(1) for i in range(k)]]
    b = [1]
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
    A, b = project(A,b,k,[])[:-1]
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
