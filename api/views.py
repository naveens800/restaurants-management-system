from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .models import Restaurant, Recipe
from rest_framework import mixins
from rest_framework import generics
from django.http import Http404
from rest_framework import status


# ------------------------------------------------------------------------------------
class Restaurants(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    # retreve instances

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    # crete new instance

    def post(self, request):
        return self.create(request)
# ------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------
class RestaurantDetail(APIView):

    # retrive detail of a particular restaurant
    def get(self, request, restaurant_id):
        # try to retrive if there any
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        # if not raise exception
        except Restaurant.DoesNotExist:
            raise Http404
        # serialize the data before giving response
        serializer = serializers.RestaurantSerializer(restaurant)
        return Response(serializer.data)

    # Handles deletion of a particular restaurant
    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Http404

        restaurant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
class Recipes(APIView):

    # retrive recipe's from database
    def get(self, request, restaurant_id):
        recipes = Recipe.objects.filter(restaurant__id=restaurant_id)
        # serializes the data before giving response
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, restaurant_id):
        # Before creating a recipe try to get details ('id') of restaurant that belongs to
        try:
            Restaurant.objects.get(pk=restaurant_id)
        # If details not found raise an exception
        except Restaurant.DoesNotExist:
            raise Http404

        # If details exist serialize the request.data
        serializer = serializers.RecipeSerializer(data=request.data)
        # If serializer is valid save the recipe with corresponding restaurant id
        if serializer.is_valid():
            serializer.save(restaurant_id=restaurant_id,
                            ingredients=request.data.get("ingredients"))
            return Response(serializer.data, status=status.HTTP_200_OK)
        # If not valid give status of bad request with errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
class RecipeDetail(APIView):

    def get(self, request, restaurant_id, recipe_id):
        # Before getting the recipe we needs to get the restaurant__id.
        try:
            recipe = Recipe.objects.get(
                restaurant__id=restaurant_id, pk=recipe_id)
        # if details ("restaurant__id") not found raise an exception
        except Recipe.DoesNotExist:
            raise Http404
        # serialize the data before giving response
        serializer = serializers.RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Handles deletion of a particular restaurant
    def delete(self, request, restaurant_id, recipe_id):

        try:
            recipe = Recipe.objects.get(
                restaurant__id=restaurant_id, pk=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404

        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# --------------------------------------------------------------------------------------
