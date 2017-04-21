from django.contrib import admin
from .models import testSchema
import schemas.models_dir.thd as thd

admin.site.register(testSchema)

#  -----------------------   THD   ---------------------------------
# Outgoing Archive

admin.site.register(thd.thdSales)
admin.site.register(thd.thdReceipts)
admin.site.register(thd.thdMargin)
admin.site.register(thd.thdInv)
admin.site.register(thd.thdApsw)

# Incoming Archive

admin.site.register(thd.thdAUTH)
admin.site.register(thd.thdCATM)
admin.site.register(thd.thdCATR)
admin.site.register(thd.thdCLST)
admin.site.register(thd.thdLOCH)
admin.site.register(thd.thdPGAD)
admin.site.register(thd.thdPGHD)
admin.site.register(thd.thdPGSR)
admin.site.register(thd.thdPRDH)
admin.site.register(thd.thdPSPC)
admin.site.register(thd.thdPSSD)
admin.site.register(thd.thdSKUA)
admin.site.register(thd.thdSKUM)
admin.site.register(thd.thdSTRM)
admin.site.register(thd.thdSTRT)
admin.site.register(thd.thdUDSG)
admin.site.register(thd.thdUDSV)