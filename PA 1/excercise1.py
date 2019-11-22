#programming excercise 1
def read_polyhedron(text):
    A, b = [], []
    poly_flag = None
    with open(text) as file:
        for line in file:
            if line[0] == "#":
                continue
            if line[0] == "k":
                k = int(line.strip("\n").split(" ")[1])
                all_k.append(k)
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
    
def read_matrix(text):
    M = []
    poly_flag = False
    with open(text) as file:
        for line in file:
            if line[0] == "#":
                poly_flag = False
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

def project(A, b, k):
    if len(A) == 0: #no bounds
        return [],[]
    assert 1 <= k <= len(A[0])
    if k == len(A[0]): 
        return A[:],b[:]    #copys
    new_A = []
    new_b = []
    for (row_first,b_first) in zip(A,b):    #iterate through rows
        if row_first[-1] > 0:   #every positiv coefficient - every negativ coefficient(last coef)
            for (row_second,b_second) in zip(A,b):
                if row_second[-1] < 0:
                    new_A.append([ai-aj for (ai,aj) in zip([i/row_first[-1] for i in row_first[:-1]],[i/row_second[-1] for i in row_second[:-1]])])
                    new_b.append(b_first/row_first[-1] - b_second/row_second[-1])
        elif row_first[-1] == 0:    #no bounds
            new_A.append(row_first[:-1])
            new_b.append(b_first)
    return project(new_A, new_b, k)

def compute_x_or_y(A,b):
    matrices = [project(A,b,i) for i in range(1,len(A[0])+1)]  #compute dimension from 1,...n
    x= []
    
    for (A_new,b_new) in matrices:
        if len(A_new) == 0: #no bounds
            x.append(0)
            continue
        else:          
            for i in range(len(A_new)): #for every row
                for j in range(len(x)): #calculate b-x1*a-x2*b....
                    b_new[i] -= A_new[i][j] * x[j]
                if A_new[i][-1] != 0:   #divide by coefficient of last last variable
                    b_new[i] /= A_new[i][-1]
                if b[i] != 0: #x1....xn = 0 and b != 0
                    feas = [A[i][k] != 0 for k in range(len(A[i]))]
                    if sum(feas) == 0:
                        return False, 
            x.append(max(b_new))
    return True, x

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

    return project(matrix, b_new, row_dim)

def H_representation(X):
    k = len(X)
    P = [[float(1) for i in range(k)]]
    b = [1]
    return image(X,P,b)

#main