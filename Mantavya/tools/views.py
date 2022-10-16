from random import randrange
from typing import ValuesView
from django.shortcuts import render
from django.http import Http404, JsonResponse
from feedback.models import *
import datetime as dt
from officer.models import User

def debug(data, message=''):
    print(f"::  [ {data} ] ----- {message} -----")

def index(request):
    return render(request, 'tools.html')

# Tools
def insertData(request):
    DT = {
        "Ahmedabad":["Bavla","Daskroi","Detroj-Rampura","Dhandhuka","Dholera","Dholka","Mandal","Sanand","Viramgam"],
        "Amreli":["Babra","Bagasara","Dhari","Jafrabad","Khambha","Kunkavav vadia","Lathi","Lilia","Rajula","Savarkundla"],
        "Anand":["Anklav","Borsad","Khambhat","Petlad","Sojitra","Tarapur","Umreth"],
        "Aravalli":["Bayad","Bhiloda","Dhansura","Malpur","Meghraj","Modasa"],
        "Banaskantha": ["Amirgadh","Bhabhar","Danta","Dantiwada","Deesa","Deodar","Dhanera","Kankrej","Lakhani","Palanpur","Suigam","Tharad","Vadgam","Vav"],
        "Bharuch": ["Amod","Ankleshwar","Hansot","Jambusar","Jhagadia","Netrang","Vagra","Valia"],
        "Bhavnagar": ["Gariadhar","Ghogha","Jesar","Mahuva","Palitana","Sihor","Talaja","Umrala","Vallabhipur"],
        "Botad": ["Barwala","Gadhada","Ranpur"],
        "Chhota Udaipur": ["Bodeli","Jetpur pavi","Kavant","Nasvadi","Sankheda"],
        "Dahod": ["Devgadh baria","Dhanpur","Fatepura","Garbada","Limkheda","Sanjeli","Jhalod","Singvad"],
        "Dang": ["Ahwa","Subir","Waghai"],
        "Dwarka": ["Bhanvad","Kalyanpur","Khambhalia","Okhamandal"],
        "Gandhinagar": ["Dehgam","Kalol","Mansa"],
        "Gir Somnath": ["Gir-Gadhada","Kodinar","Sutrapada","Talala","Una","Patan-Veraval"],
        "Jamnagar": ["Dhrol","Jamjodhpur","Jodiya","Kalavad","Lalpur"],
        "Junagadh": ["Junagadh City","Bhesana","Junagadh Rural","Keshod","Malia","Manavadar","Mangrol","Mendarda","Vanthali","Visavadar"],
        "Kutch": ["Abdasa","Anjar","Bhachau","Bhuj","Gandhidham","Lakhpat","Mandvi","Mundra","Nakhatrana","Rapar"],
        "Kheda": ["Galteshwar","Kapadvanj","Kathlal","Mahudha","Matar","Mehmedabad","Nadiad","Thasra","Vaso"],
        "Mahisagar": ["Balasinor","Kadana","Khanpur","Lunawada","Santrampur","Virpur"],
        "Mehsana": ["Becharaji","Jotana","Kadi","Kheralu","Gojhariya","Satlasana","Unjha","Vadnagar","Vijapur","Visnagar"],
        "Morbi": ["Halvad","Maliya","Tankara","Wankaner"],
        "Narmada": ["Dediapada","Garudeshwar","Nandod","Sagbara","Tilakwada"],
        "Navsari": ["Vansda","Chikhli","Gandevi","Jalalpore","Khergam"],
        "Panchmahal": ["Ghoghamba","Godhra","Halol","Jambughoda","Kalol","Morwa Hadaf","Shehera"],
        "Patan": ["Chanasma","Harij","Radhanpur","Sami","Sankheswar","Santalpur","Sarasvati","Sidhpur"],
        "Porbandar": ["Kutiyana","Ranavav"],
        "Rajkot": ["Dhoraji","Gondal","Jamkandorna","Jasdan","Jetpur","Kotada Sangani","Lodhika","Paddhari","Upleta","Vinchchiya"],
        "Sabarkantha": ["Himatnagar","Idar","Khedbrahma","Poshina","Prantij","Talod","Vadali","Vijaynagar"],
        "Surat":["Bardoli","Choryasi","Kamrej","Mahuva","Mandvi","Mangrol","Olpad","Palsana","Umarpada"], 
        "Surendranagar": ["Chotila","Chuda","Dasada","Dhrangadhra","Lakhtar","Limbdi","Muli","Sayla","Thangadh","Wadhwan"],
        "Tapi": ["Nizar","Songadh","Uchhal","Valod","Vyara","Kukarmunda","Dolvan"],
        "Vadodara": ["Dabhoi","Desar","Karjan","Padra","Savli","Sinor","Vaghodia"],
        "Valsad": ["Dharampur","Kaprada","Pardi","Umbergaon","Vapi"]
    }
    
    i,j = 1,1

    for D in DT:
        District(i,D).save()
        debug(D, "District Inserted")
        for T in DT[D]:
            Taluka(j,T,i).save()
            debug(T, "Taluka Inserted")
            j+=1
        i+=1

    return JsonResponse({"status": "Inserted district and taluka into database"})

def insertTestDataSet(request):
    # Answer List Dataset

    AnswerList(1, "Through a person known to a police officer").save()
    AnswerList(2, "With a neighbour/ local leader").save()
    AnswerList(3, "On your own").save()
    debug(123,"Data inserted")

    AnswerList(4, "More than 15 minutes").save()
    AnswerList(5, "15 minutes").save()
    AnswerList(6, "10 minutes").save()
    AnswerList(7, "5 minutes").save()
    AnswerList(8, "Immediately").save()
    debug(45678,"Data inserted")

    AnswerList(9,"Worst").save()
    AnswerList(10,"Bad").save()
    AnswerList(11,"Good").save()
    AnswerList(12,"V.Good").save()
    AnswerList(13,"Excellent").save()
    debug(913,"Data inserted")

    PoliceStation(id=1, qrId=randrange(000000,999999), name="Himatnagar Rural", taluka=Taluka.objects.get(id=187)).save()
    PoliceStation(id=2,qrId=randrange(000000,999999), name="A Division Himatnagar", taluka=Taluka.objects.get(id=187), isSubDiv=True).save()
    PoliceStation(id=3, qrId=randrange(000000,999999), name="B Division Himatnagar", taluka=Taluka.objects.get(id=187), isSubDiv=True).save()
    debug(123,"PS Data inserted")

    SubDivPoliceStation(subDivision=PoliceStation.objects.get(id=2),policeStation=PoliceStation.objects.get(id=1)).save()
    SubDivPoliceStation(subDivision=PoliceStation.objects.get(id=3),policeStation=PoliceStation.objects.get(id=1)).save()
    debug(123,"PS SD Data inserted")
    
    return JsonResponse({"status": "Inserted Test Dataset into database"})

def insertFeedbackDataSet(request):

    for i in range(10):
        Citizen(
            mobileNum=randrange(8888888888,9999999999)
        ).save()
        debug(i+1,"Citizen Inserted")
    
    for i in range(499):
        Feedback(
            citizenId= Citizen.objects.get(id=randrange(1,11)),
            name="None",
            q1=AnswerList.objects.get(id=randrange(1,4)),
            q2=AnswerList.objects.get(id=randrange(4,9)),
            q3=AnswerList.objects.get(id=randrange(9,14)),
            psId=PoliceStation.objects.get(id=randrange(2,11)),
            date=(dt.datetime.now() - dt.timedelta(days=randrange(1,31))).date()
        ).save()
        debug(i+1,"Feedback inserted")

    return JsonResponse({"status": "Inserted Feedback Dataset into database"})



def insert_users_data(request):
    data = {
    "Ahmedabad":"cp-ahd@gujarat.gov.in",    
    "Amreli":"sp-amr@gujarat.gov.in",         
    "Anand":"sp-and@gujarat.gov.in",      
    "Aravalli":"sp-arv@gujarat.gov.in",      
    "Banaskantha":"sp-ban@gujarat.gov.in",      
    "Bharuch":"sp-bha@gujarat.gov.in",      
    "Bhavnagar":"sp-bav@gujarat.gov.in",      
    "Botad":"sp-botad@gujarat.gov.in",      
    "Chhota Udaipur":"sp-cpr@gujarat.gov.in",      
    "Dahod":"sp-dah@gujarat.gov.in",
    "Dang":"sp-dan@gujarat.gov.in",
    "Dwarka":"rbrdevbhoomi@yahoo.com",
    "Gandhinagar":"sp-gnr@gujarat.gov.in",
    "Gir Somnath":"sp-gir@gujarat.gov.in",      
    "Jamnagar":"sp-jam@gujarat.gov.in",      
    "Junagadh":"sp-jun@gujarat.gov.in",      
    "Kutch":"sp-kut@gujarat.gov.in",      
    "Kheda":"sp-khe@gujarat.gov.in",      
    "Mahisagar":"sdpolunapan@gujarat.gov.in",      
    "Mehsana":"cp-meh@gujarat.gov.in",      
    "Morbi":"sp-mrb@gujarat.gov.in",      
    "Narmada":"sp-nar@gujarat.gov.in",      
    "Navsari":"sp-nav@gujarat.gov.in",      
    "Panchmahal":"sp-pan@gujarat.gov.in",      
    "Patan":"sp-patan@gujarat.gov.in",      
    "Porbandar":"sp-por@gujarat.gov.in",      
    "Rajkot":"sp-raj@gujarat.gov.in",      
    "Sabarkantha":"sp-sab@gujarat.gov.in",      
    "Surat":"sp-sur@gujarat.gov.in",      
    "Surendranagar":"sp-srn@gujarat.gov.in",      
    "Tapi":"sp-tapi@gujarat.gov.in",      
    "Vadodara":"cp-vad@gujarat.gov.in",      
    "Valsad":"sp-val@gujarat.gov.in"
    }
    for i in data:
        debug(i, 'Data Inserted')
        User.objects.create_user(email=data[i], password='nisheet', view=3, view_id=District.objects.get(name=i).id)

    return JsonResponse({"status": "Inserted User Dataset into database"})

def insert_police_station_user_data(request):
    data = {
    "Anjar": ["anjar.pstn.gdam@gmail.com","Anjar"],
    "Bhachau": ["bhachau.pstn.gdam@gmail.com","Bhachau"],
    "Bhuj- A Division": ["polstn-bhuj-kut@gujarat.gov.in","Bhuj"],
    "Bhuj- B Division": ["polstn-bhujrl-kut@gujarat.gov.in","Bhuj"],
    "Bhuj - Womens Division": ["polstn-mahila-kut@gujarat.gov.in","Bhuj"],
    "Gandhidham A Div": ["polstn-gandhi-kut@gurat.gov.in","Gandhidham"],
    "Gandhidham B Div": ["gandhidham-gdam-pstn@gmail.com","Gandhidham"],
    "Mandvi": ["polstn-mandvi-kut@gujarat.gov.in","Manddvi"],
    "Mandvi Marine": ["polstn-mandvi-marine-kut@gujarat.gov.in","Manddvi"],
    "Mundra": ["polstn-mundra-kut@gujarat.gov.in","Mundra"],
    "Mundra Marine": ["polstn-mundra-marine-kut@gujarat.gov.in","Mundra"],
    "Nakhatrana": ["polstn-nakh-kut@gujarat.gov.in","Nakhatrana"],
    "Rapar": ["polstn-rapar-kut@gujarat.gov.in","Rapar"],
    }
    for i in data:
        try:
            PoliceStation(qrId=randrange(000000,999999), name=i, taluka=Taluka.objects.get(name=data[i][1])).save()
            p = PoliceStation.objects.get(name=i)
            debug(i, 'Data Inserted')
            User.objects.create_user(email=data[i][0], password='nisheet', view=1, view_id=p.id)
            debug(data[i][0], 'Data Inserted')
        except: pass
    return JsonResponse({"status": "Inserted User Dataset into database"})