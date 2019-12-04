from sys import argv
from subprocess import run, PIPE, STDOUT
from ast import literal_eval

def nextline(f):
  try:
    line = next(f).strip()
    while line == "" or line[0] == '#':
      line=next(f).strip()
  except StopIteration:
    return ""
  return line

def testequalpolyhedra(ineq1,ineq2,testpoints):
  for x in testpoints:
    inP1 = 1
    A, b = ineq1
    for i in range(len(A)):
      lhs = sum(A[i][j]*x[j] for j in range(len(A[i])))
      if lhs < b[i]-0.0000000000003:
        inP1 = -1
        break
      elif lhs < b[i]+0.0000000000003:
        inP1 = 0
    inP2 = 1
    A, b = ineq2
    for i in range(len(A)):
      lhs = sum(A[i][j]*x[j] for j in range(len(A[i])))
      if lhs < b[i]-0.00000000000001:
        inP2 = -1
        break
      elif lhs < b[i]+0.00000000000001:
        inP2 = 0
    if inP1 - inP2 > 1 or inP2 - inP1 > 1:
      return False
  return True

def test_x_or_y(output,A,b):
  if output[0]:
    x = output[1]
    for i in range(len(A)):
      if sum(A[i][j]*x[j] for j in range(len(x)))<b[i]:

    #    print(sum(A[i][j]*x[j] for j in range(len(x))))
    #    print("hier {}".format(b[i]))
        return False
  if not output[0]:
    y = output[1]
    for i in range(len(y)):
      if y[i] < 0:
        return False
    for j in range(len(A[0])):
      ytransposedai = sum(y[i]*A[i][j] for i in range(len(y)))
      if ytransposedai < -0.00000000000001 or ytransposedai > 0.00000000000001:
        return False
    if sum(y[i]*b[i] for i in range(len(y))) <= 0:
      return False
  return True

def test_project(instancefile,solutionfile,testpointfile):
  with open(instancefile,'r') as instances:
    with open(solutionfile,'r') as solutions:
      inputline = instances.readline()
      while inputline !="":
        assert inputline[0]=='k'
        k = inputline.split()[1]
        inputline = instances.readline()
        with open("tempinput.in",'w') as tempinput:
          while inputline != "" and inputline[0] != 'k':
            tempinput.write(inputline)
            inputline = instances.readline()
        run(["truncate", "-s", "-1", "tempinput.in"])
        result = run(["./fourier-motzkin.sh", "project", "tempinput.in", k, "outfile.ot"], stdout=PIPE, stderr=STDOUT)
        print("output test project: "+result.stdout.decode('utf-8'))
        solA = []
        solutionline = solutions.readline()
        assert solutionline=="A\n"
        solutionline = solutions.readline()
        while solutionline != "b\n":
          solA.append(list(map(float,solutionline.split(" "))))
          solutionline = solutions.readline()
        solutionline = solutions.readline()
        solb = list(map(float,solutionline.split(" ")))
        with open("outfile.ot",'r') as outfile:
          A = []
          outline = nextline(outfile)
          assert outline=="A"
          outline = nextline(outfile)
          while outline != "" and outline != "b":
            A.append(list(map(float,outline.split(" "))))
            outline = nextline(outfile)
          if outline == "" or outline == "\n":
            raise Exception("No correct output file")
          outline = nextline(outfile)
          if outline == "" or outline == "\n":
            print("Empty b vector")
            b = []
          else:
            b = list(map(float,outline.split(" ")))
        n = len(solA[0])
        with open(testpointfile,'r') as testpoints:
          points = []
          testline = testpoints.readline()
          assert testline[0] == "n"
          while testline != "n {}\n".format(n):
            testline = testpoints.readline()
          testline = testpoints.readline()
          while testline != "" and testline != "\n" and testline[0] != 'n':
            points.append(list(map(float,testline.split(" "))))
            testline = testpoints.readline()
        if not testequalpolyhedra((A,b),(solA,solb),points):
          return False
  return True

def test_image(instancefile,solutionfile,testpointfile):
  with open(instancefile,'r') as instances:
    with open(solutionfile,'r') as solutions:
      inputline = instances.readline()
      while inputline !="":
        assert inputline[0]=='M'
        inputline = instances.readline()
        with open("tempmatrix.in",'w') as tempmatrix:
          while inputline != "" and inputline != "A\n":
            tempmatrix.write(inputline)
            inputline = instances.readline()
        with open("temppolyhedron.in",'w') as temppolyhedron:
          while inputline != "" and inputline[0] != 'M':
            temppolyhedron.write(inputline)
            inputline = instances.readline()
        run(["truncate", "-s", "-1", "tempmatrix.in"])
        run(["truncate", "-s", "-1", "temppolyhedron.in"])
        result = run(["./fourier-motzkin.sh", "image", "temppolyhedron.in", "tempmatrix.in", "outfile.ot"], stdout=PIPE, stderr=STDOUT)
        print("output test image: "+result.stdout.decode('utf-8'))
        solA = []
        solutionline = solutions.readline()
        assert solutionline=="A\n"
        solutionline = solutions.readline()
        while solutionline != "b\n":
          solA.append(list(map(float,solutionline.split(" "))))
          solutionline = solutions.readline()
        solutionline = solutions.readline()
        solb = list(map(float,solutionline.split(" ")))
        with open("outfile.ot",'r') as outfile:
          A = []
          outline = nextline(outfile)
          assert outline=="A"
          outline = nextline(outfile)
          while outline != "" and outline != "b":
            A.append(list(map(float,outline.split(" "))))
            outline = nextline(outfile)
          if outline == "":
            raise Exception("No correct output file")
          outline = nextline(outfile)
          if outline == "" or outline == "\n":
            print("Empty b vector")
            b = []
          else:
            b = list(map(float,outline.split(" ")))
        n = len(solA[0])
        with open(testpointfile,'r') as testpoints:
          points = []
          testline = testpoints.readline()
          assert testline[0] == "n"
          while testline != "n {}\n".format(n):
            testline = testpoints.readline()
          testline = testpoints.readline()
          while testline != "" and testline != "\n" and testline[0] != 'n':
            points.append(list(map(float,testline.split(" "))))
            testline = testpoints.readline()
        if not testequalpolyhedra((A,b),(solA,solb),points):
          return False
  return True

def test_H_representation(instancefile,solutionfile,testpointfile):
  with open(instancefile,'r') as instances:
    with open(solutionfile,'r') as solutions:
      inputline = instances.readline()
      while inputline !="":
        assert inputline[0]=='X'
        inputline = instances.readline()
        with open("tempinput.in",'w') as tempinput:
          while inputline != "" and inputline != "X\n":
            tempinput.write(inputline)
            inputline = instances.readline()
        run(["truncate", "-s", "-1", "tempinput.in"])
        result = run(["./fourier-motzkin.sh", "H_representation", "tempinput.in", "outfile.ot"], stdout=PIPE, stderr=STDOUT)
        print("output test H_representation: "+result.stdout.decode('utf-8'))
        solA = []
        solutionline = solutions.readline()
        assert solutionline=="A\n"
        solutionline = solutions.readline()
        while solutionline != "b\n":
          solA.append(list(map(float,solutionline.split(" "))))
          solutionline = solutions.readline()
        solutionline = solutions.readline()
        solb = list(map(float,solutionline.split(" ")))
        with open("outfile.ot",'r') as outfile:
          A = []
          outline = nextline(outfile)
          assert outline=="A"
          outline = nextline(outfile)
          while outline != "" and outline != "b":
            A.append(list(map(float,outline.split(" "))))
            outline = nextline(outfile)
          if outline == "":
            raise Exception("No correct output file")
          outline = nextline(outfile)
          b = list(map(float,outline.split(" ")))
        n = len(solA[0])
        with open(testpointfile,'r') as testpoints:
          points = []
          testline = testpoints.readline()
          assert testline[0] == "n"
          while testline != "n {}\n".format(n):
            testline = testpoints.readline()
          testline = testpoints.readline()
          while testline != "" and testline != "\n" and testline[0] != 'n':
            points.append(list(map(float,testline.split(" "))))
            testline = testpoints.readline()
        if not testequalpolyhedra((A,b),(solA,solb),points):
          return False
  return True

def test_compute_x_or_y(instancefile):
  with open(instancefile,'r') as instances:
    inputline = instances.readline()
    while inputline !="":
      assert inputline=="A\n"
      with open("tempinput.in",'w') as tempinput:
        tempinput.write(inputline)
        A = []
        inputline = instances.readline()
        while inputline != "" and inputline != "b\n":
          tempinput.write(inputline)
          A.append(list(map(float,inputline.split(" "))))
          inputline = instances.readline()
        tempinput.write(inputline)
        inputline = instances.readline()
        tempinput.write(inputline)
      b = list(map(float,inputline.split(" ")))
      inputline = instances.readline()
      run(["truncate", "-s", "-1", "tempinput.in"])
      result = run(["./fourier-motzkin.sh", "compute_x_or_y", "tempinput.in"], stdout=PIPE, stderr=PIPE, encoding='utf-8')
      print("output test compute_x_or_y: "+result.stderr)
      output = literal_eval(result.stdout)
      print(output)
      if not test_x_or_y(output,A,b):
        print("fehler")
        return False
  return True

print("Test project: {}".format(test_project("project_instances.dat","project_solutions.dat","testpoints.dat")))
print("Test image: {}".format(test_image("image_instances.dat","image_solutions.dat","testpoints.dat")))
print("Test H_representation: {}".format(test_H_representation("H_representation_instances.dat","H_representation_solutions.dat","testpoints.dat")))
print("Test compute_x_or_y: {}".format(test_compute_x_or_y("project_solutions.dat")))
