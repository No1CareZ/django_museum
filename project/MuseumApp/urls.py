"""URLs of MuseumApp."""
from django.urls import path

from .views import (
    FloorListView, ExpositionListView, ExhibitView,
    ExpositionCreationView, ExpositionUpdateView, ExpositionDeleteView,
    ExhibitCreationView, ExhibitUpdateView, ExhibitDeleteView,
    ProfileView, edit_profile
)

app_name = 'museum'

urlpatterns = [
    path(
        'floor/<int:floor_level>/',
        FloorListView.as_view(),
        name='floor'
    ),
    path(
        'exposition/<int:exposition_pk>/',
        ExpositionListView.as_view(),
        name='exposition'
    ),
    path(
        'exposition/create/',
        ExpositionCreationView.as_view(),
        name='exposition_create'
    ),
    path(
        'exposition/update/<int:exposition_pk>/',
        ExpositionUpdateView.as_view(),
        name='exposition_update'
    ),
    path(
        'exposition/delete/<int:exposition_pk>/',
        ExpositionDeleteView.as_view(),
        name='exposition_delete'
    ),
    path(
        'exhibit/<int:exhibit_pk>/',
        ExhibitView.as_view(),
        name='exhibit'
    ),
    path(
        'exhibit/create/',
        ExhibitCreationView.as_view(),
        name='exhibit_create'
    ),
    path(
        'exhibit/update/<int:exhibit_pk>/',
        ExhibitUpdateView.as_view(),
        name='exhibit_update'
    ),
    path(
        'exhibit/delete/<int:exhibit_pk>/',
        ExhibitDeleteView.as_view(),
        name='exhibit_delete'
    ),
    path(
        'profile/edit/',
        edit_profile,
        name='edit_profile'
    ),
    path(
        'profile/<str:username>/',
        ProfileView.as_view(),
        name='profile'
    ),
]
