from django.shortcuts import render, redirect
from .models import Mesto, Interesovanja, Vreme
from django.db.models import F, Q
from .forms import SearchForm

from datetime import datetime
from .classes import MestaIzKategorije

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

import numpy as np

import requests

from django.http import Http404

# Create your views here.
def index(request):
	form = SearchForm()
	
	h = datetime.now().hour
	d = datetime.now().date()
	
	vreme = Vreme.objects.filter(datum = d)
	
	if vreme.count() == 0:
		r = requests.post('http://api.openweathermap.org/data/2.5/weather?id=792680&appid=cc9934a4bdb01e9e84dc40c802176c63')
		vreme = Vreme.objects.create(datum = d, opis = r.json())
		print(r.json())
	else:
		print('vec imam info')
	
	kategorijeImena = [ 'parkovi', 'spomenici', 'kafići/kafane', 'muzeji', 'pozorišta', 'bioskopi', 'hoteli', 'tvrđave', 'trgovi', 'verski objekti', 'ostalo' ]
	
	preporuciKategorije = []
	
	if ( request.user.is_authenticated and request.user.username != 'faks' ):
		interesovanja = Interesovanja.objects.filter(korIme = request.user.username)
		
		poseta = []
		
		interesnihKategorija = 0
		
		for int in interesovanja:
			poseta.append(int.parkovi)
			poseta.append(int.spomenici)
			poseta.append(int.kafici)
			poseta.append(int.muzeji)
			poseta.append(int.pozorista)
			poseta.append(int.bioskopi)
			poseta.append(int.hoteli)
			poseta.append(int.tvrdjave)
			poseta.append(int.trgovi)
			poseta.append(int.verski)
			poseta.append(int.ostalo)
		
		avg = np.mean(poseta)
		
		if avg != 0:
			avg += (np.max(poseta) - avg) * 0.3
			
			for int in interesovanja:
				if int.parkovi >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(1)
				if int.spomenici >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(2)
				if int.kafici >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(3)
				if int.muzeji >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(4)
				if int.pozorista >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(5)
				if int.bioskopi >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(6)
				if int.hoteli >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(7)
				if int.tvrdjave >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(8)
				if int.trgovi >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(9)
				if int.verski >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(10)
				if int.ostalo >= avg:
					interesnihKategorija += 1
					preporuciKategorije.append(11)
				
		if interesnihKategorija < 3:
			if ( h >= 6 and h <= 15  ):
				preporuciKategorije.append(1)
				
			if h >= 18:
				preporuciKategorije.append(3)
	else:
		if ( h >= 6 and h <= 18 ):
			preporuciKategorije.append(1)
		
		if h >= 18:
			preporuciKategorije.append(3)
	
	lista = []
	
	for k in preporuciKategorije:
		mik = MestaIzKategorije()
		mik.kategorija = kategorijeImena[ k - 1 ]
		mik.mesta = Mesto.objects.filter(tip = k).order_by('-brojac')[:6]
		lista.append(mik)
	
	context = {
		'form': form,
		'lista': lista,
		'h': h,
	}
	
	return render(request, 'preporucivac/index.html', context)
	
def details(request, id):
	form = SearchForm()
	
	try:
		mesto = Mesto.objects.filter(pk = id)
	except Mesto.DoesNotExist:
		raise Http404("Mesto ne postoji.")
	mesto.update(brojac=F('brojac') + 1)
	mesto = Mesto.objects.get(pk = id)
	
	tipovi = ["Parkovi", "Spomenici", "Kafići/kafane", "Muzeji", "Pozorišta", "Bioskopi", "Hoteli", "Tvrđave", "Trgovi", "Verski objekti", "Ostalo"]
	
	if request.user.is_authenticated:
		kat = [ 'parkovi', 'spomenici', 'kafici', 'muzeji', 'pozorista', 'bioskopi', 'hoteli', 'tvrdjave', 'trgovi', 'verski', 'ostalo' ]
		
		interesovanja = Interesovanja.objects.filter(korIme = request.user.username)
		
		if mesto.tip == 1:
			interesovanja.update(parkovi=F('parkovi') + 2)
		elif mesto.tip == 2:
			interesovanja.update(spomenici=F('spomenici') + 2)
		elif mesto.tip == 3:
			interesovanja.update(kafici=F('kafici') + 2)
		elif mesto.tip == 4:
			interesovanja.update(muzeji=F('muzeji') + 2)
		elif mesto.tip == 5:
			interesovanja.update(pozorista=F('pozorista') + 2)
		elif mesto.tip == 6:
			interesovanja.update(bioskopi=F('bioskopi') + 2)
		elif mesto.tip == 7:
			interesovanja.update(hoteli=F('hoteli') + 2)
		elif mesto.tip == 8:
			interesovanja.update(tvrdjave=F('tvrdjave') + 2)
		elif mesto.tip == 9:
			interesovanja.update(trgovi=F('trgovi') + 2)
		elif mesto.tip == 10:
			interesovanja.update(verski=F('verski') + 2)
		elif mesto.tip == 11:
			interesovanja.update(ostalo=F('ostalo') + 2)
		
	context = {
		'mesto': mesto,
		'form': form,
		'tip': tipovi[mesto.tip - 1],
	}
	
	return render(request, 'preporucivac/details.html', context)
	
def search(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		
		q = request.POST['q']
		qs = q.split(" ");
		
		kategorije = request.POST.getlist('kategorija')
		
		mesta_sva = Mesto.objects.all();
		
		mesta = Mesto.objects.none()
		
		for q in qs:
			mesta |= mesta_sva.filter(naziv__contains = q)
		
		if len(kategorije) != 0:
			mesta = mesta.filter(tip__in=kategorije)
		
		mesta = mesta.order_by('-brojac')
		
		broj = len(mesta)
		
		novaMesta = None
		
		if broj < 5:
			if len(kategorije) != 0:
				novaMesta = Mesto.objects.exclude(pk__in = mesta.values_list('pk', flat = True)).filter(tip__in = kategorije).order_by('-brojac')[:(5 - broj)]
			else:
				novaMesta = Mesto.objects.exclude(pk__in = mesta.values_list('pk', flat = True)).order_by('-brojac')[:(5 - broj)]
		
		context = {
			'mesta' : mesta,
			'novaMesta' : novaMesta,
			'form' : form,
		}
		
		return render(request, 'preporucivac/results.html', context)
	else:
		return redirect(request.META.get('HTTP_REFERER', '/preporucivac/'), permanent = True)

def register(request):
	if request.user.is_authenticated:
		return redirect('/preporucivac/')
		
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			
			username = form.cleaned_data.get('username')
			
			interesovanja = Interesovanja(korIme = username, parkovi = 0, spomenici = 0, kafici = 0, muzeji = 0, pozorista = 0, bioskopi = 0, hoteli = 0, tvrdjave = 0, trgovi = 0, verski = 0, ostalo = 0)
			interesovanja.save(force_insert=True)
			
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/preporucivac/')
	else:
		form = UserCreationForm()
	return render(request, 'preporucivac/register.html', { 'form' : form })
	
def login_view(request):
	if request.user.is_authenticated:
		return redirect('/preporucivac/')
		
	if request.method == 'POST':
		form = AuthenticationForm(request.POST)
		print('Stigao do x\n')
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/preporucivac/')
	else:
		form = AuthenticationForm()
	return render(request, 'preporucivac/login.html', { 'form' : form })
	
def logout_view(request):
	logout(request)
	return redirect('/preporucivac/')
		