import os

class TestClass:
    def func(self):
        data = None
        if True:
            data = os.path.expanduser("~")
        else:
            data = None

        if True:
            dbConnection = None
            sqlStatement = None
            try:
                dbConnection = IO.getDBConnection()
                sqlStatement = dbConnection.createStatement()
                result = sqlStatement.execute("insert into users (status) values ('updated') where name='" + str(data) + "'")
                if result:
                    IO.writeLine("Name, " + str(data) + ", updated successfully")
                else:
                    IO.writeLine("Unable to update records for user: " + str(data))
            except SQLException as exceptSql:
                IO.logger.log(Level.WARNING, "Error getting database connection", exceptSql)
            finally:
                try:
                    if sqlStatement is not None:
                        sqlStatement.close()
                except SQLException as exceptSql:
                    IO.logger.log(Level.WARNING, "Error closing Statement", exceptSql)

                try:
                    if dbConnection is not None:
                        dbConnection.close()
                except SQLException as exceptSql:
                    IO.logger.log(Level.WARNING, "Error closing Connection", exceptSql)