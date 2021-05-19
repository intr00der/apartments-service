from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def validate_geo_data(self, country, region, city):
        if not country or not city:
            raise ValueError('This field is required.')
        return True

    def create_user(self, email, password, first_name,
                    last_name, gender, country, region, city):
        if self.validate_geo_data(self, country=country, city=city):
            user = self.model(
                email=self.normalize_email(email),
                password=password,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                country=country,
                city=city
            )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, password, first_name,
                         last_name, gender):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            is_staff=True,
            is_superuser=True
        )

        user.set_password(password)
        user.save(using=self._db)
