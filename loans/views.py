import datetime
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from loans.models import Business,Address,Owners,Requests
from datetime import datetime


@csrf_exempt
def loanapp(request):
    html = "<html><body>It is now</body></html>"
    files = request.FILES
    raw_data = files.get('file').read()
    # print(raw_data)
    parsed = json.loads(raw_data)
    add_to_model(parsed)
    return HttpResponse(html)

@csrf_exempt
def status(request):
    id = request.GET.get('id')
    r = Requests.objects.get(filter_id=id)
    b = r.business
    response = JsonResponse({'name':b.name,'ApplicationUpdated?':b.has_been_updated,'LoanId':id,'RequestedLoanAmount':r.loan_amount})
    return response

def add_to_model(parsed):
    biz_name = parsed['Business']['Name']
    if(Business.objects.filter(name=biz_name).exists()):
        b = Business.objects.get(name=biz_name)
        address = b.address
        address.address1 = parsed['Business']['Address']['Address1']
        address.address2 = parsed['Business']['Address']['Address2']
        address.city = parsed['Business']['Address']['City']
        address.state = parsed['Business']['Address']['State']
        address.zip = int(parsed['Business']['Address']['Zip'])
        address.save()
        b.name = parsed['Business']['Name']
        b.annual_revenue = parsed['Business']['SelfReportedCashFlow']['AnnualRevenue']
        b.avg_bank_balance = parsed['Business']['SelfReportedCashFlow']['MonthlyAverageBankBalance']
        b.avg_credit_card_volume = parsed['Business']['SelfReportedCashFlow']['MonthlyAverageCreditCardVolume']
        b.tax_id = int(parsed['Business']['TaxID'])
        b.phone = int(parsed['Business']['Phone'])
        b.naics = int(parsed['Business']['NAICS'])
        b.has_been_profitable = parsed['Business']['HasBeenProfitable']
        b.bankrupted = parsed['Business']['HasBankruptedInLast7Years']
        b.inception_date = datetime.strptime(parsed['Business']['InceptionDate'][:-7],'%Y-%m-%dT%H:%M:%S.%f')
        b.has_been_updated = True
        b.save()

    else:
        owners = []
        for x in parsed['Owners']:
            name = x['Name']
            first_name = x['FirstName']
            last_name = x['LastName']
            email = x['Email']
            address1 = x['HomeAddress']['Address1']
            address2 = x['HomeAddress']['Address2']
            city = x['HomeAddress']['City']
            state = x['HomeAddress']['State']
            zip = int(x['HomeAddress']['Zip'])
            dob = datetime.fromisoformat(x['DateOfBirth'])
            phone = int(x['HomePhone'])
            ssn = int(x['SSN'])
            percent_own = float(x['PercentageOfOwnership'])
            a = Address(address1=address1, address2=address2, city=city, state=state, zip=zip)
            a.save()
            o = Owners(name=name,first_name=first_name,last_name=last_name,email=email,dob=dob,phone=phone,ssn=ssn,percent_own=percent_own,address=a)
            o.save()
            owners = owners + [o]
            
        address1 = parsed['Business']['Address']['Address1']
        address2 = parsed['Business']['Address']['Address2']
        city = parsed['Business']['Address']['City']
        state = parsed['Business']['Address']['State']
        zip = int(parsed['Business']['Address']['Zip'])
        a = Address(address1=address1, address2=address2, city=city, state=state, zip=zip)
        a.save()
        

        name = parsed['Business']['Name']
        annual_revenue = parsed['Business']['SelfReportedCashFlow']['AnnualRevenue']
        avg_bank_balance = parsed['Business']['SelfReportedCashFlow']['MonthlyAverageBankBalance']
        avg_credit_card_volume = parsed['Business']['SelfReportedCashFlow']['MonthlyAverageCreditCardVolume']
        tax_id = int(parsed['Business']['TaxID'])
        phone = int(parsed['Business']['Phone'])
        naics = int(parsed['Business']['NAICS'])
        has_been_profitable = parsed['Business']['HasBeenProfitable']
        bankrupted = parsed['Business']['HasBankruptedInLast7Years']
        inception_date = datetime.strptime(parsed['Business']['InceptionDate'][:-7],'%Y-%m-%dT%H:%M:%S.%f')
        has_been_updated = False
        b = Business(name=name, annual_revenue = annual_revenue, avg_bank_balance = avg_bank_balance, avg_credit_card_volume=avg_credit_card_volume,tax_id=tax_id, phone=phone, naics=naics, has_been_profitable=has_been_profitable, bankrupted=bankrupted, inception_date=inception_date,has_been_updated=has_been_updated, address=a)
        b.save()
        b.owners.set(owners)

        loan_amount = float(parsed['CFApplicationData']['RequestedLoanAmount'])
        credit_history = int(parsed['CFApplicationData']['StatedCreditHistory'])
        entity_type = parsed['CFApplicationData']['LegalEntityType']
        filter_id = int(parsed['CFApplicationData']['FilterID'])

        r = Requests(loan_amount=loan_amount, credit_history=credit_history, entity_type=entity_type, filter_id=filter_id, business=b)
        r.save()