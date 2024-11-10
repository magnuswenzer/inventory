from fastapi import FastAPI, HTTPException, Query, Depends
from inventory.models import Category, CategoryCreate, CategoryPublic, CategoryUpdate
from inventory.models import Item, ItemCreate, ItemPublic, ItemUpdate
from inventory.models import ItemType, ItemTypeCreate, ItemTypePublic, ItemTypeUpdate
from inventory.models import ItemTypePublicWithRelations, ItemPublicWithRelations, UnitPublicWithRelations, \
    CategoryPublicWithRelations, LocationPublicWithRelations
from inventory.models import Location, LocationCreate, LocationPublic, LocationUpdate
from inventory.models import Unit, UnitCreate, UnitPublic, UnitUpdate
from inventory.models import create_db_and_tables, engine
from sqlmodel import Session, select

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


# @app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        create_db_and_tables()
        cat1 = Category(name='Frysta grönsaker')
        cat2 = Category(name='Fryst kött')
        session.add(cat1)
        session.add(cat2)
        session.commit()
        session.refresh(cat1)
        session.refresh(cat2)


@app.post("/category/", response_model=CategoryPublic)
def create_category(*, session: Session = Depends(get_session), category: CategoryCreate):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.get("/category/", response_model=list[CategoryPublic])
def read_categories(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    category = session.exec(select(Category).offset(offset).limit(limit)).all()
    return category


@app.get("/category/{category_id}", response_model=CategoryPublicWithRelations)
def read_category(*, session: Session = Depends(get_session), category_id: int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.patch("/category/{category_id}", response_model=CategoryPublic)
def update_category(*, session: Session = Depends(get_session), category_id: int, category: CategoryUpdate):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.delete("/category/{category_id}")
def delete_category(*, session: Session = Depends(get_session), category_id: int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}

####
@app.post("/itemtype/", response_model=ItemTypePublic)
def create_itemtype(*, session: Session = Depends(get_session), itemtype: ItemTypeCreate):
    db_itemtype = ItemType.model_validate(itemtype)
    session.add(db_itemtype)
    session.commit()
    session.refresh(db_itemtype)
    return db_itemtype


@app.get("/itemtype/", response_model=list[ItemTypePublic])
def read_itemtypes(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    itemtype = session.exec(select(ItemType).offset(offset).limit(limit)).all()
    return itemtype


@app.get("/itemtype/{itemtype_id}", response_model=ItemTypePublicWithRelations)
def read_itemtype(*, session: Session = Depends(get_session), itemtype_id: int):
    itemtype = session.get(ItemType, itemtype_id)
    if not itemtype:
        raise HTTPException(status_code=404, detail="ItemType not found")
    return itemtype


@app.patch("/itemtype/{itemtype_id}", response_model=ItemTypePublic)
def update_itemtype(*, session: Session = Depends(get_session), itemtype_id: int, itemtype: ItemTypeUpdate):
    db_itemtype = session.get(ItemType, itemtype_id)
    if not db_itemtype:
        raise HTTPException(status_code=404, detail="ItemType not found")
    itemtype_data = itemtype.model_dump(exclude_unset=True)
    db_itemtype.sqlmodel_update(itemtype_data)
    session.add(db_itemtype)
    session.commit()
    session.refresh(db_itemtype)
    return db_itemtype


@app.delete("/itemtype/{itemtype_id}")
def delete_itemtype(*, session: Session = Depends(get_session), itemtype_id: int):
    itemtype = session.get(ItemType, itemtype_id)
    if not itemtype:
        raise HTTPException(status_code=404, detail="ItemType not found")
    session.delete(itemtype)
    session.commit()
    return {"ok": True}


####
@app.post("/item/", response_model=ItemPublic)
def create_item(*, session: Session = Depends(get_session), item: ItemCreate):
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.get("/item/", response_model=list[ItemPublic])
def read_items(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    item = session.exec(select(Item).offset(offset).limit(limit)).all()
    return item


@app.get("/item/{item_id}", response_model=ItemPublicWithRelations)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.patch("/item/{item_id}", response_model=ItemPublic)
def update_item(*, session: Session = Depends(get_session), item_id: int, item: ItemUpdate):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.delete("/item/{item_id}")
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}


####
@app.post("/location/", response_model=LocationPublic)
def create_location(*, session: Session = Depends(get_session), location: LocationCreate):
    db_location = Location.model_validate(location)
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location


@app.get("/location/", response_model=list[LocationPublic])
def read_locations(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    location = session.exec(select(Location).offset(offset).limit(limit)).all()
    return location


@app.get("/location/{location_id}", response_model=LocationPublicWithRelations)
def read_location(*, session: Session = Depends(get_session), location_id: int):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@app.patch("/location/{location_id}", response_model=LocationPublic)
def update_location(*, session: Session = Depends(get_session), location_id: int, location: LocationUpdate):
    db_location = session.get(Location, location_id)
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    location_data = location.model_dump(exclude_unset=True)
    db_location.sqlmodel_update(location_data)
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    return db_location


@app.delete("/location/{location_id}")
def delete_location(*, session: Session = Depends(get_session), location_id: int):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    session.delete(location)
    session.commit()
    return {"ok": True}


####
@app.post("/unit/", response_model=UnitPublic)
def create_unit(*, session: Session = Depends(get_session), unit: UnitCreate):
    db_unit = Unit.model_validate(unit)
    session.add(db_unit)
    session.commit()
    session.refresh(db_unit)
    return db_unit


@app.get("/unit/", response_model=list[UnitPublic])
def read_units(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    unit = session.exec(select(Unit).offset(offset).limit(limit)).all()
    return unit


@app.get("/unit/{unit_id}", response_model=UnitPublicWithRelations)
def read_unit(*, session: Session = Depends(get_session), unit_id: int):
    unit = session.get(Unit, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@app.patch("/unit/{unit_id}", response_model=UnitPublic)
def update_unit(*, session: Session = Depends(get_session), unit_id: int, unit: UnitUpdate):
    db_unit = session.get(Unit, unit_id)
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    unit_data = unit.model_dump(exclude_unset=True)
    db_unit.sqlmodel_update(unit_data)
    session.add(db_unit)
    session.commit()
    session.refresh(db_unit)
    return db_unit


@app.delete("/unit/{unit_id}")
def delete_unit(*, session: Session = Depends(get_session), unit_id: int):
    unit = session.get(Unit, unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    session.delete(unit)
    session.commit()
    return {"ok": True}