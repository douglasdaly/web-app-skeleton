# Web Application Backend API Skeleton

*The backend skeleton API for a modern web application.*

## Creating Custom Models

Let's run through a simple example of adding addresses to the app to
demonstrate how to customize things.  First we'll need to create the
model for our addresses.  This will be a simple object with the fields:

- Line1
- Line2
- City
- State
- Zip Code

We'll also assume you're using SQLAlchemy for a SQL database storage
system (for which support is built-in).

### Create the Schema

First we need to create the schema for this model.  The schema define
how your backend API and frontend will communicate to one another (data
expected, format, etc.).  For each model you'll likely need four schema:

- **Create**: What data do you need to create a new model?
- **Update**: What data do you need to update an existing model?
- **Read**: This is the (typical) format for the model returned to the
    frontend.
- **Stored**: Is there any additional data stored in the storage system
    for the object?

So let's do this for the new ``Address`` object.  First, create a new
file ``app/schema/address.py`` with the following:

```python
import typing as tp
from uuid import UUID

from app.schema.base import BaseSchemaJS


# Base model with common attributes
class AddressBase(BaseSchemaJS):
    line2: tp.Optional[str] = None


# Create model: the data needed to create a new Address
class AddressCreate(AddressBase):
    line1: str
    city: str
    state: str
    zipCode: str


# Update model: the data needed for updating an Address
class AddressUpdate(AddressBase):
    line1: tp.Optional[str] = None
    city: tp.Optional[str] = None
    state: tp.Optional[str] = None
    zipCode: tp.Optional[str] = None


# Read (main) model: the data for an existing Address
# NOTE: we could just extend the AddressCreate, since it already
#       defines most of these attributes.
class Address(AddressBase):
    uid: tp.Optional[UUID] = None
    line1: str
    city: str
    state: str
    zipCode: str

    class Config:
        orm_mode = True


# Stored model: any additional data specific to storage of the model
class AddressStored(Address):
    pass

```

### Define the CRUD Storage Model

Now we create the storage model (essentially an
[interface](https://en.wikipedia.org/wiki/Interface-based_programming))
which defines the model object's attributes and functionality.  We
create these primarily for the type-checking system.  Since the storage
system is loaded dynamically, we want the type-checker to understand
what to expect for this model (irrespective of the storage system
chosen) - *I'm a stickler for typing in Python*.

Create a new file, ``app/crud/models/address.py``, with the following:

```python
import typing as tp

from app.crud.models.base import Model, ModelBase

AddressType = tp.TypeVar('AddressType', bound='AddressBase')


# This is our interface, telling the system what to expect from an
# Address object.
class Address(Model, tp.Protocol):
    line1: str
    line2: tp.Optional[str]
    city: str
    state: str
    zipCode: str


# This is the actual base-class for the Address model.
class AddressBase(ModelBase):
    line1: str
    line2: tp.Optional[str]
    city: str
    state: str
    zipCode: str

```

This may seem annoying and repetitive, but it keeps our code
strongly-typed and will help avoid errors down-the-road.  The last step
here is to make sure these objects are imported in the ``models``
sub-package/module.  Open the ``app/crud/models/__init__.py`` file and
add the following:

```python
from app.crud.models.address import (
    Address,
    AddressBase,
)
```

### Define the CRUD Storage Repository

Now, utilizing the [repository pattern](https://martinfowler.com/eaaCatalog/repository.html),
we'll define how the storage system manages our Address objects.  The
basic CRUD functionality (``get``, ``get_multi``, ``create``,
``update``, and ``remove``) is already implemented in the base classes.
Here we'll define any special functionality we may need for this
particular model - in this case we might want to be able to get all the
addresses from a particular state.  If we didn't need any specific
functionality for this model (if the standard CRUD functions above would
suffice for our use) we could skip this step.  Create a new file,
``app/crud/repos/address.py``, with the following:

```python
from abc import ABCMeta, abstractmethod
import typing as tp

from app.crud.models.address import AddressType
from app.crud.repos.base import Repository, RepositoryBase
from app.schema.address import AddressCreate, AddressUpdate


# Again we define the interface first
class AddressRepository(Repository, tp.Protocol):
    def get_by_state(self, state: str) -> tp.List[AddressType]:
        ...


# Now we define the base class (as before)
class AddressRepositoryBase(
    RepositoryBase[AddressType, AddressCreate, AddressUpdate],
    metaclass=ABCMeta,
):
    @abstractmethod
    def get_by_state(self, state: str) -> tp.List[AddressType]:
        pass

```

Then open the file ``app/crud/repos/__init__.py`` and (again) make sure
these two objects are imported like before.

While, again, this may all seem redundent - there is usefulness in this
approach (beyond just keeping the type-checking in order).  If you look
at the [``app/crud/repos/user.py``](./app/crud/repos/user.py) source
code, you'll see that we define some helpful, storage-agnostic
functionality allowing us to just implement the storage-specific
functions - which we'll do right after we define the *actual* storage
implementation model (shortly)

### Register the AddressRepository with the UnitOfWork

The heart of the storage system is the repositories which are contained
within a ``UnitOfWork`` class (implementing that
[pattern](https://martinfowler.com/eaaCatalog/unitOfWork.html)).  Since
we're using a "custom" storage repository for our Address objects, we
need to make sure each ``UnitOfWork`` object uses it to manage the
Address objects.  Open the file ``app/crud/core.py`` and add the new
model and repository to the ``MODEL_MAP`` variable there.  This will
make sure the correct storage repository (regardless of the backend) is
used for managing Address objects.

### Create the Storage Model (Implementation)

As a reminder, we're assuming that we're using SQLAlchemy here.  So we
need to create a table for storing our Address objects.  To do this, we
create a new file, ``app/drivers/sqlalchemy/models/address.py``, with
the following table definition:

```python
import sqlalchemy as sa

from app.crud.models.address import AddressBase
from app.drivers.sqlalchemy.models.base import Base


class Address(AddressBase, Base):
    line1 = sa.Column(sa.String)
    line2 = sa.Column(sa.String, nullable=True)
    city = sa.Column(sa.String)
    state = sa.Column(sa.String, index=True)
    zipCode = sa.Column(sa.String)

```

Now SQLAlchemy knows how to store the data.  Note that we set ``state``
to be indexed: since we'll be using our ``get_by_state`` function this
will speed-up lookups on this.

Once again, make sure this is imported in the
``app/drivers/sqlalchemy/models/__init__.py`` file and that it's name is
added to the ``__all__`` variable (*this is important for the dynamic
loading*).

### Create the Storage Repository (Implementation)

We're almost there with the storage-side of things!  We just need to
create the SQLAlchemy implementation of the ``AddressRepository``
object.  Once again, all the basics are already taken care of (``get``,
``create``, etc.) in the base class.  Create a new file,
``app/drivers/sqlalchemy/repos/address.py``, with the following:

```python
import typing as tp

from sqlalchemy import asc

from app.crud.repos.address import AddressRepositoryBase
from app.drivers.sqlalchemy.crud import SQLRepositoryMixin
from app.drivers.sqlalchemy.models.address import Address


class AddressRepository(SQLRepositoryMixin, AddressRepositoryBase[Address]):
    # We can (optional) set the default ordering here
    __order_by__ = {
        'line1': asc,
        'line2': asc,
    }

    # We now write the implementation method for get_by_state
    def get_by_state(self, state: str) -> tp.List[Address]:
        return self.uow.db.query(self.model) \
            .filter(self.model.state == state) \
            .all()

```

Once again, the last step is to add this to the
``app/drivers/sqlalchemy/repos/__init__.py`` file, like before.  That's
it!  You can now create, update, get, and remove Address objects in the
storage system.

## Creating Additional API Endpoints

Continuing with the example (from above) let's now create some endpoints
for the API to allow interaction with our new Address storage system.
Since we've already defined most of the necessary components, this part
is pretty simple.

We'll just demonstrate a few functions here:

- Get all addresses
- Create a new address
- Get all addresses by state

Create a new file, ``app/api/v1/endpoints/addresses.py``, with the
following:

```python
import typing as tp
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from fastapi.encoders import jsonable_encoder

from app import schema
from app.api.common import (
    get_current_active_user,
    get_uow,
)
from app.crud.base import (
    IUnitOfWork,
    models,
)


router = APIRouter()


@router.get("/", response_model=tp.List[schema.Address])
async def read_addresses(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
) -> tp.List[models.Address]:
    """Gets all addresses specified."""
    return uow.address.get_multi(skip=skip, limit=limit)


@router.post("/", response_model=schema.Address)
async def create_address(
    *,
    uow: IUnitOfWork = Depends(get_uow),
    address_in: schema.AddressCreate,
    current_user: models.User = Depends(get_current_active_user),
) -> models.Address:
    """Creates a new address."""
    with uow:
        address = uow.address.create(address_in)
    return address


@router.get("/state/{state}", response_model=tp.List[schema.Address])
async def read_addresses_by_state(
    state: str,
    *,
    uow: IUnitOfWork = Depends(get_uow),
    current_user: models.User = Depends(get_current_active_user),
) -> tp.List[models.Address]:
    """Gets all the addresses for a specified state."""
    return uow.address.get_by_state(state)

```

There are a few things to note here:

- All the interactions with the storage system are done through the
  ``uow`` instance, which is automatically injected into the function.
- When creating or updating objects, we use the ``uow`` as a
  context-manager (via the ``with`` clause).  This ensures that if an
  error occurs during creation/updating that any changes will be rolled
  back before an error is thrown.
- The ``current_user`` argument automatically inserts the current user
  calling the API endpoint.  While we don't actually use this here, it
  ensures that only logged-in, active users can use these endpoints.

Now we just need to wire-up the application router with this new set of
API endpoints.  To do this open up ``app/api/v1/api.py`` and add the
following lines to the file:

```python
from app.api.v1.endpoints import (
    addresses,
    ...,
)

...

api_router.include_router(addresses.router, prefix="/addresses",
                          tags=["addresses"])

```

And that's that - these endpoints are now available on the backend API
server for use in your front-end application.
