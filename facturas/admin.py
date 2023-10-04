from django.contrib import admin
from django.db import models
from .models import factura, codigoFinanciero
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets


admin.site.site_header = "Gestion Pilar"
admin.site.site_title = "Gestion Pilar"


@admin.register(codigoFinanciero)
class codigoFinancieroAdmin(ImportExportModelAdmin):
        list_display= ('codigo',)

#controlo como se importa/exporta
class facturaResource(resources.ModelResource):
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

enviar.short_description = "Enviar"

@admin.register(factura)
class facturaAdmin(ImportExportModelAdmin):
        resource_class = facturaResource
        actions = [enviar]

        #controlo los filtros segun el grupo
        def get_list_filter(self, request):
                user = request.user
                list_filter = ('nroFactura', 'proveedor',)

                if user.groups.filter(name="administracion").exists():
                         list_filter += ('codigo',) 

                exclude = ('codigo',)
                return list_filter

        #controlo lo que ve en el cuadro segun el grupo
        def get_list_display(self, request):
                user = request.user
                common_display = ['nroFactura', 'proveedor', 'total']
                
                if user.groups.filter(name="administracion").exists():
                        return ['codigo'] + common_display 
                
                return common_display
        

        #filtr el query por grupo
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
        
 