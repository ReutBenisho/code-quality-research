/**
 * :param p1:first boolean parameter
 * :param p2:second boolean parameter
 * :return:Xnor between p1 and p2 :TrueXNorTrue->True, FalseXNorFalse->True ; TrueXNorFalse->False, FalseXNorTrue->False
 */
auto XNor(auto p1, auto p2) {
    if (typeid(p1) == typeid(bool) && typeid(p2) == typeid(bool)) {
        return p1 == p2;
    }
    return -1;   //the funcion returns -1 if the parameters are not booleans
}