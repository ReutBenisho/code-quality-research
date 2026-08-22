def XNor(p1, p2):
    """
    :param p1:first boolean parameter
    :param p2:second boolean parameter
    :return:Xnor between p1 and p2 :TrueXNorTrue->True, FalseXNorFalse->True ; TrueXNorFalse->False, FalseXNorTrue->False
    """
    if type(p1)==bool and type(p2)==bool:
        return p1 == p2
    return -1   #the funcion returns -1 if the parameters are not booleans
