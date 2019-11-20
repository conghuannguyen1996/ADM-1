#programming excercise 1
def read_project(text):
    all_k, all_A, all_b, A = [], [], [], []
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
                all_b.append([float(i) for i in line.strip("\n").split(" ")])
                all_A.append(A)
                A = []
    return all_A, all_b, all_k
    
def read_image(text):
    all_M, all_A, all_b, M, A= [], [], [], [], []
    poly_flag = 0
    with open(text) as file:
        for line in file:
            if line[0] == "#":
                continue
            if line[0] == "M":
                poly_flag = 1
                continue
            if line[0] == "A":
                poly_flag = 2
                continue
            if line[0] == "b":
                poly_flag = 3
                continue
                
            if poly_flag == 1:
                M.append([float(i) for i in line.strip("\n").split(" ")])
            elif poly_flag == 2:
                A.append([float(i) for i in line.strip("\n").split(" ")])
            elif poly_flag == 3:
                all_b.append([float(i) for i in line.strip("\n").split(" ")])
                all_M.append(M)
                all_A.append(A)
                A, M = [], []
    return all_M, all_A, all_b
    
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
    row_dim, col_dim = len(M), len(M[0])
    b_new = [0 for i in range(row_dim*2)] + b
    matrix = []
    unten = []
    oben = []
    
    for line in A:  #lower matrix
        unten.append([0 for k in range(row_dim)] + line)
    
    for i in range(row_dim):    #1.part upper matrix
        temp = [0 for k in range(row_dim)]
        temp[i] = -1
        oben.append(temp + M[i])
            
    for i in range(row_dim):    #2.part upper matrix
        temp = [0 for k in range(row_dim)]
        temp[i] = 1
        for j in range(col_dim):
            M[i][j] *= -1
        oben.append(temp + M[i])
        
    matrix.append(oben+unten)
    print(matrix)
    
    
#main
all_A, all_b, all_k = read_project('project_instances.dat')
#print("k: {}\n".format(all_k) + "A: {}\n".format(all_A) + "b: {}\n".format(all_b))
#all_M, all_A, all_b = read_image('image_instances.dat')
#print("M: {}\n".format(all_M) + "A: {}\n".format(all_A) + "b: {}\n".format(all_b))
for i in range(len(all_A)):
    project(all_A[i], all_b[i], all_k[i])