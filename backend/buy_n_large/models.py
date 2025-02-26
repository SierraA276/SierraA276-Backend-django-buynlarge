from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)  # False = Usuario normal, True = Admin

    def __str__(self):
        return self.name

class Computador(models.Model):
    marca = models.CharField(max_length=100) #marca del pc (dell, asus, etc.)
    cpu = models.CharField(max_length=100) #procesador  
    ram = models.IntegerField() #la cantidad de ram en GB   
    gb = models.IntegerField() #el almacenamiento del pc en centenas
    precio = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.IntegerField() #cantidad de computadores
    gpu = models.CharField(max_length=100, blank=True, null=True) #Chip tarjeta grafica integrada

    def __str__(self):
        return self.brand
