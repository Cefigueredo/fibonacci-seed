import db_gateway
import schemas
import settings
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from utils import solver

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    """Validate API key and secret"""
    if not api_key_header or api_key_header != settings.Settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return True


@app.get("/fibonacci-seed/", dependencies=[Depends(get_api_key)])
async def get_fibonacci_seed():
    solver_instance = solver.Solver()

    return JSONResponse(content={"fibonacci": solver_instance.solve()})


@app.post("/fibonacci-seed/", dependencies=[Depends(get_api_key)])
async def post_fibonacci_seed(
    datetime: schemas.Input,
):

    solver_instance = solver.Solver()

    return JSONResponse(
        content={
            "fibonacci": solver_instance.solve(datetime=datetime.datetime)
        }
    )


@app.get("/fibonacci-seed/db/", dependencies=[Depends(get_api_key)])
async def get_fibonacci_seed_from_db():
    db = db_gateway.DBGateway()
    data = db.read_fibonacci()
    return JSONResponse(content=data)
