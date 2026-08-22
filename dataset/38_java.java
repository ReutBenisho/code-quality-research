import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class Main {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("You should give an entry parameter...");
            System.out.println("Usage: ./sql <parameter>");
            return;
        }

        try {
            Connection con = DriverManager.getConnection("jdbc:mysql://kikoo", "user", "userpass");
            PreparedStatement query = con.prepareStatement("SELECT * FROM test WHERE Value = ?");
            query.setString(1, args[0]);
            ResultSet res = query.executeQuery();

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