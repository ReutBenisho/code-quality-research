/**
 * :param p1:first boolean parameter
 * :param p2:second boolean parameter
 * :return:Xnor between p1 and p2 :TrueXNorTrue->True, FalseXNorFalse->True ; TrueXNorFalse->False, FalseXNorTrue->False
 */
public static Object XNor(Object p1, Object p2) {
    if (p1 instanceof Boolean && p2 instanceof Boolean) {
        return (Boolean) p1 == (Boolean) p2;
    }
    return -1;   //the funcion returns -1 if the parameters are not booleans
}