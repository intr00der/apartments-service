from django.contrib.auth.base_user import BaseUserManager


class ApartmentServiceUserManager(BaseUserManager):
    #
    # def serialize_user_data(
    #         self, email, password, first_name,
    #         last_name, gender, country, city
    # ):
    #     """
    #     тут я как-то пытался сделать метод сериализации,
    #     чтобы в методах ниже не повторять код, но пока не получилось
    #     """
    #     user = self.model(
    #         email=self.normalize_email(email),
    #         password=password,
    #         first_name=first_name,
    #         last_name=last_name,
    #         gender=gender,
    #         country=country,
    #         city=city
    #     )
    #     user.set_password(password)
    #     return user

    def create_user(
            self, email, password, first_name,
            last_name, gender, country, city
    ):
        # user = self.serialize_user_data(
        #     self, email=email, password=password,
        #     first_name=first_name, last_name=last_name,
        #     gender=gender, country=country, city=city
        # )

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

    def create_superuser(
            self, email, password, first_name,
            last_name, gender, country, city
    ):
        # user = self.serialize_user_data(
        #     self, email=email, password=password,
        #     first_name=first_name, last_name=last_name,
        #     gender=gender, country=country, city=city
        # )
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
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
