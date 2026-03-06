from typing import List

from fastapi import APIRouter

from esm_fullstack_challenge.models import AutoGenModels
from esm_fullstack_challenge.routers.utils import \
    get_route_list_function, get_route_id_function, \
    get_update_function, get_insert_function, get_delete_function


drivers_router = APIRouter()

table_model = AutoGenModels['drivers']

# Route to get driver by id
get_driver = get_route_id_function('drivers', table_model)
drivers_router.add_api_route(
    '/{id}', get_driver,
    methods=["GET"], response_model=table_model,
)

# Route to get a list of drivers
get_drivers = get_route_list_function('drivers', table_model)
drivers_router.add_api_route(
    '', get_drivers,
    methods=["GET"], response_model=List[table_model],
)

# new driver create route on POST
create_driver = get_insert_function('drivers', table_model)
drivers_router.add_api_route(
    '', create_driver,
    methods=["POST"], response_model=table_model
)

# new driver update route on PUT with id
update_driver = get_update_function('drivers', table_model)
drivers_router.add_api_route(
    '/{id}', update_driver,
    methods=["PUT"], response_model=table_model
)

# new driver delete route on DELETE with id
delete_driver = get_delete_function('drivers', table_model, get_driver)
drivers_router.add_api_route(
    '/{id}', delete_driver,
    methods=["DELETE"], response_model=table_model
)
