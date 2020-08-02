from django.db import models
from baseapps.core.models import User

class Employee(models.Model):
    PRIA = 'laki-laki'
    WANITA= 'perempuan'
    jk = (
        (PRIA,'laki-laki'),
        (WANITA,'perempuan')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    no_ktp = models.CharField(max_length=50, null=True,blank=True)
    jenis_kelamin = models.CharField(max_length=50, null=True,blank=True, choices=jk)
    no_bpjs =models.CharField(max_length=50, null=True,blank=True)
    status = models.CharField(max_length=150, null=True,blank=True)
    masa_kontrak =models.IntegerField(default=0, null=True,blank=True)
    tanggal_mulai_kontrak = models.DateField(null=True,blank=True)


    def __str__(self):
        return self.user.nama