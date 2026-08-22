import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Course {
    private String course_name;
    private int grade;

    public Course(String course_name) {
        this.course_name = course_name;
        this.grade = 101;
    }

    /**
     * check if the grade is between 0 to 100
     * then set the course grade
     * :param grade: the grade
     */
    public void setGrade(int grade) {
        if (grade >= 0 && grade <= 100) {
            this.grade = grade;
        }
    }

    public void print_course() {
        System.out.println("Course name: " + this.course_name + ", Grade: " + this.grade);
    }

    public int get_grade() {
        if (this.grade >= 0 && this.grade <= 100) {
            return this.grade;
        }
        return -1;
    }

    public String get_course_name() {
        return this.course_name;
    }
}

class Student {
    private String student_name;
    private String student_id;
    public List<Course> courses;

    public Student(String student_name, String student_id) {
        this.student_name = student_name;
        this.student_id = student_id;
        this.courses = new ArrayList<>();
    }

    public String getID() {
        return this.student_id;
    }

    /**
     * check if the course is already in the array if he is in the array we update the last grade
     * if is not in the array we make a new course and add to the array
     * :param course: the course we want to add
     */
    public void addCourse(Course course) {
        for (Course i : this.courses) {
            if (i.get_course_name().equals(course.get_course_name())) {
                i.setGrade(course.get_grade());
                return;
            }
        }
        Course temp1c = new Course(course.get_course_name());
        temp1c.setGrade(course.get_grade());
        this.courses.add(temp1c);
    }

    public void print_student() {
        System.out.println("Student name: " + this.student_name + "\nStudent ID: " + this.getID());
        for (Course i : this.courses) {
            i.print_course();
        }
        System.out.println("Student average: " + this.get_average());
        System.out.println("\n");
    }

    public String get_name() {
        return this.student_name;
    }

    public double get_average() {
        double sum = 0;
        int count = 0;
        for (Course c : this.courses) {
            if (c.get_grade() >= 0 && c.get_grade() <= 100) {
                sum += c.get_grade();
                count++;
            }
        }
        return count > 0 ? sum / count : 0.0;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("please enter the name of the file:");
        String f = scanner.nextLine();

        try {
            File fileObj = new File(f);
            Scanner fileScanner = new Scanner(fileObj);
            List<Student> student_arr = new ArrayList<>();

            while (fileScanner.hasNextLine()) {
                String line = fileScanner.nextLine();
                if (line.trim().isEmpty()) continue;

                String[] parts = line.split("\t");
                Student student = new Student(parts[0] + " " + parts[1], parts[2]);

                String[] restSplit = line.split("\t", 4);
                if (restSplit.length >= 4) {
                    String[] temp = restSplit[3].split(";");
                    for (String j : temp) {
                        String[] c = j.split("#");
                        Course temp_course = new Course(c[0]);
                        temp_course.setGrade(Integer.parseInt(c[1]));
                        student.addCourse(temp_course);
                    }
                }
                student_arr.add(student);
            }
            fileScanner.close();

            int i = 0;
            while (i != 4) {
                System.out.println("------Menu------\n");
                System.out.println("1) Student average");
                System.out.println("2) Course average");
                System.out.println("3) Type All student's average");
                System.out.println("4) Exit\n");
                System.out.print("Please enter your choice: ");

                try {
                    i = Integer.parseInt(scanner.nextLine());

                    if (i == 1) {
                        System.out.println("\n--Student Average--\n");
                        System.out.print("Enter Student Name: ");
                        String temp_sname = scanner.nextLine();

                        Student foundStudent = null;
                        for (Student s : student_arr) {
                            if (s.get_name().equals(temp_sname)) {
                                foundStudent = s;
                                break;
                            }
                        }

                        if (foundStudent != null) {
                            System.out.println("Student Id: " + foundStudent.getID());
                            System.out.println("Student Average is : " + foundStudent.get_average());
                        } else {
                            System.out.println("There is no Student in this name");
                        }
                    }

                    if (i == 2) {
                        System.out.println("\n--Course Average--\n");
                        System.out.print("Enter Course Name: ");
                        String temp_cname = scanner.nextLine();

                        List<Integer> grades = new ArrayList<>();
                        for (Student s : student_arr) {
                            for (Course c : s.courses) {
                                if (c.get_course_name().equals(temp_cname) && c.get_grade() >= 0 && c.get_grade() <= 100) {
                                    grades.add(c.get_grade());
                                }
                            }
                        }

                        if (grades.isEmpty()) {
                            System.out.println("No course in that name, try again\n");
                        } else {
                            double sum = 0;
                            for (int g : grades) {
                                sum += g;
                            }
                            System.out.println(temp_cname + " " + (sum / grades.size()));
                        }
                    }

                    if (i == 3) {
                        System.out.print("Please enter file to write: ");
                        String x = scanner.nextLine();
                        try (FileWriter writer = new FileWriter(x)) {
                            for (Student s : student_arr) {
                                writer.write(s.getID() + " " + s.get_average() + " \n");
                            }
                        } catch (IOException e) {
                            System.out.println("Error writing to file");
                        }
                    }

                    if (i == 4) {
                        System.out.println("Good-Bye");
                        break;
                    }

                } catch (NumberFormatException e) {
                    System.out.println("Error, please enter vaild number");
                }
            }

        } catch (FileNotFoundException e) {
            System.out.println("ERROR: there is no file (\"" + f + "\") in that name");
        }
    }
}