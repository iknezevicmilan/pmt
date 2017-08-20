from django import forms

class SearchForm(forms.Form):
	q = forms.CharField(label = 'Pretraga', max_length = 256, required = False, widget = forms.TextInput(attrs = {'size' : 100}))
	
	KATEGORIJE = (
		(1, 'parkovi'),
		(2, 'spomenici'),
		(3, 'kafići/kafane'),
		(4, 'muzeji'),
		(5, 'pozorišta'),
		(6, 'bioskopi'),
		(7, 'hoteli'),
		(8, 'tvrđave'),
		(9, 'trgovi'),
		(10, 'verski objekti'),
		(11, 'ostalo'),
	)
	
	kategorija = forms.MultipleChoiceField(choices = KATEGORIJE, required = False, widget = forms.CheckboxSelectMultiple)