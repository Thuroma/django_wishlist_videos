from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
# makes sure users are logged in to view
from django.contrib.auth.decorators import login_required
# http response forbidden returns to bad actors accessing other user's content

# Shows temporary message to user
from django.contrib import messages


@login_required
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST)   # creates a form
        place = form.save(commit=False)     # creating a model object from form, , checks for integrety errors
        place.user = request.user
        if form.is_valid():     # validation against DB constraints
            place.save()        # saves place to db
            return redirect('place_list')   # reloads home page (from urls.py)

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()     # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk) - a pk that doesn't exist will skip to reload template
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('places_visited')


@login_required
def about(request):
    author = 'Thurman'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # Does this place belong to the current user?
    if place.user != request.user:
        HttpResponseForbidden

    # Is this a GET request (show data + form), or a POST request (update Place object)

    # if POST request, validate form and update
    # POST form never shown, used to encapsulate data that has been sent as part of the web request
    # Data is information filled into the form on the template
    if request.method == 'POST':
        # make new trip review form (imported ^)
        # request.POST is data in the form 
        # request.FILES are any files uploaded
        # instance is the place model instance in the database
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            # updates place object with the data provided
            form.save()
            messages.info(request, 'Trip information updated')
        else:
            messages.error(request, form.errors)

        # Return the user to the datail page for this place
        return redirect('place_details', place_pk=place_pk)

    else:
        # if Get request, show place info and optional form
        # if place is visited, show form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        # if place not visited, no form
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden

