from django.db import models

# Create your models here.
class Mesto(models.Model):
	naziv = models.CharField(max_length=256)
	tip = models.IntegerField()
	slika = models.CharField(max_length=256)
	opis = models.TextField()
	adresa = models.CharField(max_length=256)
	linije = models.CharField(max_length=256)
	referenca = models.CharField(max_length=256)
	brojac = models.BigIntegerField()
	
	def __str__(self):
		return self.naziv
		
class Interesovanja(models.Model):
	korIme = models.CharField(max_length=150)
	parkovi = models.BigIntegerField()
	spomenici = models.BigIntegerField()
	kafici = models.BigIntegerField()
	muzeji = models.BigIntegerField()
	pozorista = models.BigIntegerField()
	bioskopi = models.BigIntegerField()
	hoteli = models.BigIntegerField()
	tvrdjave = models.BigIntegerField()
	trgovi = models.BigIntegerField()
	verski = models.BigIntegerField()
	ostalo = models.BigIntegerField()
	
	def __str__(self):
		return self.korIme
		
class Vreme(models.Model):
	datum = models.DateField()
	opis = models.TextField()
	
	def __str__(self):
		return str(self.datum)