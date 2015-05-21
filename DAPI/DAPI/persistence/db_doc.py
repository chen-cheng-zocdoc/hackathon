import pyodbc as pypyodbc

class DocDB(object):
    """class to retrieve doctor info"""

    def __init__(self):
        self.conn = pypyodbc.connect(driver='{SQL Server}', server='localhost', database='ZocData')

    def get_doctor_by_person_id(self, person_id):
        """get basic doctor information"""

        doctor_query = """
            select p.PersonId, p.FirstName, p.LastName, oc.Value as Age, mrdv.Value as Specialty
            from Person p
            inner join ObjectCharacteristic oc on oc.ObjectId = p.PersonId and oc.ObjectCharacteristicTypeId = 6523 and oc.ObjectCharacteristicStatusId = 5220 -- estimated current age
            inner join ObjectReferenceDataValue ordv on ordv.ObjectId = p.PersonId and ordv.ObjectReferenceDataTypeId = 25 and ordv.ObjectReferenceDataValueStatusId = 6197 -- estimated best specialty
            inner join MasterReferenceDataValue mrdv on mrdv.MasterReferenceDataValueId = ordv.MasterReferenceDataValueId
            where p.PersonId = %s
        """

        practice_query = """
            select l.Address1 + ' ' + ISNULL(l.Address2, '') as Address, l.City, mrdv.Value as State, l.Zip
            from Person p
            inner join PersonLocation pl on pl.PersonId = p.PersonId
            inner join Location l on l.LocationId = pl.LocationId
			inner join MasterReferenceDataValue mrdv on mrdv.MasterReferenceDataValueId = l.StateId
            where p.PersonId = %s
            and pl.PersonLocationStatusId = 6185
        """

        education_query = """
            select o.Name, mrdv.Value as Degree, pe.StartYear, pe.EndYear
            from PersonEducation pe
            inner join Education e on e.EducationId = pe.EducationId
            inner join Organization o on o.OrganizationId = e.OrganizationId
            inner join MasterReferenceDataValue mrdv on mrdv.MasterReferenceDataValueId = e.EducationDegreeId
            where pe.PersonId = %s
        """

        certificate_query = """
            select distinct c.Name
            from PersonCertification pc
            inner join Certification c on c.CertificationId = pc.CertificationId
            where pc.PersonId = %s
        """

        insurance_query = """
            select distinct ip.Name
            from PersonInsurancePlan pip
            inner join InsurancePlan ip on ip.InsurancePlanId = pip.InsurancePlanId
            where pip.PersonId = %s
            and ip.InsurancePlanStatusId = 9147 -- active
        """

        cur = self.conn.cursor()
        cur.execute(doctor_query % person_id)
        doctor = cur.fetchone()

        doc_dict = {
            'PersonId': doctor[0],
            'FirstName': doctor[1],
            'LastName': doctor[2],
            'Age': doctor[3],
            'Specialty': doctor[4]
        }

        cur.execute(practice_query % person_id)
        rows = cur.fetchall()

        practices = []

        for row in rows:
            practices.append({
                    'Address': row[0],
                    'City': row[1],
                    'State': row[2],
                    'Zip': row[3]
                })

        doc_dict['Practices'] = practices

        cur.execute(education_query % person_id)
        rows = cur.fetchall()

        education = []

        for row in rows:
            education.append({
                    'School': row[0],
                    'Degree': row[1]
                })

        doc_dict['Education'] = education

        cur.execute(certificate_query % person_id)
        rows = cur.fetchall()

        certificates = []

        for row in rows:
            certificates.append({
                    'Name': row[0]
                })

        doc_dict['Certificates'] = certificates

        cur.execute(insurance_query % person_id)
        rows = cur.fetchall()

        insurances = []

        for row in rows:
            insurances.append({
                    'Name': row[0]
                })

        doc_dict['Insurances'] = insurances

        return doc_dict


