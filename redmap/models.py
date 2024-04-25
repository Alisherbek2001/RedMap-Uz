from django.db import models


CHOICES = (
    ("Hayvonlar", "Hayvonlar"),
    ("O'simliklar", "O'simliklar"),
)
REGIONS = [
    ["Xorazm", "Xorazm"],
    ["Andijon", "Andijon"],
    ["Surxondaryo", "Surxondaryo"],
    ["Buxoro", "Buxoro"],
    ["Toshkent", "Toshkent"],
    ["Navoiy", "Navoiy"],
    ["Fargona", "Farg'ona"],
    ["Nukus", "Nukus"],
    ["Jizzax", "Jizzax"],
    ["Qarshi", "Qarshi"],
    ["Namangan", "Namangan"],
    ["Samarqand", "Samarkand"],
    ["Sirdaryo", "Sirdaryo"]
]


class Oilasi(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Oilasi")
        verbose_name_plural = ("Oilalari")


class Hayvon(models.Model):
    oilasi = models.ForeignKey(Oilasi, on_delete=models.CASCADE)
    nomi = models.CharField(max_length=255)
    yili = models.IntegerField(default=2000)
    maqomi = models.TextField()
    tarqalishi = models.TextField()
    yashash_joylari = models.TextField()
    soni = models.TextField()
    yashash_tarzi = models.TextField()
    cheklovchi_omillar = models.TextField()
    kupaytirish = models.CharField(max_length=255)
    choralari = models.TextField()
    img = models.ImageField(upload_to="nature/", default="")

    class Meta:
        verbose_name = ("Hayvon")
        verbose_name_plural = ("Hayvonlar")

    def __str__(self):
        return self.nomi
    
class Osimlik(models.Model):
    oilasi = models.ForeignKey(Oilasi, on_delete=models.CASCADE)
    nomi = models.CharField(max_length=255)
    maqomi = models.TextField()
    tavsif = models.TextField()
    tarqalishi = models.TextField()
    sharoiti = models.TextField()
    soni = models.TextField()
    kupayishi = models.CharField(max_length=255)
    ozgarish_sabablari = models.TextField() 
    madaniylashtirish = models.TextField()
    muhofaza_choralari = models.TextField()
    img = models.ImageField(upload_to="nature/", default="")

    class Meta:
        verbose_name = ("O'simlik")
        verbose_name_plural = ("O'simliklar")

    def __str__(self):
        return self.nomi


class CoordinateHayvon(models.Model):
    nomi = models.ForeignKey(Hayvon, on_delete=models.CASCADE)
    region = models.CharField(max_length=20,choices=REGIONS)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)

    class Meta:
        verbose_name = ("Kordinata Hayvon")
        verbose_name_plural = ("Kordinatalar Hayvon")

    def __str__(self):
        return self.nomi.nomi

class CoordinateOsimlik(models.Model):
    nomi = models.ForeignKey(Osimlik, on_delete=models.CASCADE)
    region = models.CharField(max_length=20,choices=REGIONS)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)

    class Meta:
        verbose_name = ("Kordinata O'simlik")
        verbose_name_plural = ("Kordinatalar O'simliklar")

    def __str__(self):
        return self.nomi.nomi
