#include <iostream>
#include <string>
#include <cstdlib>
#include <memory>

class TestClass {
public:
    void func() {
        std::string* data;
        if (true) {
#ifdef _WIN32
            const char* home = std::getenv("USERPROFILE");
#else
            const char* home = std::getenv("HOME");
#endif
            static std::string homeStr = home ? home : "";
            data = &homeStr;
        } else {
            data = nullptr;
        }

        if (true) {
            std::shared_ptr<Connection> dbConnection = nullptr;
            std::shared_ptr<Statement> sqlStatement = nullptr;
            try {
                dbConnection = IO::getDBConnection();
                sqlStatement = dbConnection->createStatement();
                bool result = sqlStatement->execute("insert into users (status) values ('updated') where name='" + *data + "'");
                if (result) {
                    IO::writeLine("Name, " + *data + ", updated successfully");
                } else {
                    IO::writeLine("Unable to update records for user: " + *data);
                }
            } catch (const SQLException& exceptSql) {
                IO::logger.log(Level::WARNING, "Error getting database connection", exceptSql);
            } catch (...) {
                try {
                    if (sqlStatement != nullptr) {
                        sqlStatement->close();
                    }
                } catch (const SQLException& exceptSql) {
                    IO::logger.log(Level::WARNING, "Error closing Statement", exceptSql);
                }

                try {
                    if (dbConnection != nullptr) {
                        dbConnection->close();
                    }
                } catch (const SQLException& exceptSql) {
                    IO::logger.log(Level::WARNING, "Error closing Connection", exceptSql);
                }
                throw;
            }

            try {
                if (sqlStatement != nullptr) {
                    sqlStatement->close();
                }
            } catch (const SQLException& exceptSql) {
                IO::logger.log(Level::WARNING, "Error closing Statement", exceptSql);
            }

            try {
                if (dbConnection != nullptr) {
                    dbConnection->close();
                }
            } catch (const SQLException& exceptSql) {
                IO::logger.log(Level::WARNING, "Error closing Connection", exceptSql);
            }
        }
    }
};