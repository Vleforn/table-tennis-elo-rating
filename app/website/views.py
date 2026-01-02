from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .models import Player, Match, RatingRecords, EloParameter
from django.db.models import Window, F
from django.db.models.functions import Rank
from .forms import AddPlayerForm, AddMatchForm, EloParameterForm
from django.contrib import messages
from .elo_calc import update_rating
from .queries import get_curr_rating
from django.core.paginator import Paginator

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.success(request, 'There was error with logging in. Please, try again...')
            return redirect('login_page')
    else:
        return render(request, 'login_page.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out')
    return redirect('home')

def control_center(request):
    if request.user.is_authenticated:
        parameters = EloParameter.objects.first()
        if request.method == 'POST':
            elo_parameter_form = EloParameterForm(request.POST, instance=parameters)
            if elo_parameter_form.is_valid():
                elo_parameter_form.save()
                # recalculate all ratings
            return redirect('control_center')
        else:
            elo_parameter_form = EloParameterForm(instance=parameters)
            return render(request, 'control_center.html', {'elo_parameter_form': elo_parameter_form})
    else:
        messages.success(request, 'You must be logged in to see that page')
        return redirect('home')


def home(request):
    curr_rating = get_curr_rating()
    players = curr_rating.annotate(
        rank=Window(
            expression=Rank(),
            order_by=F('curr_rating').desc()
        )
    ).order_by('rank')
    players_paginator = Paginator(players, 20)
    players_page_number = request.GET.get('players_page', 1)
    players_page_obj = players_paginator.get_page(players_page_number)

    matches = Match.objects.all().order_by('-created_at')
    matches_paginator = Paginator(matches, 20)
    matches_page_number = request.GET.get('matches_page', 1)
    matches_page_obj = matches_paginator.get_page(matches_page_number)

    if request.user.is_authenticated:
        add_player_form = AddPlayerForm()
        add_match_form = AddMatchForm()
        return render(
            request,
            'home.html',
            {'players_page_obj': players_page_obj, 'matches_page_obj': matches_page_obj, 'add_player_form': add_player_form, 'add_match_form': add_match_form})
    else:
        return render(request, 'home.html', {'players_page_obj': players_page_obj, 'matches_page_obj': matches_page_obj})

def player(request):
    players = Player.objects.all()

    return render(request, 'player.html', {'players': players,})

def add_player(request):
    if request.method == "POST":
        add_player_form = AddPlayerForm(request.POST)
        if add_player_form.is_valid():

            # add player into the db
            player = add_player_form.save()

            # add starting rating into the db
            parameters = EloParameter.objects.first()
            rating_record = RatingRecords(player=player, rating=parameters.start_elo)
            rating_record.save()

            messages.success(request, 'Новый игрок добавлен')
        return redirect('home')
    else:
        add_player_form = AddPlayerForm()
        return render(request, 'add_player.html', {'form': add_player_form})


def match(request):
    matches = Match.objects.all().order_by('-created_at')
    return render(request, 'match.html', {'matches': matches})

def add_match(request):
    if request.method == 'POST':
        add_match_form = AddMatchForm(request.POST)
        if add_match_form.is_valid():
            match = add_match_form.save()

            # get curr rating
            curr_rating = get_curr_rating()
            player_one = curr_rating.get(pk=match.player_one.id)
            player_two = curr_rating.get(pk=match.player_two.id)

            # calc new rating
            upd_rating_one, upd_rating_two = update_rating(player_one.curr_rating, match.score_one, player_two.curr_rating, match.score_two)
            
            # update rating
            RatingRecords(player=match.player_one, rating=upd_rating_one, match=match).save()
            RatingRecords(player=match.player_two, rating=upd_rating_two, match=match).save()
            messages.success(request, 'Новый матч добавлен')
        return redirect('home')
    else:
        add_match_form = AddMatchForm()
        return render(request, 'add_match.html', {'form': add_match_form})

def rating(request):
    records = RatingRecords.objects.all()
    return render(request, 'rating.html', {'records': records})
