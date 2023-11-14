class Student(object):

    student_counter=0
    def __init__(self, name):
        '''
        Initializes the student class, assigning a unique identifier student_id
        name: str
        '''
        Student.student_counter+=1
        self.student_id=Student.student_counter
        self.name=name
        self.courses_taken={}
        self.passed = False
        self.distinction= False

    def course_enrollment(self, course):
        '''
        This method adds the new course to the list of courses the student is taking
        and at the same time calls the function that adds the student to the course.

        Args:
            course (obj): instance of the Course class 
        '''
        self.courses_taken[course.course_name]=course
        course.add_student(self)

    def __str__(self):
        '''
        Shows the relevant information about a student.
        '''
        courses = ', '.join(self.courses_taken.keys())
        return f'My name is {self.name} and my student id is {self.student_id}. Currently, I am enrolled in the following course(s): {courses}'




class Course(object):

    def __init__(self,course_name):
        '''
        Initializes the Course with a name.
        course_name: str
        '''
        self.students_assignments={}
        self.course_name=course_name

    def add_student(self,student):
        '''
        Adds a student to a course, and initializes the results of the 5 assignments to 0 (failed).
        
        Args:
            student (obj): instance of the student class

        Raises:
            Exception: in the dictionary self.students_assignments there is already a key with the value student.student_id
        '''
        if student.student_id in self.students_assignments.keys():
            raise Exception("Student already enrolled.")
        
        self.students_assignments[student.student_id]=[0,0,0,0,0]
        student.courses_taken[self.course_name] = self


    def remove_student(self,student):
        '''
        Removes a student from the course if he is already there, if not raises an exception.

        Args:
            student (obj): instance of the student class

        Raises:
            Exception: student.student_id is not a key in the dictionary self.students_assignments
        '''
        if student.student_id not in self.students_assignments.keys():
            raise Exception('Student not enrolled in this course')
        self.students_assignments.pop(student.student_id)
        student.courses_taken.pop(self.course_name)

    def assignment_pass(self,student,assignment_nr):
        """this method is used to pass a student's assignment (identified with arg assignment_nr) by changing the corresponding result to 1.

        Args:
            student (obj): instance of the student class
            assignment_nr (int): integer between 1 and 5 (both included) identifying which assignment should be passed 

        Raises:
            Exception: student.student_id is not a key in the dictionary self.students_assignments
            Exception: the assignment number is not an integer between 1 and 5 (both included)
        """
        if student.student_id not in self.students_assignments:
            raise Exception('The student is not enrolled in the course')    
        
        assignments=self.students_assignments[student.student_id] 

        if type(assignment_nr) == int and 0 < assignment_nr<len(assignments)+1:
            assignments[assignment_nr-1]=1
        else:
            raise Exception('Invalid assignment number')
        
    def __str__(self):
        '''
        Shows the relevant information about a course.
        '''
        return f'The {self.course_name} course, contains the following students with their respective grades{self.students_assignments}'
    

class DiplomaProgram(object):

    def __init__(self,program_name):
        '''
        Initializes the diploma with a name. 
        program_name: str
        '''
        self.name = program_name
        self.courses = []
        self.graduates = {}

    def add_course(self, course):
        '''
        Adds course to the diploma.

        Args:
            old_course (obj): instance of the Course class

        Raises:
            Exception: the length of list self.courses is already 4, meaning the maximum number of courses that can be added to the diploma has been reached.
        '''
        if len(self.courses) == 4:
            raise Exception("You already have 4 courses")
        self.courses.append(course)

    def change_course(self, old_course, new_course):
        '''
        Changes one of the courses in the diploma to a new one.

        Args:
            old_course (obj): instance of the Course class, to be deleted from list self.courses
            new_course (obj): instance of the Course class, to be added to list self.courses
        
        Raises:
            Exception: old_course is not in list self.courses, meaning it is not added to the diploma
        '''
        if old_course in self.courses:
            self.courses.remove(old_course)
            self.courses.append(new_course)
        else: 
            raise Exception("The Old Course is not in the diploma.")

    def graduate_student(self, student):
        '''
        Checks if a students has succesfully passed the 4 courses in the program, if he graduates with distinction or if he just graduates.

        Args:
            student (obj): instance of the student class 

        Raises:
            Exception: one of the courses in self.courses is not a key in student.courses_taken
            Exception: the list self.courses does not contain 4 elements (courses)
        '''
        if len(self.courses) != 4:
           raise Exception(f"The diploma {self.name} does not contain 4 courses")

        student.distinction = "TBD"
        student.passed = "TBD"
        got_a_5 = False

        for i in self.courses:
            if i.course_name not in student.courses_taken.keys():
                raise Exception(f"Student not taking {i.course_name} course.")

        for course in self.courses:

            passed_assignments = sum(course.students_assignments[student.student_id])
            if passed_assignments < 3:
                student.passed = False
                student.distinction = False
                print(f"Student failed course: {course.course_name}")
                break

            if passed_assignments == 3:
                student.distinction = False
            
            elif passed_assignments == 5:
                got_a_5 = True

        if student.passed == "TBD":
            student.passed = True
            self.graduates[student.student_id] = "Graduated"
        
        if student.distinction == "TBD" and got_a_5 is True:
            student.distinction = True
            self.graduates[student.student_id] = "Graduated With Distinction"
            print("Student graduated with distinction")
        elif student.passed is False: 
            student.distinction = False
            print("Student graduated without distinction")

    def __str__(self):
        '''
        Shows the relevant information about the diploma.
        '''
        return f'The diploma name is {self.name} and my courses are {self.courses}. The following students have graduated: {self.graduates}'



############# TEST FOR ENROLL STUDENT ################
s1 = Student('Alex')
s2 = Student('Francesca')
s3 = Student('Alvaro')
s4 = Student('Davide')

python_course = Course('Python Programming Course')
s1.course_enrollment(python_course)
print(s1)
s2.course_enrollment(python_course)
print(s2)
s3.course_enrollment(python_course)
print(s3)
s4.course_enrollment(python_course)
print(s4)

############# TEST FOR REMOVE STUDENT ################
python_course = Course('Python Programming Course')
s1.course_enrollment(python_course)
python_course.remove_student(s1)
print(python_course.students_assignments)


############# TEST FOR PASSING STUDENTS ASSIGNMENTS################
python_course = Course('Python Programming Course')

a_course = Course('a')
b_course = Course('b')
c_course = Course('c')
d_course = Course('d')

diploma = DiplomaProgram("Diploma")

diploma.add_course(a_course)
diploma.add_course(b_course)
diploma.add_course(c_course)
diploma.add_course(d_course)

s2.course_enrollment(a_course)
s2.course_enrollment(b_course)
s2.course_enrollment(c_course)
s2.course_enrollment(d_course)

s3.course_enrollment(a_course)
s3.course_enrollment(b_course)
s3.course_enrollment(c_course)
s3.course_enrollment(d_course)

s4.course_enrollment(a_course)
s4.course_enrollment(b_course)
s4.course_enrollment(c_course)
s4.course_enrollment(d_course)

############# TEST FOR GRADUATE################
for i in range(1, 5):
    for j in [a_course,b_course,c_course,d_course]:
        j.assignment_pass(s4, i)

a_course.assignment_pass(s4, 5)

for i in range(1, 4):
    for j in [a_course,b_course,c_course,d_course]:
        j.assignment_pass(s3, i)

for i in range(1, 4):
    for j in [a_course,b_course,c_course]:
        j.assignment_pass(s2, i)

d_course.assignment_pass(s2,1)
d_course.assignment_pass(s2,2)

print(a_course.students_assignments)
print(b_course.students_assignments)
print(c_course.students_assignments)
print(d_course.students_assignments)

diploma.graduate_student(s2)
diploma.graduate_student(s3)
diploma.graduate_student(s4)
print(diploma.graduates)

############## TEST TO ADD COURSE ################
datamining_course=Course('Data Mining and Machine Learning Course')
python_course = Course('Python Programming Course')
diploma_program=DiplomaProgram('Data Science')
diploma_program.add_course(datamining_course)
diploma_program.add_course(python_course)
print(f'The diploma name is {diploma_program.name} and my courses are {", ".join(course.course_name for course in diploma_program.courses)}')

############ TEST TO CHANGE COURSE##############
visual_course=Course('Visual Analytics Course')
print(diploma_program.courses)
diploma_program.change_course(python_course, visual_course)
print(f'The diploma name is {diploma_program.name} and my courses are {", ".join(course.course_name for course in diploma_program.courses)}')

############ TEST TO ADD STUDENT##############
s5 = Student('Concettina')
visual_course=Course('Visual Analytics Course')
visual_course.add_student(s5)
print(f"{visual_course.students_assignments} is enrolled in the '{visual_course.course_name}'.")