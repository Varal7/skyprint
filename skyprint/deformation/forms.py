from django import forms
import json

class CoordsField(forms.CharField):
    def to_python(self, value):
        #"Normalize data into array"
        if not value:
            return []
        print(json.loads(value))
        return json.loads(value)


class coordsForm(forms.Form):
    coordsList = CoordsField(label='List of coordonnates',
                            widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'id' : 'coords', 'value' : '[]'}))
