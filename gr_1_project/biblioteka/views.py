from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Osoba, Stanowisko
from .serializers import BookSerializer, OsobaSerializer, StanowiskoSerializer

# określamy dostępne metody żądania dla tego endpointu
@api_view(['GET', "POST"])
def book_list(request):
    """
    Lista wszystkich obiektów modelu Book.
    """
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):

    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Book
    :return: Response (with status and/or object/s data)
    """
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Zwraca pojedynczy obiekt typu Book.
    """
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET","POST","DELETE"])
def osoba_detail(request, pk):
    try:
        osoba = Osoba.objects.get(pk=pk)
    except Osoba.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = OsobaSerializer(osoba)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = OsobaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        osoba.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def osoba_list(request):
    if request.method == "GET":
        return Response(OsobaSerializer(Osoba.objects.all(),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        
@api_view(["GET"])
def osoba_name_filter_url(request, name):
    if request.method == "GET":
        return Response(OsobaSerializer(Osoba.objects.filter(nazwisko__icontains = name),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        
@api_view(["GET"])
def osoba_name_filter_params(request):
    if request.method == "GET":
        # Pobranie parametru 'name' z query params
        name = request.query_params.get('name', None)
        if name is not None:
            return Response(OsobaSerializer(Osoba.objects.filter(nazwisko__icontains = name),
                                            many = True).data,
                            status = status.HTTP_200_OK)
        else:
            return Response({"error": "Parametr 'name' jest wymagany."}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET","POST","DELETE"])
def stanowisko_detail(request, pk):
    try:
        stanowisko = Stanowisko.objects.get(pk=pk)
    except Stanowisko.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StanowiskoSerializer(stanowisko)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StanowiskoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        stanowisko.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(["GET"])
def stanowisko_list(request):
    if request.method == "GET":
        return Response(StanowiskoSerializer(Stanowisko.objects.all(),
                                        many = True).data,
                        status = status.HTTP_200_OK)
        


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

class BookListView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# # 1. Wyświetlanie, dodawanie i usuwanie pojedynczego obiektu Osoba
# class OsobaDetailAPIView(RetrieveDestroyAPIView, CreateAPIView):
#     queryset = Osoba.objects.all()
#     serializer_class = OsobaSerializer

# # 2. Wyświetlanie listy wszystkich obiektów Osoba
# class OsobaListAPIView(ListAPIView):
#     queryset = Osoba.objects.all()
#     serializer_class = OsobaSerializer

# # 3. Wyświetlanie listy osób po fragmencie nazwiska
# class OsobaSearchAPIView(ListAPIView):
#     serializer_class = OsobaSerializer

#     def get_queryset(self):
#         # Pobieramy parametr 'name' z URL
#         name = self.kwargs.get('name', None)
#         if name:
#             return Osoba.objects.filter(nazwisko__icontains=name)
#         return Osoba.objects.none()  # jeśli brak parametru, zwracamy pusty queryset
    
# class OsobaNameFilterView(APIView):
#     # #Prostsza wersja ale wtedy wpisujemy po ?search= zamiast ?name=
#     # queryset = Osoba.objects.all()
#     # serializer_class = OsobaSerializer
#     # filter_backends = [SearchFilter]
#     # search_fields = ['nazwisko']
#     def get(self, request):
#         # Pobranie parametru 'name' z query params
#         name = request.query_params.get('name', None)

#         if name:
#             osoby = Osoba.objects.filter(nazwisko__icontains=name)
#             serializer = OsobaSerializer(osoby, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Parametr 'name' jest wymagany."}, status=status.HTTP_400_BAD_REQUEST)

# # 4. Wyświetlanie, dodawanie i usuwanie pojedynczego obiektu Stanowisko
# class StanowiskoDetailAPIView(RetrieveDestroyAPIView, CreateAPIView):
#     queryset = Stanowisko.objects.all()
#     serializer_class = StanowiskoSerializer

# # 5. Wyświetlanie listy wszystkich obiektów Stanowisko
# class StanowiskoListAPIView(ListAPIView):
#     queryset = Stanowisko.objects.all()
#     serializer_class = StanowiskoSerializer


from django.http import HttpResponse
import datetime


def welcome_view(request):
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)

def osoba_list_html(request):
    # pobieramy wszystkie obiekty Osoba z bazy poprzez QuerySet
    osoby = Osoba.objects.all()
    #return HttpResponse(osoby)
    return render(request,
                  "biblioteka/osoba/list.html",
                  {'osoby': osoby})