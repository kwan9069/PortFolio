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
# 회원가입
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
# 로그인
def login(request):
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)

        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
    else:
        return render(request, 'login.html')


# 로그아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    # logout으로 GET 요청이 들어왔을 때, 메인 화면을 띄워준다.
    return render(request, 'main.html')
