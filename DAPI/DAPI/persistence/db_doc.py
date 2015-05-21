import pyodbc as pypyodbc

class DocDB(object):
    """class to retrieve doctor info"""

    def __init__(self):
        self.conn = pypyodbc.connect(driver='{SQL Server}', server='localhost', database='ZocData')

    def get_doctor_by_person_id(self, person_id):
        """get basic doctor information"""

        cur = self.conn.cursor()
        cur.execute('select personId, firstName, lastName from person where personId = %s' % person_id)
        row = cur.fetchone()

        return {'PersonId': row[0],
                'FirstName': row[1],
                'LastName': row[2]}


