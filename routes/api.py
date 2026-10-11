from infrastructure.supabase.supabase import supabase
from fastapi import requests, APIRouter
from datetime import datetime, timezone
from infrastructure.models.models import (
    newItem,
    updatePurchase,
    deleteCategory,
    deleteItem
)

router = APIRouter()

@router.get("/")
def home():
    return {"mesage" : "inventory"}

@router.get("/all")
def all():
    res = (supabase.table("categories")
           .select("name, items(id, name, in_stock, purchases(id, quantity, unit, purchased_at))")
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
                        })
                    .select()
                    .execute())
        
        purchases = (supabase.table("purchases")
                    .insert({
                        "item_id" : items_info.data[0]["id"],
                        "quantity" : item.quantity,
                        "unit":item.unit.capitalize()
            })
            .select()
            .execute()
            )
        
        res = (supabase.table("categories")
            .select("id","name","items(id, name, in_stock, purchases(id, quantity, unit, purchased_at))")
            .execute()
        )

        return res.data

    else:
        items_info = (supabase.table("items")
            .insert({
                "category_id" : category.data[0]["id"],
                "name" : item.item.capitalize(),
                "in_stock" : "true" if item.quantity > 0 else "false",
                })
            .select()
            .execute())

        purchases = (supabase.table("purchases")
            .insert({
                "item_id" : items_info.data[0]["id"],
                "quantity" : item.quantity,
                "unit":item.unit.capitalize()
            })
            .select()
            .execute()
            )

        res = (supabase.table("categories")
            .select("id","name","items(id, name, in_stock, purchases(id, quantity, unit, purchased_at))")
            .eq("name",item.category.capitalize())
            .execute()
        )

        return res.data


#====================== update purchase ============================================

@router.post("/update_purchase")
def update_purchase(purchase: updatePurchase):
    item = (supabase.table("items")
        .select("*")
        .eq("name",purchase.item.capitalize())
        .execute()
        )

    now = datetime.now(timezone.utc)
    isoformat = now.isoformat()

    if len(item.data) > 0:
        new_purchase_info = (supabase.table("purchases")
            .update({
                "quantity" : purchase.quantity,
                "unit" : purchase.unit.capitalize(),
                "purchased_at" : isoformat
                })
            .eq("item_id", item.data[0]["id"])
            .execute()
        )
    
    return new_purchase_info.data


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
