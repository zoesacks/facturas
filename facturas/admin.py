from django.contrib import admin
from .models import factura, codigoFinanciero
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets


admin.site.site_header = "Gestion Pilar"
admin.site.site_title = "Gestion Pilar"


@admin.register(codigoFinanciero)
class codigoFinancieroAdmin(ImportExportModelAdmin):
        list_display= ('codigo',)


class FacturaResource(resources.ModelResource):
        emision = fields.Field(attribute='emision',  column_name='emision')
        alta = fields.Field(attribute='alta', column_name='alta')
        codigo = fields.Field(attribute='codigo', column_name='codigo', widget=widgets.ForeignKeyWidget(codigoFinanciero, 'codigo')) # Acceso al campo 'codigo' en codigoFinanciero
        nroFactura = fields.Field(attribute='nroFactura', column_name='nroFactura')
        proveedor = fields.Field(attribute='proveedor', column_name='proveedor')
        oc = fields.Field(attribute='oc', column_name='oc')
        total = fields.Field(attribute='total', column_name='total')
        ff = fields.Field(attribute='ff', column_name='ff')
        unidadEjecutora = fields.Field(attribute='unidadEjecutora', column_name='unidadEjecutora')
        objeto = fields.Field(attribute='objeto', column_name='objeto')
        fondoAfectado = fields.Field(attribute='fondoAfectado', column_name='fondoAfectado')

        class Meta:
                model = factura

def enviar(modeladmin, request, queryset):
    queryset.update(estado='enviado')

enviar.short_description = "Marcar seleccionadas como Enviadas"

@admin.register(factura)
class facturaAdmin(ImportExportModelAdmin):
        resource_class = FacturaResource
        list_display=('codigo','estado', 'emision', 'nroFactura', 'proveedor', 'total', 'objeto')
        list_filter = ('nroFactura', 'proveedor',)
        actions = [enviar]

        #filtrar por tipo de usuario
        def get_queryset(self, request):
                user = request.user
                queryset = super().get_queryset(request)

                #los de admin solo pueden ver lo enviado
                if user.groups.filter(name="administracion").exists():
                        queryset = queryset.filter(estado='enviado')

                else:
                        user_group_name = user.groups.first().name if user.groups.exists() else None

                        #los demas lo que esta para enviar
                        if user_group_name:
                                queryset = queryset.filter(codigo__codigo=user_group_name, estado = 'enviar')

                return queryset
 