import unicodecsv as csv
from commonregex import CommonRegex
from nltk.tag.stanford import StanfordNERTagger


class PiiAnalyzer(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.parser = CommonRegex()
        self.standford_ner = StanfordNERTagger('classifiers/english.conll.4class.distsim.crf.ser.gz')

    #def analysis(self, people = False, organizations = False,locations = False, emails = False, phone_numbers = False, street_addresses = False, credit_cards = False, ips=False):
    def analysis(self, **kwargs):
        people = []
        organizations = []
        locations = []
        emails = []
        phone_numbers = []
        street_addresses = []
        credit_cards = []
        ips = []
        data = []

        get_all = len(kwargs)==0
        get_people = get_all or kwargs.get('people',False)
        get_organizations = get_all or kwargs.get('organizations',False)
        get_locations = get_all or kwargs.get('locations',False)
        get_emails = get_all or kwargs.get('emails',False)
        get_phone_numbers = get_all or kwargs.get('phone_numbers',False)
        get_street_addresses = get_all or kwargs.get('street_addresses',False)
        get_credit_cards = get_all or kwargs.get('credit_cards',False)
        get_ips = get_all or kwargs.get('ips',False)

        with open(self.filepath, 'rU') as filedata:
            reader = csv.reader(filedata)

            for row in reader:
                data.extend(row)
                for text in row:
                    if(get_emails):
                        emails.extend(self.parser.emails(text))
                    if(get_phone_numbers):
                        phone_numbers.extend(self.parser.phones("".join(text.split())))
                    if(get_street_addresses):
                        street_addresses.extend(self.parser.street_addresses(text))
                    if(get_credit_cards):
                        credit_cards.extend(self.parser.credit_cards(text))
                    if(get_ips):
                        ips.extend(self.parser.ips(text))

        for title, tag in self.standford_ner.tag(set(data)):
            if get_people and tag == 'PERSON':
                people.append(title)
            if get_locations and tag == 'LOCATION':
                locations.append(title)
            if get_organizations and tag == 'ORGANIZATION':
                organizations.append(title)

        pii_results = dict()
        if people is not None: pii_results['people'] = people 
        if locations is not None: pii_results['locations'] = locations 
        if organizations is not None: pii_results['organizations'] = organizations 
        if emails is not None: pii_results['emails'] = emails 
        if phone_numbers is not None: pii_results['phone_numbers'] = phone_numbers 
        if street_addresses is not None: pii_results['street_addresses'] = street_addresses 
        if credit_cards is not None: pii_results['credit_cards'] = credit_cards 
        if ips is not None: pii_results['ips'] = ips 

        return pii_results