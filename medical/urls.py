from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from inventory.views import *

static_urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', updateInventory),
    path('billing', billing),
    path('getComposition', getComposition),
    path('findAlternative', findAlternative),
    path('findMedicine', findMedicine),
    path("api/medicine/<str:name>", getprice),
    path("api/bill",generateBill),
    path('bill/<str:name>', fetchBill),
    path("analyse",analysis),
    path('inventory',StockItems),
    path("checkQuantity",checkQuantity),
    path("setup",setup),
    path('',include("authentication.urls")),
    path('oldstock',oldInventory),
    path('backup',backupdb),
    path('findMedicineByComposition',findMedicineByComposition),
    path('findMedicineByName',findMedicineByName),
]
