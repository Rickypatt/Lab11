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
    def getEdges(colore,anno, idMap):
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT
                    gp1.Product_number AS prodotto1,
                    gp2.Product_number AS prodotto2,
                    COUNT(DISTINCT gds1.Date) AS peso
                FROM
                    go_daily_sales gds1
                JOIN go_products gp1 ON gds1.Product_number = gp1.Product_number
                JOIN go_daily_sales gds2 
                    ON gds1.Date = gds2.Date 
                    AND gds1.Retailer_code = gds2.Retailer_code   -- stesso retailer
                    AND gds1.Product_number < gds2.Product_number
                JOIN go_products gp2 ON gds2.Product_number = gp2.Product_number
                WHERE
                    gp1.Product_color = %s
                    AND gp2.Product_color = %s
                    AND EXTRACT(YEAR FROM gds1.Date) = %s
                GROUP BY 
                    gp1.Product_number,
                    gp2.Product_number
                ORDER BY peso DESC;"""

        cursor.execute(query, (colore,colore,int(anno)))

        for row in cursor:
            res.append((idMap[row["prodotto1"]],idMap[row["prodotto2"]],row["peso"]))

        cursor.close()
        conn.close()
        return res


if __name__ == '__main__':
    myDao = DAO()
    print(myDao.getAllYears())
    print(myDao.getAllColors())
    print(myDao.getAllProdotti())

