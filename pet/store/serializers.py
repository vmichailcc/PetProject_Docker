from rest_framework import serializers

from store.models import Product, ProductComment, Order, Pictures


class StoreSerializer(serializers.ModelSerializer):
    comments = serializers.IntegerField()

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "brand",
            "main_picture",
            'comments',
            "like",
        ]
        read_only_fields = [
            "name",
            "brand",
            "main_picture",
        ]

    def get_comments(self, obj):
        return len(obj.comments)


class PicturesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pictures
        fields = ["pictures"]
        # read_only_fields = ["pictures"]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductComment
        fields = [
            "text",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    pictures = PicturesSerializer(many=True, read_only=True)
    text_product = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField()

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "brand",
            "main_picture",
            "pictures",
            "comments_count",
            "text_product",
            "like",
        ]
        read_only_fields = [
            "name",
            "description",
            "brand",
            "main_picture",
            "pictures",
            "comments_count",
            "text_product",
            "like",
        ]

    def get_comments_count(self, obj):
        return len(obj.comments_count)


class ProductCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductComment
        fields = [
            "text_product",
            "text_author",
            "text",
            "text_created_at",
        ]
        read_only_fields = ["text_author", "text_created_at"]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "product",
            "quantity",
            "owner_comment",
            "status",
        ]
        read_only_fields = ["status"]


class OrderDetailSerializer(serializers.ModelSerializer):
    product = serializers.CharField()

    class Meta:
        model = Order
        fields = [
            "product",
            "quantity",
            "status",
            "owner_comment",
            "admin_comment"
        ]
        read_only_fields = [
            "product",
            "quantity",
            "status",
            "owner_comment",
            "admin_comment"
        ]
