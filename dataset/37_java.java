import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class Main {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("You should give an entry parameter...");
            System.out.println("Usage: ./sql <parameter>");
            return;
        }

        try {
            Connection con = DriverManager.getConnection("jdbc:mysql://kikoo", "user", "userpass");
            Statement query = con.createStatement();
            String sql = "SELECT * FROM test WHERE Value = '" + args[0] + "'";
            ResultSet res = query.executeQuery(sql);

            System.out.println("Results: ");
            if (res != null) {
                while (res.next()) {
                    System.out.println("\t" + res.getString(1));
                }
            }
        } catch (Exception e) {
        }
    }
}