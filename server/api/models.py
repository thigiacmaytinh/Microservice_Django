from mongoengine import Document, IntField, StringField, DateTimeField, BooleanField, EmailField, DictField, FloatField, ListField

################################################################
#No.1
LEVELS = (
    'Root',
    'Admin', #register
    'Gate', #admin create
    'Supporter' #root create
)

USER_STATUS = (
    'Registered',
    'Verified', #verify by phone number
    'Approved', #root approve
    'Suspend',
    'Invited'
)

SERVICE_PACK = (
    'Free',
    'Basic',
    'Premium',
    'Subscription'
)

class User(Document):    
    email               =  StringField(unique=True) #require with admin
    fullname            =  StringField()
    position            =  StringField()
    password            =  StringField(required=True)
    phone               =  StringField()
    orgName             =  StringField(default="")
    addressOrg          =  StringField()
    phoneOrg            =  StringField()
    level               =  StringField(choices=LEVELS)
    status              =  StringField(choices=USER_STATUS)
    servicePack         =  StringField(choices=SERVICE_PACK)
    owner               =  StringField(required=True) #email of owner
    timeRegister        =  DateTimeField()
    timeUpdate          =  DateTimeField()
    numGateAccount      =  IntField(default=0)
    numGateAccountAdded =  IntField(default=0)
    numPerson           =  IntField(default=0)
    countPerson         =  IntField(default=0) #num person has image
    suspendReason       =  StringField()
    references          =  StringField()
    secretkey           =  StringField()
    currentPersonIdx    =  IntField(default=0)
    isDeleted           =  BooleanField(default = False)            

################################################################

class Level(Document):
    levelID             =  StringField(required=True)
    levelName           =  StringField(required=True)

################################################################

class SearchOption(Document):
    optionID            =  StringField(required=True)
    optionName          =  StringField(required=True)
    admin               =  BooleanField(default=True)
    smod                =  BooleanField(default=False)
    mod                 =  BooleanField(default=False)
    staff               =  BooleanField(default=False)
    partner             =  BooleanField(default=False)
    guest               =  BooleanField(default=False)
  
################################################################
GENDERS = (
    'Male',
    'Female',
    'undefined',
    'Nam',
    'Nữ',
    'Chưa biết'
)
STATE = (
    'Checked_in',
    'Checked_out',
    'Visitor',
    'Khách vào',
    'Khách ra',
    'Vãng lai'
)
PERSON_TYPE = (
    'Guest',
    'Staff',
    'Khách',
    'Nhân viên'
)
#No.4
class Person(Document):
    personID            =  StringField()
    fullName            =  StringField(default="Khách mới")
    fullName_ascii      =  StringField()
    dirName             =  StringField()
    email               =  StringField()
    birthday            =  DateTimeField()
    cmnd                =  StringField()
    issuedDate          =  DateTimeField() #CMND
    address             =  StringField(default="")
    job                 =  StringField(default="")
    note                =  StringField()
    attachments         =  ListField(StringField()) 
    dateCreate          =  DateTimeField(required=True)
    firstTimeAppear     =  DateTimeField()
    lastTimeAppear      =  DateTimeField()
    gender              =  StringField(choices=GENDERS, default='Chưa biết')
    phone               =  StringField()
    totalAppear         =  IntField(default=0)    
    group_pk            =  StringField()
    groupName           =  StringField()
    owner               =  StringField(required=True) #email
    orgName             =  StringField()    
    lastestImgPath      =  StringField() #to remove because has avatar
    avatar              =  StringField()  
    cardID              =  StringField()
    timeUpdate          =  DateTimeField()    
    userUpdate          =  StringField()
    timeAddTemplate     =  DateTimeField() #TODO: delete
    timeAddSample       =  DateTimeField()
    state               =  StringField(choices=STATE, default='Visitor')
    personType          =  StringField(choices=PERSON_TYPE, default='Khách')
    startShift          =  StringField() #hh:mm
    endShift            =  StringField() #hh:mm
    isDeleted           =  BooleanField(default = False)
    
################################################################
#No.5
class Appear(Document):
    person_pk           =  StringField(required=True)
    person_id           =  StringField()
    fullName            =  StringField(default='Khách mới')
    fullName_ascii      =  StringField()
    birthday            =  DateTimeField()
    phone               =  StringField()
    timeAppear          =  DateTimeField(required=True)
    timeCheckout        =  DateTimeField()
    imagePath           =  StringField(required=True)
    personExist         =  BooleanField(default=False)
    client_pk           =  StringField()
    group_pk            =  StringField()
    groupName           =  StringField()
    gate                =  StringField()
    owner               =  StringField(required=True)
    distance            =  FloatField()
    percent             =  IntField()
    elapsed             =  FloatField()
    gender              =  StringField(choices=GENDERS, default='Chưa biết') #to retrain model
    state               =  StringField(choices=STATE, default='Vãng lai')
    numSecond           =  IntField() #total second between login - logout
    lastAppear_pk       =  StringField() #pk of last checkin
    stage               =  IntField()
    shift_id            =  IntField()
    timeUpdate          =  DateTimeField()
    userUpdate          =  StringField()
    checked_out         =  BooleanField(default=False)
    personType          =  StringField(choices=PERSON_TYPE, default='Khách')    
    similarPath         =  StringField() #path to most similar image
    isDeleted           =  BooleanField(default = False)

################################################################
#No.6
class LoginSession(Document):
    token               =  StringField()
    email               =  StringField(required=True)
    level               =  StringField(required=True)
    fullname            =  StringField()
    loginTime           =  DateTimeField(required=True)
    logoutTime          =  DateTimeField()
    platform            =  StringField()
    orgName             =  StringField()
    owner               =  StringField()
    purpose             =  StringField()    
    validTo             =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################
#No.7

class Client(Document):    
    clientName          =  StringField()
    UID                 =  StringField(required=True)
    os                  =  StringField(required=True)
    platform            =  StringField(required=True)
    note                =  StringField(max_length=1000)
    timeUpdate          =  DateTimeField()
    allow               =  BooleanField(default=False)
    isDeleted           =  BooleanField(default=False)

################################################################
#No.9
class History(Document):    
    microbe_pk          =  StringField(required=True)
    content             =  StringField(required=True)
    oldValue            =  StringField(default = ' ')
    newValue            =  StringField(default = ' ')
    dateChanged         =  DateTimeField()
    email               =  EmailField(required=True)
    platfom             =  StringField()
    isDeleted           =  BooleanField(default=False)

################################################################
#No.10
class Notification(Document):    
    notifyType          =  StringField(required=True)
    content             =  StringField(required=True)
    link                =  StringField(default = ' ')
    dateCreate          =  DateTimeField(required=True)
    userSend            =  StringField(required=True)
    userReceive         =  StringField(required=True)
    status              =  StringField(default="unseen")
    isDeleted           =  BooleanField(default=False)


################################################################

class PersonGroup(Document):
    name                =  StringField(required=True)
    alert               =  BooleanField(required=True) #alert when appear
    ignore              =  BooleanField()
    timeUpdate          =  DateTimeField()
    owner               =  StringField(required=True) #email
    userUpdate          =  StringField() #email
    bgColor             =  StringField()
    isDeleted           =  BooleanField(default=False)

################################################################

class Permission(Document):
    group_id            =  StringField(max_length=200, required=True)
    email               =  EmailField(max_length=200, required=True)  

################################################################

PHONE_STATUS = (
    'New',
    'Đã cấp quyền',
    'Đã khóa',
)

class Phone(Document):
    phoneUDID           =  StringField(max_length=200, required=True)
    name                =  StringField(required=True) 
    owner               =  StringField()    
    userUsing           =  StringField()
    appVersion          =  StringField()
    timeCreate          =  DateTimeField(required=True)
    timeUpdate          =  DateTimeField()
    lastRequestDate     =  DateTimeField()
    status              =  StringField(choices=PHONE_STATUS, default="New")
    userUpdate          =  StringField()
    isDeleted           =  BooleanField(default=False)

################################################################

class ChartValue(Document):
    owner               =  StringField(required=True)
    dateSummary         =  StringField(required=True) #dd/MM/yyyy
    dateRecord          =  DateTimeField()
    countOldAppear      =  IntField(required=True)
    countNewAppear      =  IntField(required=True)
    #isDeleted           =  BooleanField(default=False) #dont need 

################################################################
class Shift(Document):
    owner               =  StringField(required=True)
    startShift1         =  StringField(required=True) #hh:mm
    endShift1           =  StringField(required=True) #hh:mm
    startShift2         =  StringField(required=True) #hh:mm
    endShift2           =  StringField(required=True) #hh:mm
    startShift3         =  StringField(required=True) #hh:mm
    endShift3           =  StringField(required=True) #hh:mm
    dateCreate          =  DateTimeField(required=True)
    dateModify          =  DateTimeField(required=True)
    isDeleted           =  BooleanField(default=False)

################################################################

class Label(Document):
    labelIndex          =  IntField(required=True)
    labelName           =  StringField(required=True)
    dateModify          =  DateTimeField()
    isDeleted           =  BooleanField(default=False)

################################################################

ACTIVITIES = (
    'Thêm khách hàng',
    'Cập nhật khách hàng',
    'Xóa khách hàng',
    'Gộp khách hàng',
    'Xóa ảnh khách hàng',
    'Xuất report khách hàng'
    'Xuất report lượt vào'
)

class Activity(Document):
    email               =  StringField(required=True)
    activity            =  StringField(required=True)
    value               =  StringField(required=True)
    timeCreate          =  DateTimeField(required=True)
    isDeleted           =  BooleanField(default=False)

################################################################

LOGS = (
    'Thêm lượt vào thất bại',
    'Thêm khách hàng thất bại',
    'Cập nhật khách hàng thất bại',
    'Xóa khách hàng thất bại',
    'Gộp khách hàng thất bại',
    'Xóa ảnh khách hàng thất bại',
    'Xuất report khách hàng thất bại'
    'Xuất report lượt vào thất bại'
)

class Log(Document):
    activity            =  StringField(required=True)
    exception           =  StringField(required=True)
    timeCreate          =  DateTimeField(required=True)
    isDeleted           =  BooleanField(default=False)

################################################################

class Option(Document):
    optionID            =  StringField(required=True)
    optionName          =  StringField(required=True)
    value               =  StringField()
    owner               =  StringField()

################################################################

class Currency(Document):
    name                =  StringField(required=True)
    buyDifference       =  FloatField()
    sellDifference      =  FloatField()
    valueAbove          =  FloatField()
    valueBelow          =  FloatField()
    isDeleted           =  BooleanField(default=False)

################################################################

class HistoryCurrency(Document):
    name                =  StringField(required=True)
    buy                 =  FloatField()
    sell                =  FloatField()
    percent_change      =  FloatField()
    price_change        =  FloatField()
    gap                 =  FloatField()
    change              =  FloatField()  #tỉ lệ so với phiên trước đó (tiền)
    rate                =  FloatField()  #T/giá của tiền
    buyDifference       =  FloatField()
    sellDifference      =  FloatField()
    valueAbove          =  FloatField()
    valueBelow          =  FloatField()
    timeCreate          =  DateTimeField()
    isDeleted           =  BooleanField(default=False)