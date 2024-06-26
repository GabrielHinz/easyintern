from rest_framework import serializers

from users.models import UserCustom


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserCustom
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "ra",
            "student_class",
            "student_internship",
            "address",
            "contact",
            "extra_contact",
            "type",
            "company_sector",
            "company_cnpj",
        ]

    def create(self, validated_data):
        user = UserCustom.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            ra=validated_data.get("ra", ""),
            student_class=validated_data.get("student_class", ""),
            student_internship=validated_data.get("student_internship", ""),
            address=validated_data.get("address", ""),
            contact=validated_data.get("contact", ""),
            extra_contact=validated_data.get("extra_contact", ""),
            type=validated_data.get("type", ""),
            company_sector=validated_data.get("company_sector", ""),
            company_cnpj=validated_data.get("company_cnpj", ""),
        )
        return user
