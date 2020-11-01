from sqlalchemy.orm import Session

def get_or_create(db: Session, model, **kwargs):
    """Returns an item from the model, matching args specified in kwargs.
    If it does not exists, creates a new one
    """
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        return instance

def get_filter_by_args(model, dic_args: dict):
    """Get list of SQLAlchemy filters from dictionary of arguments.
    """
    filters = []
    for key, value in dic_args.items():  # type: str, any
        if key.endswith('__lte'):
            key = key.replace('__lte', '')
            filters.append(getattr(model, key) <= value)
        elif key.endswith('__lt'):
            key = key.replace('__lt', '')
            filters.append(getattr(model, key) < value)
        elif key.endswith('__gte'):
            key = key.replace('__gte', '')
            filters.append(getattr(model, key) >= value)
        elif key.endswith('__gt'):
            key = key.replace('__gt', '')
            filters.append(getattr(model, key) > value)
        elif key.endswith('__ne'):
            key = key.replace('__ne', '')
            filters.append(getattr(model, key) != value)
        elif key.endswith('__eq'):
            key = key.replace('__eq', '')
            filters.append(getattr(model, key) == value)
        else:
            filters.append(getattr(model, key).ilike("%{}%".format(value)))
    return filters

def get_sorter_by_args(model, args: list):
    """Get list of SQLAlchemy order_by args from dictionary of arguments.
    """
    sorters = []
    for key in args:
        if key[0] == '-':
            sorters.append(getattr(model, key[1:]).desc())
        else:
            sorters.append(getattr(model, key))
    return sorters
