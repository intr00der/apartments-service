from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name,
                    gender, birthday, country, city, passport):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birthday=birthday,
            country_id=country.id,
            city_id=city.id,
            passport=passport,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name,
                         gender, birthday, country, city):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birthday=birthday,
            country_id=city.id,
            city_id=country.id,
            is_verified=True,
            is_staff=True,
            is_superuser=True
        )

        user.set_password(password)
        user.save(using=self._db)
