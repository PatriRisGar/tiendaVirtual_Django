from .models import User, Producto, Marca, Compra
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
  model = User
  fieldsets = UserAdmin.fieldsets + (
  (None, {'fields': ('vip','saldo',)}),
  )
#Con esto te saldra al crear un nuevo usuario desde admin los campos customizados
add_fieldsets = UserAdmin.add_fieldsets + (
(None, {'fields': ('vip','saldo',)}),
)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Producto)
admin.site.register(Marca)
admin.site.register(Compra)