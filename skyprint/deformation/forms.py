from django import forms

class coordsForm(forms.Form):
    coordsList = forms.CharField(label='List of coordonnates',
                            widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'id' : 'coords', 'value' : '[]'}))
        
