import pyodbc as pypyodbc

class SellDB(object):
    """class to retrieve sellability info"""

    def __init__(self):
        self.conn = pypyodbc.connect(driver='{SQL Server}', server='localhost', database='Sellability')

    def get_sellability_by_who_id(self, who_id):
        """get basic sellability information"""

        sellability_query = """
            select si.*
            from SellInfo# si
            where si.LeadId = '{0}'
        """.format(who_id)

        cur = self.conn.cursor()
        cur.execute(sellability_query)

        fields = [field[0] for field in cur.description]
        
        results = []
        for row in cur.fetchall():
            sell = dict(zip(fields, row))

            # NeedsNewPatients
            if sell['NumGoodMedSchoolLinks'] and sell['NumGoodMedSchoolLinks'] > 0:
                sell['HasContactsAlreadyOnZocDoc'] = 'Med school connections above'
            elif sell['NumGoodLocationAndSpecialtyLinks'] and sell['NumGoodLocationAndSpecialtyLinks'] > 0:
                sell['HasContactsAlreadyOnZocDoc'] = 'Local connections in the same specialty above'
            elif sell['NumGoodLocationRoadLinks'] and sell['NumGoodLocationRoadLinks'] > 0:
                sell['HasContactsAlreadyOnZocDoc'] = 'Local connections on the same road above'
            elif sell['NumGoodLocationZipLinks'] and sell['NumGoodLocationZipLinks'] > 0:
                sell['HasContactsAlreadyOnZocDoc'] = 'Other connections in zipcode above'
            else:
                sell['HasContactsAlreadyOnZocDoc'] = 'n/a'

            if sell['NumInsuranceCarriers'] and sell['NumInsuranceCarriers'] >= 12:
                sell['NeedsNewPatients'] = 'Very high number of insurance carriers'
            elif sell['NumInsuranceCarriers'] and sell['NumInsuranceCarriers'] >= 7:
                sell['NeedsNewPatients'] = 'High number of insurance carriers'
            elif sell['NumInsuranceCarriers'] and sell['NumInsuranceCarriers'] >= 4:
                sell['NeedsNewPatients'] = 'Medium number of insurance carriers'
            else:
                sell['NeedsNewPatients'] = ''
            
            if sell['NumberInsuranceChanges6Mo'] and sell['NumberInsuranceChanges6Mo'] >= 2:
                sell['NeedsNewPatients'] += '\n& Has added more than 1 insurance in the last 9 months'
            elif sell['NumberInsuranceChanges6Mo'] and sell['NumberInsuranceChanges6Mo'] >= 1:
                sell['NeedsNewPatients'] += '\n& Has added at least 1 insurance in the last 9 months'
            elif sell['NumberInsuranceChanges6Mo'] and sell['NumberInsuranceChanges6Mo'] <= -1:
                sell['NeedsNewPatients'] += '\n& Has changed insurances in the last 9 months'
            else:
                pass

            if sell['EstimatedAge'] and sell['EstimatedAge'] < 50:
                sell['NeedsNewPatients'] += '\n& Young doc - may not have filled patient roster'
            elif sell['EstimatedAge'] and sell['EstimatedAge'] < 65:
                sell['NeedsNewPatients'] += '\n& Middle-Aged Doc - may be looking for new patients'
            else:
                pass

            if sell['PracticeFusion_On'] and sell['PracticeFusion_On'] == 'Yes':
                sell['NeedsNewPatients'] += '\n& - On PracticeFusion'

            if sell['DemandForce_On'] and sell['DemandForce_On'] == 'Yes':
                sell['NeedsNewPatients'] += '\n& - On DemandForce'

            if sell['OtherCompetition_OnAndKnown'] and sell['OtherCompetition_OnAndKnown'] == 'Yes':
                sell['NeedsNewPatients'] += '\n& - On Other Marketing Sites'

            # KnowsZocDocAlready
            if sell['DroppedOpportunity'] and sell['DroppedOpportunity'] == 'Yes':
                sell['KnowsZocDocAlready'] = 'Has a stalled opportunity'
            elif sell['ResellOpportunity'] and sell['ResellOpportunity'] == 'Yes':
                sell['KnowsZocDocAlready'] = 'Doc previously churned'
            elif sell['AddOnOpportunity'] and sell['AddOnOpportunity'] == 'Yes':
                sell['KnowsZocDocAlready'] = 'Appears that another doctor in this practice already on ZocDoc'
            else:
                sell['KnowsZocDocAlready'] = 'N/A'            

            # CaresAboutOnlineReputation
            if sell['Healthgrades_NumReviews'] and sell['Healthgrades_NumReviews'] >= 5:
                sell['CaresAboutOnlineReputation'] = 'Lots of Healthgrades reviews'
            elif sell['Vitals_NumReviews'] and sell['Vitals_NumReviews'] >= 2:
                sell['CaresAboutOnlineReputation'] = 'Lots of Vitals reviews'
            elif sell['Doximity_Registered'] and sell['Doximity_Registered'] == 'Yes':
                sell['CaresAboutOnlineReputation'] = 'Registered on Doximity'
            elif sell['Doximity_OnDoximity'] and sell['Doximity_OnDoximity'] == 'Yes':
                sell['CaresAboutOnlineReputation'] = 'Unclaimed Doximity Profile'
            else:
                sell['CaresAboutOnlineReputation'] = 'N/A'  

            # fix Vitals_NumReviews
            if sell['Vitals_NumReviews']:
                sell['Vitals_NumReviews'] = int(sell['Vitals_NumReviews'])

            results.append(sell)

        return results[0]
