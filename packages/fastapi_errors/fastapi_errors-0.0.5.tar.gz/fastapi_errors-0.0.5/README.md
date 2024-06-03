**Example of using exceptions schema generator for FastAPI.**

```
from abc import abstractproperty
from typing import Optional
from fastapi import FastAPI
from fastapi_errors.exceptions import DefaultHTTPException, BaseHTTPException
from fastapi_errors.generator import generate_examples, ExamplesGenerator
from starlette.responses import JSONResponse

app = FastAPI()


class NotAuthorized(DefaultHTTPException):
    error = "UNAUTHORIZED"
    status_code = 401
    message = "Not authorized."
    field = None


class StaffOnly(DefaultHTTPException):
    error = "STAFF_ONLY"
    status_code = 401
    message = "Staff only."
    field = None


@app.get(
    "/",
    responses=generate_examples(
        NotAuthorized
    )
)
async def get():
    pass


class CustomException(BaseHTTPException):
    """Custom class for all HTTP exceptions."""

    error: str = abstractproperty()
    message: str = abstractproperty()
    field: Optional[str] = abstractproperty()
    item_id: int = abstractproperty()

    def __init__(
        self,
        item_id: Optional[int] = None,
        message: Optional[str] = None,
        field: Optional[str] = None
    ) -> None:
        """Initialize the exception."""
        self.message = message if message else self.message
        self.field = field if field else self.field
        self.item_id = item_id
        super().__init__()

    def example(self) -> dict:
        """Return an example of the error response. This is used in the OpenAPI docs."""
        # create details
        details = {
            "field": "string",
            "message": self.message,
            "item_id": self.item_id,
        }
        # create example
        example = {
            "summary": self.error,
            "value": {
                "status": self.status_code,
                "error": {"code": self.error, "details": details},
            },
        }
        return example


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "code": exc.error,
            "details": {
                "message": str(exc.message),
                "field": exc.field,
                "item_id": exc.item_id,
            },
        },
    )


class MyException(CustomException):
    """Custom exception class."""

    error = "MY_ERROR"
    message = "My error message."
    item_id = 1
    field = None


class CustomExamplesGenerator(ExamplesGenerator):
    """Custom examples generator."""

    default_exceptions = (
        NotAuthorized,
    )

    staff = (
        StaffOnly,
    )


generate_examples = CustomExamplesGenerator.generate_examples


@app.get(
    "/{item_id}",
    responses=generate_examples(
        MyException,
        add=["staff"]
    )
)
async def get_item(item_id: int):
    raise MyException(item_id=item_id, field="burger")
```
