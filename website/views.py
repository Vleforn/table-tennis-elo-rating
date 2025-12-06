from django.shortcuts import render

def home(request):
    players = [
        (1, 'Yernur', 1500),
        (2, 'Kassym', 1300),
        (3, 'Almasbek', 1000),
    ]
    return render(request, 'home.html', {'players': players})