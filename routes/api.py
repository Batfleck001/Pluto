from config import supabase
from fastapi import requests, APIRouter
from datetime import datetime, timezone
from infrastructure.models.models import (
    newItem,
    updatePurchase,
    deleteCategory,
    deleteItem,
    request_bodyMetrics,
    response_bodyMetrics,
    create_user_request
)

router = APIRouter()

@router.get("/")
def home():
    return {"message" : "inventory"}

@router.get("/all")
def all():
    res = (supabase.table("categories")
           .select("name, items(id, name, in_stock, quantity, unit))")
           .order("name")
           .execute()
    )

    return res.data

#====================== New category and Item creation ========================

@router.post("/new_item")
def new_item(item : newItem):
    category = (supabase.table("categories")
        .select("*")
        .eq("name",item.category.capitalize())
        .execute()
        )
    print("**************************************")
    print(category.data)
    if len(category.data) == 0:

        newCategory = (supabase.table("categories")
        .insert({"name": item.category.capitalize()})
        .select()
        .execute()
        )

        items_info = (supabase.table("items")
                    .insert({
                        "category_id" : newCategory.data[0]["id"],
                        "name" : item.item.capitalize(),
                        "in_stock" : "true" if item.quantity > 0 else "false",
                        "quantity" : item.quantity,
                        "unit":item.unit.capitalize()
                        })
                    .select()
                    .execute())
        
        
        res = (supabase.table("categories")
            .select("id","name","items(id, name, in_stock, quantity, unit)")
            .execute()
        )

        return res.data

    else:
        items_info = (supabase.table("items")
            .insert({
                "category_id" : category.data[0]["id"],
                "name" : item.item.capitalize(),
                "in_stock" : "true" if item.quantity > 0 else "false",
                "quantity" : item.quantity,
                "unit":item.unit.capitalize()
                })
            .select()
            .execute())

        res = (supabase.table("categories")
            .select("id","name","items(id, name, in_stock, quantity, unit))")
            .eq("name",item.category.capitalize())
            .execute()
        )

        return res.data

@router.post("/create_user")
def create_user(request: create_user_request):
    data = (
            supabase.table("users")
            .insert({
                "username": request.username
                })
            .execute()
        )
    return data.data



@router.post("/body_metrics", response_model=response_bodyMetrics)
def body_metrics(request: request_bodyMetrics):

    BMI = request.weight / pow((request.height / 100), 2)
    BMI = round(BMI, 2)

    if request.gender.lower() == "male":
        BMR = (10 * request.weight) + (6.25 * request.height) - (5 * request.age) + 5
    else:
        BMR = (10 * request.weight) + (6.25 * request.height) - (5 * request.age) - 161

    BMR = round(BMR, 2)

    if request.exercise_per_week == 0:
        exercise = 1.2
    elif 1 <= request.exercise_per_week < 3:
        exercise = 1.375
    elif 3 <= request.exercise_per_week <= 5:
        exercise = 1.55
    elif request.exercise_per_week == 6:
        exercise = 1.725
    else:
        exercise = 1.9

    TDEE = round(BMR * exercise, 2)

    response = response_bodyMetrics(
        user=request.user,
        age=request.age,
        height=request.height,
        weight=request.weight,
        gender=request.gender,
        BMI=BMI,
        BMR=BMR,
        TDEE=TDEE
    )

    data = (
        supabase.table("body_metrics")
        .insert(response.model_dump())
        .execute()
    )

    return response

#====================== update purchase ============================================

# @router.post("/update_purchase")
# def update_purchase(purchase: updatePurchase):
#     item = (supabase.table("items")
#         .select("*")
#         .eq("name",purchase.item.capitalize())
#         .execute()
#         )

#     now = datetime.now(timezone.utc)
#     isoformat = now.isoformat()

#     if len(item.data) > 0:
#         new_purchase_info = (supabase.table("purchases")
#             .update({
#                 "quantity" : purchase.quantity,
#                 "unit" : purchase.unit.capitalize(),
#                 "purchased_at" : isoformat
#                 })
#             .eq("item_id", item.data[0]["id"])
#             .execute()
#         )
    
#     return new_purchase_info.data


# ==================== delete apis =============================


@router.delete("/delete_category")
def delete_category(categories : deleteCategory):
    res = (supabase.table("categories")
        .delete()
        .eq("name",categories.category.capitalize())
        .execute()
        ) , 200

    if res :
        return res[0]
    else :
        return {"error" : "not found"}

@router.delete("/delete_item")
def delete_item(items : deleteItem):
    res = (supabase.table("items")
        .delete()
        .eq("name",items.item.capitalize())
        .execute()
        ) , 200
    if res :
        return res[0]
    else :
        return {"error" : "Some error"}
