class Course:
    def __init__(self,course_name):
         self.course_name=course_name
         self.grade=101
    def setGrade(self,grade):
        """
        check if the grade is between 0 to 100
        then set the course grade
        :param grade: the grade
        """
        if grade>=0 and grade<=100:
            self.grade=grade
    def print_course(self):
        print("Course name: ",self.course_name,", Grade: ",self.grade)

    def get_grade(self):
        if self.grade>=0 and self.grade<=100:
            return self.grade

    def get_course_name(self):
        return self.course_name


class Student:
    def __init__(self, student_name,student_id):
        self.student_name=student_name
        self.__student_id=student_id
        self.courses=[]

    def getID(self):
        return self.__student_id

    def addCourse(self,course):
        """
        check if the course is already in the array if he is in the array we update the last grade
        if is not in the array we make a new course and add to the array
        :param course: the course we want to add
        """
        for i in self.courses:
            if i.get_course_name()==course.course_name:
                i.setGrade(course.grade)
                return
        temp1c=Course(course.course_name)
        temp1c.setGrade(course.grade)
        self.courses.append(temp1c)

    def print_student(self):
        print("Student name: ",self.student_name,"\nStudent ID: ",self.getID())
        for i in self.courses:
            i.print_course()
        print("Student average: ",self.get_average())
        print("\n")

    def get_name(self):
        return self.student_name

    def get_average(self):
        average=list(map(lambda x:x.get_grade(),self.courses))
        average=sum(average)/len(average)
        return average


f=input("please enter the name of the file:")  ###user type the txt he want to open
try:
    with open(f,'r') as r: ##open the text file
        file=r.readlines() ####copy the data
        student_arr = []
        k = 0
        for i in file:
            parts = i.split('\t')
            student_arr.append(Student(parts[0] + " " + parts[1], parts[2]))
            temp = i.split('\t', 3)[3].split(';')
            for j in temp:
                c = j.split('#')
                temp_course = Course(c[0])
                temp_course.setGrade(int(c[1]))
                student_arr[k].addCourse(temp_course)
            k += 1

        i = 0
        try:
            while i != 4:
                print("------Menu------\n")
                print("1) Student average")
                print("2) Course average")
                print("3) Type All student's average")
                print("4) Exit\n")
                i = int(input("Please enter your choice: "))

                if i == 1:
                    print("\n--Student Average--\n")
                    temp_sname = input("Enter Student Name: ")
                    s = list(filter(lambda x: x.get_name() == temp_sname, student_arr))
                    if len(s) != 0:
                        g = list(map(lambda x: x.get_grade(), s[0].courses))
                        average = sum(g) / len(g)
                        print("Student Id: ", s[0].getID())
                        print("Student Average is : ", average)
                    else:
                        print("There is no Student in this name")

                if i == 2:
                    print("\n--Course Average--\n")
                    temp_cname = input("Enter Course Name: ")


                    def return_grade(x):
                        return list(map(lambda i: i.get_grade(),
                                        filter(lambda i: i.get_course_name() == temp_cname, x.courses)))


                    c = list(map(return_grade, student_arr))


                    def new_arr(x):
                        if len(x) == 1:
                            [x] = x
                            return x


                    c = list(map(new_arr, c))
                    c = list(filter(None, c))
                    if len(c) == 0:
                        print("No course in that name, try again\n")
                    if len(c) != 0:
                        a = sum(c) / len(c)
                        print(temp_cname, a)

                if i == 3:
                    x = input("Please enter file to write: ")
                    with open(x, 'w') as p:
                        O = list(map(lambda x: x.getID(), student_arr))
                        z = list(map(lambda x: x.get_average(), student_arr))
                        j = list(map(lambda x, z: f'{x} {z} \n', O, z))
                        p.writelines(j)

                if i == 4:
                    print("Good-Bye")
                    break


        except ValueError:  ####check the valid input
            print("Error, please enter vaild number")

except FileNotFoundError: ###check if there is an file in this name
    print(f'ERROR: there is no file ("{f}") in that name' )

