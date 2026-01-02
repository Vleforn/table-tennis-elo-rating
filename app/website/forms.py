from django import forms
from django.contrib.auth.models import User
from .models import Player, Match, EloParameter

class LoginForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    password = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))

    class Meta:
        model = User
        fields = '__all__'

class AddPlayerForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'class': 'add-player-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'class': 'add-player-input', 'placeholder': 'Фамилия'}))

    class Meta:
        model = Player
        fields = '__all__'

class AddMatchForm(forms.ModelForm):
    player_one = forms.ModelChoiceField(queryset=Player.objects.all(), empty_label='Игрок 1', widget=forms.Select(attrs={'class': 'match-player'}))
    score_one = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'match-score', 'min': '0', 'value': '0'}))
    player_two = forms.ModelChoiceField(queryset=Player.objects.all(), empty_label='Игрок 2', widget=forms.Select(attrs={'class': 'match-player'}))
    score_two = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'match-score', 'min': '0', 'value': '0'}))

    class Meta:
        model = Match
        fields = '__all__'

class EloParameterForm(forms.ModelForm):
    k_index = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    start_elo = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = EloParameter
        fields = '__all__'
