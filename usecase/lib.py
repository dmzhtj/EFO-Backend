from usecase.operations import *
def modify(collections,operation,container):
    for ref in collections:
        obj = container.get_element_by_ref(ref)
        if isinstance(operation,Add):
            setattr(obj,operation.field,getattr(obj,operation.field) + operation.data)
        elif isinstance(operation,Set):
            setattr(obj,operation.field,operation.data)
        elif isinstance(operation,Apply):     ######### DO NOT EXPOSE! ######### Caution lambda injection.
            setattr(obj,operation.field,operation.data(getattr(obj,operation.field)))
        container.register(obj)
    