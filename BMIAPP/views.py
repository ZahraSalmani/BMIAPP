from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from BMI.permissions import IsOwener

from BMIAPP.models import BMI_History, User
from .serializers import BMISerializer, ReadBMISerializer, UserSerializer
from rest_framework import viewsets, permissions

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BMIViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BMI_History.objects.all()
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        method = self.request.method
        if  method not in permissions.SAFE_METHODS:
            return BMISerializer
        else:
            return ReadBMISerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)

        weight = request.data["weight"]
        height = request.data["height"]

        BMI = weight / (height / 100) ** 2
        BMI_Category = "دچار کمبود وزن"

        if BMI >= 18.5 and BMI <= 24.9:
            BMI_Category = "سالم"
        elif BMI > 24.9 and BMI <= 29.9:
            BMI_Category = "دارای اضافه وزن"
        elif BMI > 29.9:
            BMI_Category = "چاق"

        result = (
            "شاخص توده بدنی: {}".format(str(BMI))
            + "و"
            + " وضعیت وزن: {}".format(BMI_Category)
            + " می باشد . "
        )
        return Response({"result": result}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def create_user(request):
    user_ser = UserSerializer(data=request.data)
    if user_ser.is_valid():
        user_ser.save()
        return Response(user_ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsOwener])
def profile(request):
    try:
        user = User.objects.get(username=request.query_params["username"])

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    bmi_history = BMI_History.objects.filter(user=user)
    ser_bmi_history = BMISerializer(data=bmi_history, many=True)
    if ser_bmi_history.is_valid():
        return Response(ser_bmi_history.data, status=status.HTTP_200_OK)
    else:
        return Response(ser_bmi_history.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def fall_precategory(request):
    try:
        weight = float(request.query_params["weight"])
        height = float(request.query_params["height"])

    except:
        return Response("اطلاعات نامعتبراند.", status=status.HTTP_400_BAD_REQUEST)
    else:
        BMI = weight / (height / 100) ** 2
        ranges = [29.9,24.9,18.49]
        if BMI <= ranges[2]:
            return Response(
                "شاخص توده بدنی شما در پایین ترین حد قرار دارد.",
                status=status.HTTP_200_OK,
            )

        index = next(x for x, val in enumerate(ranges) if val <= BMI)
        result = round(ranges[index] * (height / 100) ** 2 - weight, 2)
        return Response(str(-result) + " kg", status.HTTP_200_OK)
