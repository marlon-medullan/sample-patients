from testdata import VITALS_FILE
import argparse
import csv


class VitalSigns: 
    """Create instances of VitalSigns list entries; 
also maintains complete VitalSigns lists by patient id"""
        
    vitalTypes = [{'name': 'height',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/8302-2',
                        'unit': 'cm',
                        'predicate': 'height'},
                      {'name': 'heart_rate',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/8867-4',
                        'unit': '{beats}/min',
                        'predicate': 'heartRate'},
                      {'name': 'respiratory_rate',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/9279-1',
                        'unit': '{breaths}/min',
                        'predicate': 'respiratoryRate'},
                      {'name': 'temperature',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/8310-5',
                        'unit': 'Cel',
                        'predicate': 'temperature'},
                      {'name': 'weight',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/3141-9',
                        'unit': 'kg',
                        'predicate': 'weight'},
                      {'name': 'bmi',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/39156-5',
                        'unit': 'kg/m2',
                        'predicate': 'bodyMassIndex'},
                      {'name': 'oxygen_saturation',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/2710-2',
                        'unit': '%{HemoglobinSaturation}',
                        'predicate': 'oxygenSaturation'},
                      {'name': 'head_circumference',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/8287-5',
                        'unit': 'cm',
                        'predicate': 'headCircumference'}
                        ]

    systolic, diastolic = [
                      {'name': 'systolic',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/8480-6',
                        'unit': 'mm[Hg]',
                        'predicate': 'systolic'},
                      {'name': 'diastolic',
                        'uri': 'http://purl.bioontology.org/ontology/LNC/8462-4',
                        'unit': 'mm[Hg]',
                        'predicate': 'diastolic'}
                ]

    bpPositionCodes =  [{'name': 'sitting',
                    'system': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                    'code': '33586001'},
                   {'name': 'supine',
                    'system': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                    'code': '40199007'},
                   {'name': 'standing',
                    'system': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                    'code': '10904000'},
                   {'name': 'right arm',
                    'system': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                    'code': '368209003'},
                   {'name': 'left thigh',
                    'system': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                    'code': '61396006'},
                   {'name': 'left arm',
                    'system': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                    'code': '368208006'},
                   {'name': 'right thigh',
                    'system': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                    'code': '11207009'},
                   {'name': 'invasive',
                    'system': 'http://smarthealthit.org/terms/codes/BloodPressureMethod#',
                    'code': 'invasive'},
                   {'name': 'palpation',
                    'system': 'http://smarthealthit.org/terms/codes/BloodPressureMethod#',
                    'code': 'palpation'},
                   {'name': 'machine',
                    'system': 'http://smarthealthit.org/terms/codes/BloodPressureMethod#',
                    'code': 'machine'},
                   {'name': 'auscultation',
                    'system': 'http://smarthealthit.org/terms/codes/BloodPressureMethod#',
                    'code': 'auscultation'}
                    ]

    vitals = {} # Dictionary of VitalSign lists, by patient id 

    @classmethod
    def load(cls):
      """Loads patient VitalSigns observations"""
      
      # Loop through VitalSigns and build patient VitalSigns lists:
      VitalSigns = csv.reader(file(VITALS_FILE,'U'),dialect='excel-tab')
      header = VitalSigns.next()
      for VitalSign in VitalSigns:
          cls(dict(zip(header,VitalSign))) # Create a VitalSign instance (saved in VitalSigns.vitals)

    @classmethod
    def loadVitalsPatient (cls, vp):
        vitals = vp['vitals']
        for (i, v) in enumerate(vitals):
            id = "vp-%s" % (i+1)
            m = {}
            if 'height' in v.keys():
                m = {'WEIGHT': '', 'TEMPERATURE': '', 'RESPIRATORY_RATE': '', 'HEAD_CIRCUMFERENCE': '', 'HEART_RATE': '', 'OXYGEN_SATURATION': '', 'BMI': '',
                    'TIMESTAMP': v['encounter']['date'],
                    'START_DATE': v['encounter']['start_date'],
                    'END_DATE': v['encounter']['end_date'],
                    'PID': vp['pid'],
                    'ID': id,
                    'HEIGHT': v['height'],
                    'ENCOUNTER_TYPE': v['encounter']['type'],
                    'BP_POSITION': '',
                    'BP_METHOD': '',
                    'BP_SITE': '',
                    'SYSTOLIC': '',
                    'DIASTOLIC': ''}
            else:
                m = {'WEIGHT': '', 'TEMPERATURE': '', 'RESPIRATORY_RATE': '', 'HEAD_CIRCUMFERENCE': '', 'HEART_RATE': '', 'OXYGEN_SATURATION': '', 'BMI': '',
                    'TIMESTAMP': v['encounter']['date'],
                    'START_DATE': v['encounter']['start_date'],
                    'END_DATE': v['encounter']['end_date'],
                    'PID': vp['pid'],
                    'ID': id,
                    'HEIGHT': '',
                    'ENCOUNTER_TYPE': v['encounter']['type'],
                    'BP_POSITION': v['position'],
                    'BP_METHOD': v['method'],
                    'BP_SITE': v['site'],
                    'SYSTOLIC': v['sbp'],
                    'DIASTOLIC': v['dbp']}
            cls(m)

    def __init__(self,m):
        for f in m:
            setattr(self, f.lower(), m[f])
        self.sourcerow = m

        # Append VitalSign to the patient's VitalSign list:
        if self.pid in  self.__class__.vitals:
          self.__class__.vitals[self.pid].append(self)
        else: self.__class__.vitals[self.pid] = [self]

    def asTabString(self):
        return self.sourcerow

if __name__== '__main__':

  parser = argparse.ArgumentParser(description='Test Data Vitals Module')
  group = parser.add_mutually_exclusive_group()
  group.add_argument('--VitalSigns', action='store_true', help='list all VitalSigns')
  group.add_argument('--pid',nargs='?', default='1520204',
     help='display VitalSigns for a given patient id (default=1520204)')
  args = parser.parse_args()
 
  VitalSigns.load()
  if args.pid:
    if not args.pid in VitalSigns.vitals:
      parser.error("No results found for pid = %s"%args.pid)
    VitalSigns = VitalSigns.vitals[args.pid]
    for VitalSign in VitalSigns: 
      print VitalSign.asTabString()
