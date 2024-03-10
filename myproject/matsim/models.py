from django.db import models

# Create your models here.


class Chemical(models.Model):
    mat_id = models.CharField(max_length=20)
    smiles = models.CharField(max_length=100)
    inchi = models.CharField(max_length=200)
    formula = models.CharField(max_length=50)
    charge = models.IntegerField()
    num_of_heavyatom = models.IntegerField()
    HOMO = models.FloatField()
    LUMO = models.FloatField()
    GAP = models.FloatField()
    molecular_mass = models.FloatField()
    multiplicity = models.IntegerField()

    # Atoms coordinates
    # JSONField를 사용하여 atoms_coord를 딕셔너리 형태로 저장
    atoms_coord = models.JSONField()

    @classmethod
    def from_json(cls, json_data):
        atoms_coord = json_data.pop("atoms_coord", {})
        return cls.objects.create(atoms_coord=atoms_coord, **json_data)
