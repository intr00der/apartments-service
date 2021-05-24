from django.contrib.auth.base_user import BaseUserManager

from datetime import date

from apartments.models import Country, City

class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name,
                    gender, born_in, country, city, passport):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            born_in=born_in,
            country=country,
            city=city,
            passport=passport,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name,
                         gender, born_in, country, city, ):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            born_in=born_in,
            country=Country.objects.get(pk=country),
            city=City.objects.get(pk=city),
            is_staff=True,
            is_superuser=True
        )

        user.set_password(password)
        user.save(using=self._db)
