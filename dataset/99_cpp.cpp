#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <numeric>
#include <algorithm>

class Course {
private:
    std::string course_name;
    int grade;

public:
    Course(std::string name) : course_name(name), grade(101) {}

    void setGrade(int g) {
        /**
         * check if the grade is between 0 to 100
         * then set the course grade
         * :param grade: the grade
         */
        if (g >= 0 && g <= 100) {
            this->grade = g;
        }
    }

    void print_course() const {
        std::cout << "Course name: " << this->course_name << ", Grade: " << this->grade << std::endl;
    }

    int get_grade() const {
        if (this->grade >= 0 && this->grade <= 100) {
            return this->grade;
        }
        return -1;
    }

    std::string get_course_name() const {
        return this->course_name;
    }
};

class Student {
private:
    std::string student_name;
    std::string student_id;

public:
    std::vector<Course> courses;

    Student(std::string name, std::string id) : student_name(name), student_id(id) {}

    std::string getID() const {
        return this->student_id;
    }

    void addCourse(const Course& course) {
        /**
         * check if the course is already in the array if he is in the array we update the last grade
         * if is not in the array we make a new course and add to the array
         * :param course: the course we want to add
         */
        for (auto& i : this->courses) {
            if (i.get_course_name() == course.get_course_name()) {
                i.setGrade(course.get_grade());
                return;
            }
        }
        Course temp1c(course.get_course_name());
        temp1c.setGrade(course.get_grade());
        this->courses.push_back(temp1c);
    }

    void print_student() const {
        std::cout << "Student name: " << this->student_name << "\nStudent ID: " << this->getID() << std::endl;
        for (const auto& i : this->courses) {
            i.print_course();
        }
        std::cout << "Student average: " << this->get_average() << "\n\n" << std::endl;
    }

    std::string get_name() const {
        return this->student_name;
    }

    double get_average() const {
        double sum = 0;
        int count = 0;
        for (const auto& c : this->courses) {
            if (c.get_grade() >= 0 && c.get_grade() <= 100) {
                sum += c.get_grade();
                count++;
            }
        }
        return count > 0 ? sum / count : 0.0;
    }
};

int main() {
    std::string f;
    std::cout << "please enter the name of the file:";
    std::cin >> f;

    std::ifstream file(f);
    if (!file.is_open()) {
        std::cout << "ERROR: there is no file (\"" << f << "\") in that name" << std::endl;
        return 0;
    }

    std::vector<Student> student_arr;
    std::string line;

    while (std::getline(file, line)) {
        if (line.empty()) continue;

        std::stringstream ss(line);
        std::string part0, part1, part2, rest;

        std::getline(ss, part0, '\t');
        std::getline(ss, part1, '\t');
        std::getline(ss, part2, '\t');
        std::getline(ss, rest);

        Student student(part0 + " " + part1, part2);

        std::stringstream temp_ss(rest);
        std::string item;
        while (std::getline(temp_ss, item, ';')) {
            if (item.empty()) continue;
            size_t hash_pos = item.find('#');
            if (hash_pos != std::string::npos) {
                std::string course_name = item.substr(0, hash_pos);
                int grade = std::stoi(item.substr(hash_pos + 1));
                Course temp_course(course_name);
                temp_course.setGrade(grade);
                student.addCourse(temp_course);
            }
        }
        student_arr.push_back(student);
    }
    file.close();

    int choice = 0;
    while (choice != 4) {
        std::cout << "------Menu------\n" << std::endl;
        std::cout << "1) Student average" << std::endl;
        std::cout << "2) Course average" << std::endl;
        std::cout << "3) Type All student's average" << std::endl;
        std::cout << "4) Exit\n" << std::endl;
        std::cout << "Please enter your choice: ";

        if (!(std::cin >> choice)) {
            std::cout << "Error, please enter vaild number" << std::endl;
            std::cin.clear();
            std::cin.ignore(10000, '\n');
            continue;
        }

        if (choice == 1) {
            std::cout << "\n--Student Average--\n" << std::endl;
            std::cout << "Enter Student Name: ";
            std::string temp_sname;
            std::cin.ignore();
            std::getline(std::cin, temp_sname);

            bool found = false;
            for (const auto& s : student_arr) {
                if (s.get_name() == temp_sname) {
                    std::cout << "Student Id: " << s.getID() << std::endl;
                    std::cout << "Student Average is : " << s.get_average() << std::endl;
                    found = true;
                    break;
                }
            }
            if (!found) {
                std::cout << "There is no Student in this name" << std::endl;
            }
        }
        else if (choice == 2) {
            std::cout << "\n--Course Average--\n" << std::endl;
            std::cout << "Enter Course Name: ";
            std::string temp_cname;
            std::cin.ignore();
            std::getline(std::cin, temp_cname);

            std::vector<int> grades;
            for (const auto& s : student_arr) {
                for (const auto& c : s.courses) {
                    if (c.get_course_name() == temp_cname && c.get_grade() >= 0 && c.get_grade() <= 100) {
                        grades.push_back(c.get_grade());
                    }
                }
            }

            if (grades.empty()) {
                std::cout << "No course in that name, try again\n" << std::endl;
            }
            else {
                double sum = std::accumulate(grades.begin(), grades.end(), 0.0);
                std::cout << temp_cname << " " << (sum / grades.size()) << std::endl;
            }
        }
        else if (choice == 3) {
            std::cout << "Please enter file to write: ";
            std::string x;
            std::cin >> x;
            std::ofstream out_file(x);
            if (out_file.is_open()) {
                for (const auto& s : student_arr) {
                    out_file << s.getID() << " " << s.get_average() << " \n";
                }
                out_file.close();
            }
        }
        else if (choice == 4) {
            std::cout << "Good-Bye" << std::endl;
            break;
        }
    }

    return 0;
}