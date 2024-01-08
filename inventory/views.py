from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import medicines,bill,invoice,profile,backup
from .scrap import fetchDetail
import json
import itertools
import datetime 
import os
import shutil
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
cwd = os.getcwd()

def checkProfile(request):
    try:
        profile.objects.get(id=1)
    except:
        return True


# upadting the stock
# @login_required
def updateInventory(request):
    if checkProfile(request):
        return redirect('/setup')
    if request.method == 'POST':
        name = request.POST['name']
        TPP = request.POST.get("TPP")
        price = float("{:.2f}".format(float(request.POST.get("price"))/(int(TPP))))
        purchasePrice = float("{:.2f}".format(float(request.POST.get("Pprice"))/int(TPP)))
        batchNo = request.POST.get("BatchNo")
        composition = request.POST.get("composition")
        quantity = request.POST.get("quantity")
        HSN = request.POST.get("HSN")
        expiry = request.POST.get("expiry")
        med =medicines()
        med.name = name
        med.price = price
        med.composition = composition
        med.quantity = quantity
        med.purchasedPrice = purchasePrice
        med.batchNo = batchNo
        med.HSN = HSN
        med.expiryDate = expiry
        med.save()
        return redirect('/')
    return render(request,"inventory.html")

# Render bill generator page, for adding transactions
def billing(request):
    if checkProfile(request):
        return redirect('/setup')
    return render(request,'billing.html')

# Fetch composition of unknown drug(relative to stock)
def getComposition(request):
    if request.method == 'POST':
        name =json.loads(request.body.decode('utf-8')).get('name')
        medName, composition = fetchDetail(name)
        return JsonResponse({"medName":medName,"composition":composition})

# Find alternative of unknown drug
def findAlternative(request):
    if request.method == 'POST':
        name = request.body.decode('utf-8').split("=")[1].replace("+"," ")
        x,comp = fetchDetail(name)
        # try:
        #     comp = medicines.objects.get(name=name).composition
        #     print("Here")
        # except:
        # print(comp)
        try:
            alts = medicines.objects.filter(composition= comp, quantity__gte=1)
        except:
            alts = []
        # print(alts)
        res = {}
        for alt in alts:
            res[alt.name] = [alt.quantity,alt.price]
        if(len(alts)!=0):
            return JsonResponse(res)
        altsalt = comp.split('-')[0]
        med = medicines.objects.filter(composition__icontains=altsalt, quantity__gte=1)
        res = {}
        asalt = set([])
        for alt in med:
            res[alt.name] = [alt.quantity,alt.price]
            asalt.add(alt.composition)
        res["FetchedComp"] = [comp,list(asalt)]
        # print(res)
        return JsonResponse(res)

# Auto complete form finding meds in stock
def findMedicine(request):
    if request.method == 'POST':
        name = request.body.decode('utf-8').split("=")[1].replace("+"," ")
        # print("----",name)
        med = medicines.objects.filter(name__icontains=name , quantity__gte=1)
        print(med)
        res = {}
        for i in range(len(med)):
            res[str(i)] = med[i].name
            # print(med[i].name)
        return JsonResponse(res)

def getprice(request, name):
    try:
        med = medicines.objects.filter(name=name, quantity__gte=1)[0]
        return JsonResponse({"price":med.price,"quantity":med.quantity})
    except:
        return JsonResponse({"price":"Not Available","quantity":"Not Available"})
    
def generateBill(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = json.loads(data)
        # print(data)
        name = data.get('patient')
        doctor = data.get('doctor')
        total = data.get('total')
        discount = data.get('discount')
        subtotal = data.get('subtotal')
        meds = data.get('medicines')
        for i in meds.keys():
            newEntry = bill()
            medName = meds[i].get('medicine')
            quantity = meds[i].get('quantity')
            med = medicines.objects.get(name=medName)
            if int(quantity) > int(med.quantity):
                return JsonResponse({"status":"StockOut","med":medName,"stock": med.quantity})
        newBill = invoice.objects.create(name = name,doctor = doctor,total = total,discount = discount, subtotal = subtotal)

        for i in meds.keys():
            newEntry = bill()
            medName = meds[i].get('medicine')
            quantity = meds[i].get('quantity')
            med = medicines.objects.get(name=medName,quantity__gte=1)
            med.quantity = int(med.quantity) - int(quantity)
            med.save()
            newEntry = bill.objects.create(meds=med,quantity=quantity)
            newBill.meds.add(newEntry)

        billId = newBill.id
        # print(billId)
        res = {}
        res['status'] = "success"
        res['billId'] = billId
        return JsonResponse(res)

def fetchBill(request,name):
    bill = invoice.objects.get(id=name)
    meds = bill.meds.all()
    firmData = profile.objects.get(id=1)
    return render(request,'bill.html',{'bill':bill,'data':meds,'firmData':firmData})

@login_required
def analysis(request):
    if checkProfile(request):
        return redirect('/setup')
    monthsList = ["",'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    try:
        data = bill.objects.all()
        if not data.exists():
            return render(request,'analysis.html',{'isData':False})

    except:
        return render(request,'analysis.html',{'isData':False})
    res = {}
    for i in data:
            if i.meds.name in res.keys():
                res[i.meds.name] += i.quantity
            else:
                res[i.meds.name] = i.quantity
    # print(res)
    dict(sorted(res.items(), key=lambda item: item[1]))
    dict(itertools.islice(res.items(), 10))
    key = list(res.keys())
    value = list(res.values())
    medFrequency = {}
    medFrequency["MedicineName"] = key
    medFrequency["Frequency"] = value
    medFrequency['min'] = min(value)
    medFrequency['max'] = max(value)
    # Sales
    sales = invoice.objects.all()
    salesData = {}
    dailySales = {}
    earning = {"Revenue":0,"shopPrice":0}
    currentMonth, currentYear = datetime. datetime.now().date().month, str(datetime. datetime.now().date().year)
    if currentMonth<10:
        currentMonth = "0"+str(currentMonth)
    
    mdate = "-".join([str(currentYear),str(currentMonth)])

    for data in sales:
        month = "-".join(str(data.date).split("-")[:2:])
        currdate = "-".join(str(data.date).split("-")[2::])
        newMonth = "-".join([monthsList[int(month.split('-')[1])],month.split("-")[0]])
        if(newMonth not in salesData.keys()):
            salesData[newMonth] = {"Revenue": data.total, "Earned": sum([(round((res.meds.price*res.quantity)*100)/100 - round((res.meds.purchasedPrice*res.quantity)*100)/100) for res in (rev for rev in data.meds.all())]), "Sold": sum([res.quantity for res in (rev for rev in data.meds.all())])}
        else:
            salesData[newMonth] = {"Revenue": salesData[newMonth]['Revenue']+data.total,"Earned": salesData[newMonth]['Earned'] + sum([(res.meds.price*res.quantity - res.meds.purchasedPrice*res.quantity) for res in (rev for rev in data.meds.all())]), "Sold": salesData[newMonth]['Sold'] + sum([res.quantity for res in (rev for rev in data.meds.all())])}
        salesData[newMonth]['Earned'] = salesData[newMonth]['Earned'] - data.discount
        earning['Revenue'] += data.total
        earning['shopPrice'] += sum([(res.meds.purchasedPrice*res.quantity) for res in (rev for rev in data.meds.all())])
        if(month == mdate):
            if currdate not in dailySales:
                dailySales[str(currdate)] = {"Revenue": data.total}
            else:
                dailySales[str(currdate)] = {"Revenue" : dailySales[str(currdate)]['Revenue']+data.total}
    salesMonth = {}
    salesMonth["Month"] = "-".join([monthsList[int(mdate.split('-')[1])],mdate.split("-")[0]])

    earning["Earned"] = earning['Revenue'] - earning['shopPrice']
    earning = json.loads(json.dumps(earning))
    # print(dailySales,salesData,earning)
    return render(request,'analysis.html',{'isData':True,'data':medFrequency,'sales':salesData,'daily':dailySales,'earning':earning,'salesMonth': salesMonth})

@login_required
def StockItems(request):
    if checkProfile(request):
        return redirect('/setup')
    data = medicines.objects.filter(quantity__gte=1)
    return render(request,'items.html',{'data':data})

def checkQuantity(request):
    name =request.body.decode('utf-8')
    name = json.loads(name)
    name = name.get('name')
    med = medicines.objects.get(name=name)
    return JsonResponse({"quantity":med.quantity})


@login_required
def setup(request):
    if request.method == 'POST':
        name = request.POST.get('Sname')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        gst = request.POST.get('gst')
        upiid = request.POST.get('upiid')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        dlno = request.POST.get('dlno')
        usr = request.user
        try:
            data = profile.objects.get(id = 1)
            data.name = name
            data.address1 = address1
            data.address2 = address2
            data.city = city
            data.state = state
            data.pincode = pincode
            data.GSTNo = gst
            data.UPIid = upiid
            data.phone = phone
            data.email = email
            data.dlno = dlno
            data.save()

            return redirect('/setup')
        except:
            profile.objects.create(name=name,address1=address1,address2=address2,city=city,state=state,pincode=pincode,GSTNo=gst,UPIid=upiid,phone=phone,email=email,dlno=dlno,ownerName=usr)
            return redirect('/setup')
    try:
        data = profile.objects.get(id = 1)
        return render(request,'setup.html',{'data':data,'isData':True})
    except:
        return render(request,'setup.html',{'isData':False})

@login_required
def oldInventory(request):
    if checkProfile(request):
        return redirect('/setup')
    data = medicines.objects.filter(quantity__lte=1)
    return render(request,'oldstock.html',{'data':data})

@login_required
def backupdb(request):
    if checkProfile(request):
        return redirect('/setup')
    if request.method == 'POST':
        base_dir = cwd+"\\db.sqlite3"
        new_dir = "\\".join(cwd.split("\\")[:len(cwd.split("\\"))-1:])
        id = backup()
        id.name = str(new_dir+"\\backup")
        id.save()
        try:
            os.mkdir(new_dir+"\\backup")
            shutil.copy(base_dir,new_dir+"\\backup\\db"+str(id.id)+".sqlite3")
        except:
            shutil.copy(base_dir,new_dir+"\\backup\\db"+str(id.id)+".sqlite3")
        
        return redirect('/backup')
    try:
        data = backup.objects.all()
        return render(request,'backup.html',{'data':data,'isData':True})
    except:
        return render(request,'backup.html',{'isData':False})


def findMedicineByComposition(request):
    if request.method == 'POST':
        comp = request.body.decode('utf-8').split("=")[1].upper()
        data = medicines.objects.filter(composition__icontains=comp, quantity__gte=1)
        res = {}
        for i in range(len(data)):
            res[i] = data[i].composition
        return JsonResponse(res)

def findMedicineByName(request):
    if request.method == 'POST':
        name = request.body.decode('utf-8').upper()
        name = json.loads(name)['MED']
        data = medicines.objects.filter(composition=name, quantity__gte=1)
        res = {}
        for alt in data:
            res[alt.name] = [alt.quantity,alt.price]
        return JsonResponse(res)