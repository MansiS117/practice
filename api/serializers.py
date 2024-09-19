from rest_framework import serializers

from store.models import Book, Category, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "user_type",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Passwords must match."}
            )
        return attrs

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number", ""),
            address=validated_data.get("address", ""),
            user_type=validated_data.get("user_type", "buyer"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class BookSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Book
        fields = [
            "title",
            "category",
            "seller",
            "author",
            "price",
            "description",
        ]
