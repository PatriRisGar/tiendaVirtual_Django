from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User (AbstractUser):
  username = models.CharField(max_length=10, unique=True)
  vip = models.BooleanField(default='False')
  saldo = models.DecimalField(max_digits=5, decimal_places=2,null= True, blank= True)

  def __str__(self):
    return self.username
  
class Marca (models.Model):
  nombre = models.CharField(max_length=10)

  def __str__(self):
    return self.nombre

class Producto (models.Model):
  nombre = models.CharField(max_length=10)
  modelo = models.CharField(max_length=10)
  marca = models.ForeignKey('Marca', on_delete=models.PROTECT)
  unidades = models.PositiveIntegerField()
  precio = models.DecimalField(max_digits=5, decimal_places=2)
  vip = models.BooleanField()

  def __str__(self):
    return self.nombre
  
  class Meta:
    unique_together = ['marca','modelo']


class Compra (models.Model):
  fecha = models.DateTimeField()
  user = models.ForeignKey('User',on_delete=models.PROTECT)
  producto = models.ForeignKey('Producto',on_delete=models.PROTECT)
  unidades = models.PositiveIntegerField()
  importe = models.DecimalField(max_digits=5, decimal_places=2)
  iva = models.DecimalField(max_digits=5, decimal_places=2, default=0.21)

  def __str__(self):
    return f'{self.user.username}'

  class Meta:
    unique_together = ['fecha','user','producto']
