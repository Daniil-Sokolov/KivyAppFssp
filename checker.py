from suds.client import Client
from dadata import Dadata
from datetime import datetime


#xV = input("Пример 19116347468736: ")
#yV = input("Пример 47: ")
#zV = input("Пример 468736: ")


#resFile = open("result.txt",'w', encoding="utf-8")
#resFile.write('')
#resFile.close()


#resFile = open("result.txt",'a', encoding="utf-8")


# Check function

rsultir = {}


def CheckTrack(x): #, y, z):
    url = 'https://tracking.russianpost.ru/rtm34?wsdl'
    client = Client(url,headers={'Content-Type': 'application/soap+xml; charset=utf-8'})

    barcode = str(x) #+str(y)+str(z)#'19116347468736'

    my_login = 'hswccEDLwtVIwT'
    my_password = 'GW0UbrO0mLEM'
    message = \
        """<?xml version="1.0" encoding="UTF-8"?>
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:oper="http://russianpost.org/operationhistory" xmlns:data="http://russianpost.org/operationhistory/data" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Header/>
                    <soap:Body>
                       <oper:getOperationHistory>
                          <data:OperationHistoryRequest>
                             <data:Barcode>""" + barcode+ """</data:Barcode>  
                             <data:MessageType>0</data:MessageType>
                             <data:Language>RUS</data:Language>
                          </data:OperationHistoryRequest>
                          <data:AuthorizationHeader soapenv:mustUnderstand="1">
                             <data:login>"""+ my_login +"""</data:login>
                             <data:password>""" + my_password + """</data:password>
                          </data:AuthorizationHeader>
                       </oper:getOperationHistory>
                    </soap:Body>
                 </soap:Envelope>"""

    result = client.service.getOperationHistory(__inject={'msg':message})

    #sFile = open("otv.txt",'w', encoding="utf-8")
    #sFile.write(str(result))
    #sFile.close()

    
    #print('Трэк-номер\n'+barcode+'\n')
    #rsultir.append('Трэк-номер '+barcode)
    rsultir['barcode'] = str('Трэк-номер '+barcode)
    #resFile.write(str('\nТрэк-номер\n'+barcode+'\n\n'))

    i = 1
    mResult = []
    for rec in result.historyRecord:
        voz =  rec.OperationParameters.OperType.Name == "Возврат"
        prib = rec.OperationParameters.OperAttr.Name == "Прибыло в место вручения"
        if (prib or voz):
            mResult.append({'data': str(rec.OperationParameters.OperDate), 'indexx': rec.AddressParameters.OperationAddress.Index, 'OperType': rec.OperationParameters.OperType.Name, 'Operation': rec.OperationParameters.OperAttr.Name, 'Getter': rec.UserParameters.Rcpn})
            i = i + 1
        #print(str(rec.OperationParameters.OperDate) + '": "' + rec.OperationParameters.OperAttr.Name +' - '+ rec.AddressParameters.OperationAddress.Index)

    #print(mResult)
    fIndex = ''
    for di in mResult:
        voz =  di['OperType'] == "Возврат"
        if voz:
            fIndex = di['indexx']
            break
    #print(fIndex)

    rtt = 1
    for wi in mResult:
        if wi['indexx'] == fIndex:
            strR = str(wi['data']) # строка с вашей датой
            PATTERN_IN = "%Y-%m-%d %H:%M:%S+03:00" # формат вашей даты
            PATTERN_OUT = "%d.%m.%Y" # формат даты, который вам нужен на выходе
        # переводим строку шаблона PATTERN_IN в объект даты
            date = datetime.strptime(strR, PATTERN_IN) 
        # выводим дату в нужном формате
        #print(datetime.strftime(date, PATTERN_OUT))
            varRes = str(rtt)+'. '+str(datetime.strftime(date, PATTERN_OUT))+': '+str(wi['OperType'])+', '+str(wi['Operation'])+', '+str(wi['Getter'])
            #print(str(varRes))
            #rsultir.append(str(varRes))
            rsultir[f'VarRess{rtt}'] = str(varRes)
        #resFile.write(str(varRes))
            rtt = rtt + 1




    token = "7fb2dbf343e283ceeae7d598064fb49ec9c84420"
    dadata = Dadata(token)
    result = dadata.find_by_id("postal_unit", str(fIndex))

    z = "data"
    index = "postal_code"
    adr = "address_str"
    mon = "schedule_mon"
    tue = "schedule_tue"
    wed = "schedule_wed"
    thu = "schedule_thu"
    fri = "schedule_fri"
    sat = "schedule_sat"
    sun = "schedule_sun"

    qq = 1
    wknd = {}

    for i in result:
        if z in i.keys():
        #print(i[z])
            #print('\nИндекс ОПС: ' + str(i[z][index]))
            #rsultir.append('Индекс ОПС: ' + str(i[z][index]))
            rsultir['indexOPS'] = str('Индекс ОПС: ' + i[z][index])
        #resFile.write(str('\nИндекс ОПС: ' + str(i[z][index])))
            #print('Адрес ОПС: ' + str(i[z][adr])+'\n')
            #rsultir.append('Адрес ОПС: ' + str(i[z][adr]))
            rsultir['adressOPS'] = str('Адрес ОПС: ' + i[z][adr])
        #resFile.write(str('Адрес ОПС: ' + str(i[z][adr])+'\n\n'))
        if i[z][mon] == None:
            #print('Выходной: Понедельник')# + str(i[z][mon]))
            #rsultir.append('Выходной: Понедельник')
            rsultir['mon'] = 'Понедельник: Выходной'
            #resFile.write(str('Выходной: Понедельник\n'))
            wknd[qq] = 'Понедельник'
            qq = qq + 1
        if i[z][tue] == None:
            #print('Выходной: Вторник') #+ str(i[z][tue]))
            #rsultir.append('Выходной: Вторник')
            rsultir['tue'] = 'Вторник: Выходной'
          #resFile.write(str('Выходной: Вторник\n'))
            wknd[qq] = 'Вторник'
            qq = qq + 1
        if i[z][wed] == None:
            #print('Выходной: Среда')# + str(i[z][wed]))
            #rsultir.append('Выходной: Среда')
            rsultir['wed'] = 'Среда: Выходной'
          #resFile.write(str('Выходной: Среда\n'))
            wknd[qq] = 'Среда'
            qq = qq + 1
        if i[z][thu] == None:
            #print('Выходной: Четверг')# + str(i[z][thu]))
            #rsultir.append('Выходной: Четверг')
            rsultir['thu'] = 'Четверг: Выходной'
          #resFile.write(str('Выходной: Четверг\n'))
            wknd[qq] = 'Четверг'
            qq = qq + 1
        if i[z][fri] == None:
            #print('Выходной: Пятница')# + str(i[z][fri]))
            #rsultir.append('Выходной: Пятница')
            rsultir['fri'] = 'Пятница: Выходной'
          #resFile.write(str('Выходной: Пятница\n'))
            wknd[qq] = 'Пятница'
            qq = qq + 1
        if i[z][sat] == None:
            #print('Выходной: Суббота')# + str(i[z][sat]))
            #rsultir.append('Выходной: Суббота')
            rsultir['sat'] = 'Суббота: Выходной'
          #resFile.write(str('Выходной: Суббота\n'))
            wknd[qq] = 'Суббота'
            qq = qq + 1
        if i[z][sun] == None:
            #print('Выходной: Воскресенье')# + str(i[z][sun]))
            #rsultir.append('Выходной: Воскресенье')
            rsultir['sun'] = 'Воскресенье: Выходной'
          #resFile.write(str('Выходной: Воскресенье\n'))
            wknd[qq] = 'Воскресенье'
            qq = qq + 1
        #print('\n100% выходные, дают +1 день даже в середине недели:\n1. Новогодние праздники\n2. 23 февраля\n3. 8 марта\n4. 1 мая\n5. 9 мая\n6. 12 июня\n7. 4 ноября ')
        #rsultir.append('100% выходные, дают +1 день даже в середине недели: 1. Новогодние праздники; 2. 23 февраля; 3. 8 марта; 4. 1 мая; 5. 9 мая; 6. 12 июня; 7. 4 ноября')
        rsultir['wknd'] = str('\n100% выходные, дают +1 день даже в середине недели:\n1. Новогодние праздники\n2. 23 февраля\n3. 8 марта\n4. 1 мая\n5. 9 мая\n6. 12 июня\n7. 4 ноября ')
        
        rsultir['link'] = str(f'https://www.pochta.ru/tracking#{x}')
        #print(rsultir)
        

  #CheckTrack('19116347468736') #str(sys.argv[1])) #, yV, zV)
  #resFile.close()

