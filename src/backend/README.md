# Web Application Backend API Skeleton

*The backend skeleton API for a modern web application.*

## Creating new Models

Customizing this skeleton for your use will likely require some
additional models specific to your use case.  Let's walk through an
example of adding an ``Address`` model to the framework.

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

So let's do this for the new ``Address`` object.
