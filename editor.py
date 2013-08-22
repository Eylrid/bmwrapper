import re
import hashlib
import bminterface
import json

SAMPLETEXT = '''Tue, 2013-06-25 16:59:56 UTC   Message ostensibly from BM-orBMya4QReKJsfWzmpuZZfS3MHcFcQdBm:

It has now stopped on /b/ as well.

/b/ is a chan.
Passphrase: "/b/"
Address: BM-2DBrj7qjmbVHNZUMPe6uVER6DmJauZppwA

------------------------------------------------------
Tue, 2013-06-25 16:38:32 UTC   Message ostensibly from BM-GuKFGpT5gGFmXDB61KPM8BSeSpxZpz5T:

whats the address of /b/?

------------------------------------------------------
Mon, 2013-06-24 07:29:48 UTC   Message ostensibly from BM-orBMya4QReKJsfWzmpuZZfS3MHcFcQdBm:

The spam seems to be dying down on general. It is still coming in on /b/.'''

FIRSTNAMES = ['Sophia', 'Isabella', 'Emma', 'Olivia', 'Ava',
              'Emily', 'Abigail', 'Madison', 'Mia', 'Chloe',
              'Elizabeth', 'Ella', 'Addison', 'Natalie', 'Lily',
              'Grace', 'Samantha', 'Avery', 'Sofia', 'Aubrey',
              'Brooklyn', 'Lillian', 'Victoria', 'Evelyn', 'Hannah',
              'Alexis', 'Charlotte', 'Zoey', 'Leah', 'Amelia',
              'Zoe', 'Hailey', 'Layla', 'Gabriella', 'Nevaeh',
              'Kaylee', 'Alyssa', 'Anna', 'Sarah', 'Allison',
              'Savannah', 'Ashley', 'Audrey', 'Taylor', 'Brianna',
              'Aaliyah', 'Riley', 'Camila', 'Khloe', 'Claire',
              'Sophie', 'Arianna', 'Peyton', 'Harper', 'Alexa',
              'Makayla', 'Julia', 'Kylie', 'Kayla', 'Bella',
              'Katherine', 'Lauren', 'Gianna', 'Maya', 'Sydney',
              'Serenity', 'Kimberly', 'Mackenzie', 'Autumn', 'Jocelyn',
              'Faith', 'Lucy', 'Stella', 'Jasmine', 'Morgan',
              'Alexandra', 'Trinity', 'Molly', 'Madelyn', 'Scarlett',
              'Andrea', 'Genesis', 'Eva', 'Ariana', 'Madeline',
              'Brooke', 'Caroline', 'Bailey', 'Melanie', 'Kennedy',
              'Destiny', 'Maria', 'Naomi', 'London', 'Payton',
              'Lydia', 'Ellie', 'Mariah', 'Aubree', 'Kaitlyn',
              'Violet', 'Rylee', 'Lilly', 'Angelina', 'Katelyn',
              'Mya', 'Paige', 'Natalia', 'Ruby', 'Piper',
              'Annabelle', 'Mary', 'Jade', 'Isabelle', 'Liliana',
              'Nicole', 'Rachel', 'Vanessa', 'Gabrielle', 'Jessica',
              'Jordyn', 'Reagan', 'Kendall', 'Sadie', 'Valeria',
              'Brielle', 'Lyla', 'Isabel', 'Jacob', 'Mason',
              'William', 'Jayden', 'Noah', 'Michael', 'Ethan',
              'Alexander', 'Aiden', 'Daniel', 'Anthony', 'Matthew',
              'Elijah', 'Joshua', 'Liam', 'Andrew', 'James',
              'David', 'Benjamin', 'Logan', 'Christopher', 'Joseph',
              'Jackson', 'Gabriel', 'Ryan', 'Samuel', 'John',
              'Nathan', 'Lucas', 'Christian', 'Jonathan', 'Caleb',
              'Dylan', 'Landon', 'Isaac', 'Gavin', 'Brayden',
              'Tyler', 'Luke', 'Evan', 'Carter', 'Nicholas',
              'Isaiah', 'Owen', 'Jack', 'Jordan', 'Brandon',
              'Wyatt', 'Julian', 'Aaron', 'Jeremiah', 'Angel',
              'Cameron', 'Connor', 'Hunter', 'Adrian', 'Henry',
              'Eli', 'Justin', 'Austin', 'Robert', 'Charles',
              'Thomas', 'Zachary', 'Jose', 'Levi', 'Kevin',
              'Sebastian', 'Chase', 'Ayden', 'Jason', 'Ian',
              'Blake', 'Colton', 'Bentley', 'Dominic', 'Xavier',
              'Oliver', 'Parker', 'Josiah', 'Adam', 'Cooper',
              'Brody', 'Nathaniel', 'Carson', 'Jaxon', 'Tristan',
              'Luis', 'Juan', 'Hayden', 'Carlos', 'Jesus',
              'Nolan', 'Cole', 'Alex', 'Max', 'Grayson',
              'Bryson', 'Diego', 'Jaden', 'Vincent', 'Easton',
              'Eric', 'Micah', 'Kayden', 'Jace', 'Aidan',
              'Ryder', 'Ashton', 'Bryan', 'Riley', 'Hudson',
              'Asher', 'Bryce', 'Miles', 'Kaleb', 'Giovanni',
              'Antonio', 'Kaden', 'Colin', 'Kyle', 'Brian',
              'Timothy', 'Steven', 'Sean', 'Miguel', 'Richard',
              'Ivan']

LASTNAMES = ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES',
            'MILLER', 'DAVIS', 'GARCIA', 'RODRIGUEZ', 'WILSON',
            'MARTINEZ', 'ANDERSON', 'TAYLOR', 'THOMAS', 'HERNANDEZ',
            'MOORE', 'MARTIN', 'JACKSON', 'THOMPSON', 'WHITE',
            'LOPEZ', 'LEE', 'GONZALEZ', 'HARRIS', 'CLARK',
            'LEWIS', 'ROBINSON', 'WALKER', 'PEREZ', 'HALL',
            'YOUNG', 'ALLEN', 'SANCHEZ', 'WRIGHT', 'KING',
            'SCOTT', 'GREEN', 'BAKER', 'ADAMS', 'NELSON',
            'HILL', 'RAMIREZ', 'CAMPBELL', 'MITCHELL', 'ROBERTS',
            'CARTER', 'PHILLIPS', 'EVANS', 'TURNER', 'TORRES',
            'PARKER', 'COLLINS', 'EDWARDS', 'STEWART', 'FLORES',
            'MORRIS', 'NGUYEN', 'MURPHY', 'RIVERA', 'COOK',
            'ROGERS', 'MORGAN', 'PETERSON', 'COOPER', 'REED',
            'BAILEY', 'BELL', 'GOMEZ', 'KELLY', 'HOWARD',
            'WARD', 'COX', 'DIAZ', 'RICHARDSON', 'WOOD',
            'WATSON', 'BROOKS', 'BENNETT', 'GRAY', 'JAMES',
            'REYES', 'CRUZ', 'HUGHES', 'PRICE', 'MYERS',
            'LONG', 'FOSTER', 'SANDERS', 'ROSS', 'MORALES',
            'POWELL', 'SULLIVAN', 'RUSSELL', 'ORTIZ', 'JENKINS',
            'GUTIERREZ', 'PERRY', 'BUTLER', 'BARNES', 'FISHER',
            'HENDERSON', 'COLEMAN', 'SIMMONS', 'PATTERSON', 'JORDAN',
            'REYNOLDS', 'HAMILTON', 'GRAHAM', 'KIM', 'GONZALES',
            'ALEXANDER', 'RAMOS', 'WALLACE', 'GRIFFIN', 'WEST',
            'COLE', 'HAYES', 'CHAVEZ', 'GIBSON', 'BRYANT',
            'ELLIS', 'STEVENS', 'MURRAY', 'FORD', 'MARSHALL',
            'OWENS', 'MCDONALD', 'HARRISON', 'RUIZ', 'KENNEDY',
            'WELLS', 'ALVAREZ', 'WOODS', 'MENDOZA', 'CASTILLO',
            'OLSON', 'WEBB', 'WASHINGTON', 'TUCKER', 'FREEMAN',
            'BURNS', 'HENRY', 'VASQUEZ', 'SNYDER', 'SIMPSON',
            'CRAWFORD', 'JIMENEZ', 'PORTER', 'MASON', 'SHAW',
            'GORDON', 'WAGNER', 'HUNTER', 'ROMERO', 'HICKS',
            'DIXON', 'HUNT', 'PALMER', 'ROBERTSON', 'BLACK',
            'HOLMES', 'STONE', 'MEYER', 'BOYD', 'MILLS',
            'WARREN', 'FOX', 'ROSE', 'RICE', 'MORENO',
            'SCHMIDT', 'PATEL', 'FERGUSON', 'NICHOLS', 'HERRERA',
            'MEDINA', 'RYAN', 'FERNANDEZ', 'WEAVER', 'DANIELS',
            'STEPHENS', 'GARDNER', 'PAYNE', 'KELLEY', 'DUNN',
            'PIERCE', 'ARNOLD', 'TRAN', 'SPENCER', 'PETERS',
            'HAWKINS', 'GRANT', 'HANSEN', 'CASTRO', 'HOFFMAN',
            'HART', 'ELLIOTT', 'CUNNINGHAM', 'KNIGHT', 'BRADLEY',
            'CARROLL', 'HUDSON', 'DUNCAN', 'ARMSTRONG', 'BERRY',
            'ANDREWS', 'JOHNSTON', 'RAY', 'LANE', 'RILEY',
            'CARPENTER', 'PERKINS', 'AGUILAR', 'SILVA', 'RICHARDS',
            'WILLIS', 'MATTHEWS', 'CHAPMAN', 'LAWRENCE', 'GARZA',
            'VARGAS', 'WATKINS', 'WHEELER', 'LARSON', 'CARLSON',
            'HARPER', 'GEORGE', 'GREENE', 'BURKE', 'GUZMAN',
            'MORRISON', 'MUNOZ', 'JACOBS', 'OBRIEN', 'LAWSON',
            'FRANKLIN', 'LYNCH', 'BISHOP', 'CARR', 'SALAZAR',
            'AUSTIN', 'MENDEZ', 'GILBERT', 'JENSEN', 'WILLIAMSON',
            'MONTGOMERY', 'HARVEY', 'OLIVER', 'HOWELL', 'DEAN',
            'HANSON', 'WEBER', 'GARRETT', 'SIMS', 'BURTON',
            'FULLER']

def lookupname(address):
    if address.startswith('BM-'): address = address[3:]
    hash = hashlib.sha256(address).digest()
    firstname = FIRSTNAMES[ord(hash[0])]
    lastname = LASTNAMES[ord(hash[1])]
    return '%s %s' %(firstname, lastname)

def label(address):
    myAddDict = myAddressDict()
    addbookDict = addressbookDict()
    subDict = subscriptionDict()
    if address in myAddDict:
        label = myAddDict[address]
    elif address in addbookDict:
        label = addbookDict[address].decode('base64')
    elif address in subDict:
        label = subDict[address].decode('base64')
    else:
        label = lookupname(address)

    #non word or space charcters could cause problems
    #later when removing the label, so we get rid of them
    label = re.sub(r'[^\w\s]', '', label)

    return label

def subaddress(matchobj):
    return '[%s, %s]' %(label(matchobj.group(0)), matchobj.group(0))

def subaddresses(input):
    pattern = r'BM-[a-zA-Z0-9]+'
    output = re.sub(pattern, subaddress, input)
    return output

def desubaddress(matchobj):
    return matchobj.group(1)

def desubaddresses(input):
    pattern = r'\[[\w\s]+,\s+(BM-[a-zA-Z0-9]+)]'
    output = re.sub(pattern, desubaddress, input)
    return output

def edit(input):
    output = subaddresses(input)
    return output

def deedit(input):
    '''reverse the changes made by edit, if possible'''
    output = desubaddresses(input)
    return output

def myAddressDict():
    '''return a dict mapping addresses to labels'''
    jsonAddresses = json.loads(bminterface.getAddresses())
    addressList = [(i['address'], i['label']) for i in jsonAddresses['addresses']]
    addressDict = dict(addressList)
    return addressDict

def addressbookDict():
    '''return a dict mapping addresses to labels'''
    jsonAddresses = json.loads(bminterface.getAddressbook())
    addressList = [(i['address'], i['label']) for i in jsonAddresses['addresses']]
    addressDict = dict(addressList)
    return addressDict

def subscriptionDict():
    '''return a dict mapping addresses to labels'''
    jsonAddresses = json.loads(bminterface.getSubscriptions())
    addressList = [(i['address'], i['label']) for i in jsonAddresses['subscriptions']]
    addressDict = dict(addressList)
    return addressDict

