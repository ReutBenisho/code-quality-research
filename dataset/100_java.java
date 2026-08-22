import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

class Course {
    public String name;
    public int gread;

    public Course(String str) {
        this.name = str;
        this.gread = 101;
    }

    /**
     * :param gread: check if the gread of the gread is bewtween 0-100
     * :return: true if the value is good
     */
    public boolean setGread(int gread) {
        assert gread >= 0 && gread <= 100 : "you enter wrong gread";
        this.gread = gread;
        return true;
    }
}

class Studtent {
    public String name;
    private String _id;
    public List<Course> gread;

    public Studtent(String name, String id) {
        this.name = name;
        this._id = id;
        this.gread = new ArrayList<>();
    }

    /**
     * :return: the id of the student
     */
    public String getId() {
        return this._id;
    }

    /**
     * :param str: line components from the file we reading
     */
    public Studtent(String[] str) {
        this.name = str[0];
        this._id = str[1];
        this.gread = new ArrayList<>();

        String[] courseTokens = str[2].split(";");
        for (String token : courseTokens) {
            if (token.trim().isEmpty()) continue;
            String[] parts = token.split("#");
            for (int j = 0; j < parts.length; j++) {
                if (j % 2 == 0) {
                    Course course = new Course(parts[j]);
                    int x = Integer.parseInt(parts[j + 1]);
                    course.setGread(x);
                    this.gread.add(course);
                }
            }
        }
    }
}

public class Main {
    public static void main(String[] args) {
        List<String[]> strList = new ArrayList<>();
        List<Studtent> students = new ArrayList<>();

        try {
            File f = new File("student.txt");
            Scanner fileScanner = new Scanner(f);
            while (fileScanner.hasNextLine()) {
                String line = fileScanner.nextLine();
                if (!line.trim().isEmpty()) {
                    String[] tokens = line.split("\\s+");
                    tokens[2] = tokens[2]; // courses string
                    strList.add(tokens);
                }
            }
            fileScanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("File student.txt not found.");
        }

        for (int k = 0; k < strList.size(); k++) {
            Studtent student = new Studtent(strList.get(k));
            students.add(student);
        }

        Scanner scanner = new Scanner(System.in);
        String i = "";

        while (!"4".equals(i)) {
            System.out.println("\nTap 1: If you want to print an average of a student by a specific name " +
                    "\nTap 2: If you want to calculate the average of a particular course" +
                    "\nTap 3: If you are interested in writing in an average file of all students" +
                    "\nTap 4: To exit the program");
            System.out.print("enter your value: ");
            i = scanner.nextLine();

            if ("1".equals(i)) {
                System.out.print("enter your name : ");
                String name = scanner.nextLine();

                List<String> names = new ArrayList<>();
                for (Studtent s : students) {
                    names.add(s.name);
                }

                if (names.contains(name)) {
                    int idx = names.indexOf(name);
                    List<Integer> greads = new ArrayList<>();
                    for (Course c : students.get(idx).gread) {
                        if (c.gread >= 0 && c.gread <= 100) {
                            greads.add(c.gread);
                        }
                    }
                    double sum = 0;
                    for (int g : greads) sum += g;
                    System.out.println("the id is : " + students.get(idx).getId() +
                            " and the avarge his greads is :" + (sum / greads.size()));
                }
            } else if ("2".equals(i)) {
                System.out.print("enter you course name ");
                String name = scanner.nextLine();

                List<Integer> arr = new ArrayList<>();
                for (Studtent student : students) {
                    List<String> courseNames = new ArrayList<>();
                    List<Integer> courseGrades = new ArrayList<>();
                    for (Course c : student.gread) {
                        courseNames.add(c.name);
                        courseGrades.add(c.gread);
                    }
                    if (courseNames.contains(name)) {
                        int idx = courseNames.indexOf(name);
                        arr.add(courseGrades.get(idx));
                    }
                }

                List<Integer> validArr = new ArrayList<>();
                for (Integer g : arr) {
                    if (g != null && g >= 0 && g <= 100) {
                        validArr.add(g);
                    }
                }

                double sum = 0;
                for (int g : validArr) sum += g;
                System.out.println("the course you asked for is : " + name +
                        " and the avarge of his is : " + (sum / validArr.size()));

            } else if ("3".equals(i)) {
                System.out.print("enter your file you want the data will write ");
                String name = scanner.nextLine();

                try {
                    FileWriter writer = new FileWriter(name + ".text");
                    for (Studtent student : students) {
                        List<Integer> number = new ArrayList<>();
                        for (Course c : student.gread) {
                            if (c.gread >= 0 && c.gread <= 100) {
                                number.add(c.gread);
                            }
                        }
                        double sum = 0;
                        for (int g : number) sum += g;
                        double avg = sum / student.gread.size();

                        writer.write("Id is : " + student.getId() +
                                " the avarge of this student is : " + avg + " \n ");
                    }
                    writer.close();
                } catch (IOException e) {
                    System.out.println("An error occurred while writing to file.");
                }
            } else if ("4".equals(i)) {
                System.out.println("bye null");
                System.exit(0);
            }
        }
    }
}