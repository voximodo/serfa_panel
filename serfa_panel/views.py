from serfa_panel.models import measurement, Sensor, Unit, user_sensor
from django.utils import timezone
import datetime
from django.template.loader import get_template
from django.http import HttpResponse
from serfa.forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from serfa_panel.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

#dodawanie pomiaru przez API
def add_mes(request):
    if 'mad' in request.GET and 'key' in request.GET and 'value' in request.GET and 'unit' in request.GET:

        key = request.GET['key']
        value = request.GET['value']
        unit = request.GET['unit']
        try:
            s = Sensor.objects.get(key=key)
        except:
            return HttpResponse('Błędny klucz autoryzacyjny!')
        try:
            u = Unit.objects.get(key=unit)
        except:
            return HttpResponse('Błędna jednostka!')

        #usuwanie gdy baza danych jest przepelniona
        lp = measurement.objects.filter(sensor=s)
        if (len(lp) >= s.max):
            lp.order_by('date')
            td = lp[0]
            td.delete()

        m = measurement(sensor=s, date=datetime.datetime.now(), value=value, unit=u)
        m.save()
        return HttpResponse('Success!')

    else:
        return HttpResponse('Błędna składnia.')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Aktywuj swoje konto w panelu SerFa IoT'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 's_signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    current_user = request.user
    t = get_template('account_activation_sent.html')
    html = t.render()
    return HttpResponse(html)

def profile_after_login(request):
    current_user = request.user
    lm = dict()
    ls = user_sensor.objects.filter(user=current_user)
    for us in ls:
        lm[us] = get_last(us.sensor)
    u = Unit.objects.all()
    t = get_template('h_home.html')
    html = t.render(({'username': current_user.username, 'mes': lm, 'units': u}))
    return HttpResponse(html)

def change_password(request):
    current_user = request.user
    t = get_template('h_home.html')
    html = t.render(({'username': current_user.username}))

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'p_password.html', {
            'form': form
        })

    return HttpResponse(html)

#lista czujnikow
def sensors(request):
    current_user = request.user
    sensor_list = user_sensor.objects.filter(user=current_user)
    t = get_template('l_list.html')
    html = t.render({'sensor_list': sensor_list})
    return HttpResponse(html)

#ekran czujnika
def sensorview(request):

    current_user = request.user
    if 'key' in request.GET and request.GET['key']:
        key = request.GET['key']
        try:
            s = Sensor.objects.get(key=key)
        except:
            return HttpResponse('Błędny klucz autoryzacyjny!')

        us = user_sensor.objects.get(user=current_user, sensor=s)

        days = 1

        if 'nazwa' in request.GET and request.GET['nazwa']:
            nazwa = request.GET['nazwa']
            us.name = nazwa
            us.save()

        if 'delete' in request.GET and request.GET['delete']:
            us.delete()
            return redirect('sensorslist')

        if 'clean' in request.GET and request.GET['clean']:
            measurement.objects.filter(sensor=s).delete()

        if 'days' in request.GET and request.GET['days']:
            days = int(request.GET['days'])
            if (days > 31):
                days = 1

        units = Unit.objects.all()
        last_mes = []
        x = []
        y = []
        d = timezone.now() - datetime.timedelta(days=5000)
        m = dict()
        enddate = datetime.datetime.now()
        startdate = datetime.datetime.now() - datetime.timedelta(days=days)
        q = len(measurement.objects.filter(sensor=s))
        for index in range(len(units)):
            lp = measurement.objects.filter(sensor=s, unit=units[index])
            if (len(lp)>0):
                lp.order_by('date')
                last_mes.append(lp[len(lp)-1])
                if (lp[len(lp)-1].date > d):
                    d  = lp[len(lp)-1].date
                lp = measurement.objects.filter(sensor=s, unit=units[index], date__range=[startdate, enddate])
                lp.order_by('date')
                leng = len(lp)
                if (leng > 0):
                    if (leng > 100):
                        hm = int(leng/60)
                        lp = lp[::hm]
                    m[units[index].name] = (lp)

        t = get_template('s_sensor.html')
        html = t.render({'user_sensor': us, 'last_mes' : last_mes, 'sensor' : s, 'date' : d, 'mess' : m, 'day':days, 'quan':q})
        return HttpResponse(html)

#dodawanie czujnika
def addsensor(request):
    t = get_template('a_add.html')
    if 'pwd' in request.GET and request.GET['pwd']:
        if 'name' in request.GET and request.GET['name']:
            current_user = request.user
            key = request.GET['pwd']
            name = request.GET['name']
            try:
                if(len(user_sensor.objects.filter(sensor=Sensor.objects.get(key=key), user=current_user))>0):
                    html = t.render({'alert': 'Sensor znajduje się już w twojej bazie danych!'})
                    return HttpResponse(html)
                us = user_sensor(name=name, sensor=Sensor.objects.get(key=key), user=current_user)
            except:
                html = t.render({'alert': 'Błędny klucz autoryzacyjny!'})
                return HttpResponse(html)

            us.save()
            html = t.render({'succ': 'Pomyślnie dodano czujnik do twojej bazy danych.'})
            return HttpResponse(html)

    current_user = request.user
    html = t.render()
    return HttpResponse(html)

#diagnostyka - poki co reczne sprawdzanie
def checkeverything(request):
    sen = Sensor.objects.all()
    for s in sen:
        check_premium(s)
    return HttpResponse('Skonczono!')

#to be worked
#pobieranie ostatnich pomiarow
def get_last(Sensorr):
    units = Unit.objects.all()
    last_mes = []
    q = len(measurement.objects.filter(sensor=Sensorr))
    for index in range(len(units)):
        try:
            lp = measurement.objects.filter(sensor=Sensorr, unit=units[index]).order_by('-date')[0]
            last_mes.append(lp)
            Sensorr.last_synchro = lp.date
            Sensorr.save()
        except:
            print('error')

    return last_mes

#sprawdzanie czy czujnik posiada wersje premium
def check_premium(Sensorr):
    d = timezone.now()
    if d > Sensorr.premium_date:
        Sensorr.is_premium = 0
        Sensorr.max = 800
        Sensorr.save()
        clean(Sensorr)
    else:
        Sensorr.is_premium = 1
        Sensorr.max = 10000

    Sensorr.save()

#czyszczenie danych czujnika do maksymalnej wartosci
def clean(Sensorr):
    ms = measurement.objects.filter(sensor=Sensorr).order_by('date')
    hm = len(ms) - Sensorr.max
    if (hm > 0):
        sd = ms[0].date
        ed = ms[hm-1].date
        measurement.objects.filter(sensor=Sensorr, date__range=[sd, ed]).delete()