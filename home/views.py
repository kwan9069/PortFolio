from django.shortcuts import render
import datetime
from django.http import HttpResponse,JsonResponse
from .models import News
from .models import Encar,Kcar
from django.db.models import Min,Count
from .functions import to_csv,get_trim
import joblib
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from sklearn.ensemble import RandomForestRegressor



# import xgboost
import numpy as np
# Create your views here.

TEMPLATE_DIRS= (
    'os.path.join(BASE_DIR, "templates"),'
)
def index(request):
    return render(request, "index.html",{})
def buy_1(request):
    return render(request, "buy_1.html",{})

def buy_3(request):

    return render(request, "buy3.html")



def buy_2(request):
    bra = request.GET.get('brand', '')
    na = request.GET.get('name', '')
    mile = request.GET.get('km', '')
    mile1 = request.GET.get('km1', '')
    year = request.GET.get('year', '')
    year1 = request.GET.get('year1', '')
    fuel = request.GET.get("fuel", "")
    loc = request.GET.get("loc", "")
    sort = request.GET.get("ascend","")
    if sort == "ASC":
       info = Encar.objects.filter(brand=bra, name__icontains=na, year__gte=year, year__lte=year1, km__gte=mile,km__lte=mile1, fuel=fuel, location=loc).order_by('price')
    elif sort == "DESC":
       info = Encar.objects.filter(brand=bra, name__icontains=na, year__gte=year, year__lte=year1, km__gte=mile,km__lte=mile1, fuel=fuel, location=loc).order_by('-price')
    info1 = Encar.objects.filter(brand=bra, name__icontains=na, year__gte=year, year__lte=year1, km__gte=mile,km__lte=mile1, fuel=fuel, location=loc).annotate(num=Count('brand'))   
    try:
        total = info1[0].num
        return render(request, "buy_2.html", {'info': info, 'info1': info1,'total':total})
    except:
        return render(request,"buy3.html")




def cars(request):
    return render(request, "cars.html",{})

def topics(request):
    news= News.objects.all()
    paginator=Paginator(news,9)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request, template_name="topics.html",context={'news':page_obj})

def about(request):
    return render(request, "about.html",{})

def main(request):
    return render(request, "main.html",{})

def sell1(request):
    bra = request.GET.get('brand', '')
    na = request.GET.get('name', '')
    trim = request.GET.get('trim', '')
    fuel = request.GET.get("fuel", "")
    year = request.GET.get('year', '')
    acci = request.GET.get('accident', '')
    color = request.GET.get('color', '')
    wd = request.GET.get("wd", "")
    km = request.GET.get("km", "")
    trim1 = get_trim(bra,trim)
    a = to_csv(bra,na,trim1,fuel,year,acci,color,wd,km)
    model = joblib.load('RandomForest.pkl')
    #model = joblib.load('XGBoost.pkl')
    price = model.predict(a)
    price = np.expm1(price)[0]
    num = round(int(price))
    under = round(num*0.95)
    over = round(num*1.05)
    return render(request,'sell1.html',{'price':num,'brand':bra,'name':na,
                                        'under':under,'over':over})


# Create your views here.
# ????????????
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],
                email=request.POST['email'],
            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'signup.html')
    else:
        form = UserCreationForm
        return render(request, 'signup.html', {'form': form})
# ?????????
def login(request):
    # login?????? POST ????????? ???????????? ???, ????????? ????????? ?????????.
    if request.method == 'POST':
        # login.html?????? ????????? username??? password??? ??? ????????? ????????????.
        username = request.POST['username']
        password = request.POST['password']

        # ?????? username??? password??? ???????????? user ????????? ????????????.
        user = auth.authenticate(request, username=username, password=password)

        # ?????? user ????????? ???????????????
        if user is not None:
            # ????????? ??????
            auth.login(request, user)
            return redirect('/')
        # ???????????? ????????????
        else:
            # ??????????????? ?????????????????? ???????????? ?????? login.html ???????????? ????????????.
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    # login?????? GET ????????? ???????????????, ????????? ????????? ????????????.
    else:
        return render(request, 'login.html')


# ????????????
def logout(request):
    # logout?????? POST ????????? ???????????? ???, ???????????? ????????? ?????????.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    # logout?????? GET ????????? ???????????? ???, ?????? ????????? ????????????.
    return render(request, 'main.html')
