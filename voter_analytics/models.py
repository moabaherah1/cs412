# File: models.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 3 April 2025
# Description: Contains models which model the data attributes of individual Facebook users. 
from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one voter from the town data.
*    Last Name
*    First Name
*    Residential Address - Street Number
*    Residential Address - Street Name
*    Residential Address - Apartment Number
*    Residential Address - Zip Code
*    Date of Birth
*    Date of Registration
*    Party Affiliation
*    Precinct Number

*    v20state
*    v21town
*    v21primary
*    v22general
*    v23town
    '''
    # identification
    first_name = models.TextField()
    last_name = models.TextField()
    Street_Number = models.IntegerField()
    Street_Name = models.TextField()
    Apartment_Number = models.TextField()
    Zip_Code = models.IntegerField()

    # Dates
    DOB = models.DateField()
    DOR = models.DateField()

    #Affiliation
    Party = models.TextField()
    Precinct_Number = models.TextField()

    Voter_Score = models.IntegerField()

    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} {self.Party}, {self.Precinct_Number}, {self.Voter_Score}'

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    filename = '/Users/mohammedabaherah/Desktop/django/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
            fields = line.split(',')
        
            try:
                # create a new instance of Result object with this record from CSV
                result = Voter(
                                last_name=fields[1],
                                first_name=fields[2],
                                Street_Number = fields[3],
                                Street_Name = fields[4],
                                Apartment_Number = fields[5],
                                
                                Zip_Code = fields[6],

                                DOB = fields[7],
                                DOR = fields[8],

                                Party = fields[9],
                                Precinct_Number = fields[10],
                                v20state = fields[11],
                                v21town = fields[12],
                                v21primary = fields[13],
                                v22general = fields[14],
                                v23town = fields[15],
                                Voter_Score = fields[16],
                            )
            

                result.save() # commit to database
                print(f'Created result: {result}')
                
            except Exception as e: 
                print(f"Skipped: {e}")
        
    print(f'Done. Created {len(Voter.objects.all())} Results.')
