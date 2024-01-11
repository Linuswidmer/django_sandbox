from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Player  # Assuming you have a Player model

app_name = "spa"

@csrf_exempt
def start_game(request):
    if request.method == 'POST':
        # Extract player name from the POST data
        player_name = request.POST.get('playerName')

        if player_name:
            # Check if a player with the given name already exists
            existing_player = Player.objects.filter(name=player_name).first()

            if existing_player:
                # Player already exists, update the waiting status
                existing_player.is_waiting = True
                existing_player.save()

                response_data = {
                    'status': 'success',
                    'name': existing_player.name,
                    'wins': existing_player.num_wins,  # Adjust based on your model
                    'losses': existing_player.num_losses,  # Adjust based on your model
                }
            else:
                # Player does not exist, create a new player
                new_player = Player(name=player_name, is_waiting=True)
                new_player.save()

                response_data = {
                    'status': 'success',
                    'name': new_player.name,
                    'wins': new_player.num_wins,  # Adjust based on your model
                    'losses': new_player.num_losses,  # Adjust based on your model
                }

            # Return a JSON response indicating success
            return JsonResponse(response_data)

    # Return an error response if something went wrong
    return JsonResponse({'status': 'error'})

def index(request):
    context = {}
    return render(request, "spa/index.html", context)