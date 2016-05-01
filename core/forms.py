from django import forms


class ImportCsvForm(forms.Form):
    channel = forms.CharField(
        label='Channel',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'light-blue-border',
            'placeholder': 'Name of the channel to be updated/created'
        })
    )
    file = forms.FileField()
