from django.test import TestCase
from django.contrib.auth.models import User

from core_app.models import Region, City, Commune, Address, Country
from .models import BusinessEntity


class BusinessEntityTestCase(TestCase):
    def test_business_entity(self):
        country = Country.objects.create(english_name="D.R. Congo",
                                        french_name="R.D. Congo",
                                        local_name="R.D. Congo",
                                        region="Central Africa",
                                        continent="Africa") 
        province = Region.objects.create(name="Kinshasa",
                                        country=country,
                                        is_active=True)
        city = City.objects.create(name="Funa District",
                                    region=province,
                                    country=country,
                                    city_type="District",
                                    is_active=True)
        commune = Commune.objects.create(name="Selembao",
                                        city=city,
                                        is_active=True)
        
        address = Address.objects.create(region=province,
                            city=city,
                            commune=commune,
                            street="14 Avenue du Commerce")
        user = User.objects.create(first_name="firstnameTest",
                                last_name="lastnameTest",
                                email="emailTest@gmail.com",
                                password="PasswordTest_1")

        self.assertEquals(
            BusinessEntity.objects.count(),
            0
        )
        BusinessEntity.objects.create(
            account_admin=user,
            address=address,
            business_name="businessNameTest",
            identification_number="idN_001",
            email="busEmailTest@gmail.com",
            phone_number="+0019785529846"
        )
        self.assertEquals(
            BusinessEntity.objects.count(),
            1
        )
