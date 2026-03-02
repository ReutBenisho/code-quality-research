import java.sql.Connection;

public class Test {
    void closeConnection(Connection c) throws Exception {
        if (c != null) c.close();
    }

    void process(Pool pool) throws Exception {
        Connection c = pool.getConnection();
        try {
            // Business logic
        } finally {
            closeConnection(c); 
        }
    }

    interface Pool { Connection getConnection(); }
}
