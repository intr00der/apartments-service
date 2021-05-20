from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name,
                    last_name, gender, born_at, country, city):
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            born_at=born_at,
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
