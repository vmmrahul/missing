"""missingPerson URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AdminView import *
import userView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('loginPage', login, name='loginPage'),
    path('dashboard', dashboard, name='dashboard'),
    path('signout', signout, name='signout'),
    path('changePassword', changePassword, name='changePassword'),
    path('changePassword', changePassword, name='changePassword'),

    # Area work Start
    path('addArea', addArea, name='addArea'),
    path('viewArea', viewArea, name='viewArea'),
    path('deleteArea', deleteArea, name='deleteArea'),
    # Area work ends

    # Add Story
    path('addStroy', addStroy, name='addStroy'),
    path('viewStory', viewStory, name='viewStory'),

    # end of story work

    #     user work start
    path('signup', userView.signupPage, name='signup-Page'),
    path('userlogin', userView.userlogin, name='userlogin'),
    path('userlogout', userView.userlogout, name='userlogout'),
    path('', userView.home, name='home'),
    path('createPost', userView.createPost, name='createPost'),
    path('deletePost', userView.deletePost, name='deletePost'),
    path('userProfile', userView.userProfile, name='userProfile'),
    path('validateImages', userView.validateImages, name='validateImages'),
    path('updatePostStatus', userView.updatePostStatus, name='updatePostStatus'),
    path('topStoryFound', userView.topStoryFound, name='topStoryFound'),
    path('searchMissingPerson', userView.searchMissingPerson, name='searchMissingPerson'),
    path('searchResultAction', userView.searchResultAction, name='searchResultAction'),
]
