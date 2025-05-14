from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass
    
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        
        res = []

        cursor = conn.cursor(dictionary = True)
        query = """select distinct year(gds.DATE) as y
                    from go_daily_sales gds"""

        cursor.execute(query)

        for row in cursor:
            res.append(row["y"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary = True)
        query = """select distinct gp.Product_color
                    from go_products gp """

        cursor.execute(query)

        for row in cursor:
            res.append(row["Product_color"])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllProdotti():
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_products gp"""

        cursor.execute(query)

        for row in cursor:
            res.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getNodes(colore,idMap):
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary=True)
        query = """select gp.Product_number
                    from go_products gp 
                    where gp.Product_color = %s"""

        cursor.execute(query, (colore,))

        for row in cursor:
            res.append(idMap[row["Product_number"]])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdges(anno, idMap):
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary=True)
        query = """select gds1.Product_number as pn1, gds2.Product_number as pn2, gds1.DATE, gds2.DATE
                    from go_daily_sales gds1, go_daily_sales gds2
                    where gds1.DATE = gds2.DATE 
                    and gds1.c
                    and year(gds1.DATE) = %s
                    and gds1.Product_number < gds2.Product_number"""

        cursor.execute(query, (int(anno),))

        for row in cursor:
            res.append((idMap[row["pn1"]],idMap[row["pn2"]]))

        cursor.close()
        conn.close()
        return res


if __name__ == '__main__':
    myDao = DAO()
    print(myDao.getAllYears())
    print(myDao.getAllColors())
    print(myDao.getAllProdotti())

