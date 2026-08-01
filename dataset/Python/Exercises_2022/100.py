class Course:
  def __init__(self,str):
    self.name = str
    self.gread = 101
  def setGread(self,gread):
      """
      :param gread: check if the gread of the gread is bewtween 0-100
      :return: true if the value is good
      """
      assert gread >= 0 and gread <= 100 , "you enter wrong gread"
      self.gread = gread
      return True
class Studtent:
 def __init__(self,name,id):
    self.name = name
    self._id = id
    self.gread = []
 def getId(self):
     """
     :return: the id of the student
     """
     return self._id
 def __init__(self,str):
         """
         :param self: the student object
         :param str: line from the file we reading
         :return: the
         """
         self.name = str[0]
         self._id = str[1]
         self.gread = []
         for i in range (len(str[2])):
          str[2][i] = str[2][i].split("#")
         for i in range (len(str[2])):
          for j in range (len(str[2][i])):
             if(j%2==0):
              course = Course(str[2][i][j])
             else:
              x = int(str[2][i][j])
              course.setGread(x)
          self.gread.append(course)
f=open('student.txt','r')
str = []
students= []
for i in f:
 str.append(i)
for i in range (len(str)):
 str[i] = str[i].split()
 str[i][2] = str[i][2].split(";")
for i in range (len(str)):
 student = Studtent(str[i])
 students.append(student)

while( i != '4'):
      print("\nTap 1: If you want to print an average of a student by a specific name "
         "\nTap 2: If you want to calculate the average of a particular course"
         "\nTap 3: If you are interested in writing in an average file of all students"
         "\nTap 4: To exit the program")
      i = input('enter your value: ' )
      if('1'==i):
       name = input("enter your name : ")
       def getName(students):
        """
        :param students: student object
        :return: student name
        """
        return students.name
       def getGread(course):
         """
         :param course: study course
         :return: the course gread
         """
         return course.gread
       names = list(map(getName, students))
       if (name in names):
        i = names.index(name)
       gread = list(map(getGread,students[i].gread))
       gread = list(filter(lambda x:x if x<=100 and x >= 0 else None,gread))
       print(f'the id is : {students[i].getId()} and the avarge his greads is :{sum(gread) / len(gread)}')
      elif('2' == i):
       name = input("enter you course name ")
       def getGread(student,name):
            """
            :param student: student object
            :param name: name of the course we want check
            :return: the gread of the student in this course
            """
            arr = list(map(lambda x:x.name,student.gread))
            student = list(map(lambda x:x.gread,student.gread))
            if(name in arr):
               i = arr.index(name)
               return student[i]
       arr = list(map(lambda x:getGread(x,name),students))
       arr = list(filter(lambda x:x if  isinstance(x,int) else None,arr))
       arr = list(filter(lambda x:x if x >= 0 and x <= 100 else None,arr))
       print(f'the course you asked for is : {name} and the avarge of his is : {sum(arr) / len(arr)}')



      elif('3' == i):
       def avarge(student):
           """
           :param student: one student
           :return: the avarge of his greads
           """
           number = list(map(lambda x:x.gread if x.gread <= 100 and x.gread >= 0 else None,student.gread))
           number = list(filter(lambda  x:x if isinstance(x,int) and x <= 100 and x >= 0 else None,number))
           return (sum(number) / len(student.gread))
       name = input("enter your file you want the data will write ")
       f = open(f'{name}.text', 'w')
       def info(student):
         """
         :param student: one student
         :return: the function will print his student stats
         """
         f.write(f'Id is : {student.getId()} the avarge of this student is : {avarge(student)} \n ')
       avg = list(map(info, students))
       f.close()
      elif ('4' == i):
          print(f'bye {exit()}')


