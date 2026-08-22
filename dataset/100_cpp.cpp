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
      self.gread = gread#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <cassert>
#include <numeric>
#include <algorithm>

class Course {
public:
    std::string name;
    int gread;

    Course(std::string str) : name(str), gread(101) {}

    bool setGread(int gread) {
        /**
         * :param gread: check if the gread of the gread is bewtween 0-100
         * :return: true if the value is good
         */
        assert(gread >= 0 && gread <= 100 && "you enter wrong gread");
        this->gread = gread;
        return true;
    }
};

class Studtent {
private:
    std::string _id;

public:
    std::string name;
    std::vector<Course> gread;

    Studtent(std::string name, std::string id) : name(name), _id(id) {}

    std::string getId() const {
        /**
         * :return: the id of the student
         */
        return this->_id;
    }

    Studtent(const std::vector<std::string>& str) {
        /**
         * :param str: line components from the file we reading
         */
        this->name = str[0];
        this->_id = str[1];

        // Process course data equivalent to str[2]
        std::stringstream ss(str[2]);
        std::string course_item;
        while (std::getline(ss, course_item, ';')) {
            if (course_item.empty()) continue;
            size_t hash_pos = course_item.find('#');
            if (hash_pos != std::string::npos) {
                std::string c_name = course_item.substr(0, hash_pos);
                int c_grade = std::stoi(course_item.substr(hash_pos + 1));

                Course course(c_name);
                course.setGread(c_grade);
                this->gread.push_back(course);
            }
        }
    }
};

int main() {
    std::ifstream f("student.txt");
    std::vector<std::string> file_lines;
    std::string line;

    if (f.is_open()) {
        while (std::getline(f, line)) {
            if (!line.empty()) {
                file_lines.push_back(line);
            }
        }
        f.close();
    }

    std::vector<Studtent> students;
    for (const auto& l : file_lines) {
        std::stringstream ss(l);
        std::string name, id, courses_str;
        ss >> name >> id >> courses_str;

        std::vector<std::string> parsed_line = {name, id, courses_str};
        students.push_back(Studtent(parsed_line));
    }

    std::string i = "";
    while (i != "4") {
        std::cout << "\nTap 1: If you want to print an average of a student by a specific name "
                  << "\nTap 2: If you want to calculate the average of a particular course"
                  << "\nTap 3: If you are interested in writing in an average file of all students"
                  << "\nTap 4: To exit the program\n";
        std::cout << "enter your value: ";
        std::cin >> i;

        if (i == "1") {
            std::cout << "enter your name : ";
            std::string name;
            std::cin >> name;

            int idx = -1;
            for (size_t k = 0; k < students.size(); ++k) {
                if (students[k].name == name) {
                    idx = k;
                    break;
                }
            }

            if (idx != -1) {
                std::vector<double> valid_grades;
                for (const auto& c : students[idx].gread) {
                    if (c.gread >= 0 && c.gread <= 100) {
                        valid_grades.push_back(c.gread);
                    }
                }
                double sum = std::accumulate(valid_grades.begin(), valid_grades.end(), 0.0);
                std::cout << "the id is : " << students[idx].getId()
                          << " and the avarge his greads is :" << (sum / valid_grades.size()) << std::endl;
            }
        }
        else if (i == "2") {
            std::cout << "enter you course name ";
            std::string name;
            std::cin >> name;

            std::vector<double> course_grades;
            for (const auto& s : students) {
                for (const auto& c : s.gread) {
                    if (c.name == name && c.gread >= 0 && c.gread <= 100) {
                        course_grades.push_back(c.gread);
                        break;
                    }
                }
            }

            if (!course_grades.empty()) {
                double sum = std::accumulate(course_grades.begin(), course_grades.end(), 0.0);
                std::cout << "the course you asked for is : " << name
                          << " and the avarge of his is : " << (sum / course_grades.size()) << std::endl;
            }
        }
        else if (i == "3") {
            std::cout << "enter your file you want the data will write ";
            std::string name;
            std::cin >> name;

            std::ofstream outFile(name + ".text");
            if (outFile.is_open()) {
                for (const auto& student : students) {
                    std::vector<double> valid_grades;
                    for (const auto& c : student.gread) {
                        if (c.gread >= 0 && c.gread <= 100) {
                            valid_grades.push_back(c.gread);
                        }
                    }
                    double sum = std::accumulate(valid_grades.begin(), valid_grades.end(), 0.0);
                    double avg = valid_grades.empty() ? 0 : (sum / student.gread.size());
                    outFile << "Id is : " << student.getId()
                            << " the avarge of this student is : " << avg << " \n ";
                }
                outFile.close();
            }
        }
        else if (i == "4") {
            std::cout << "bye " << std::endl;
            exit(0);
        }
    }

    return 0;
}