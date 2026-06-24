from fastapi.responses import JSONResponse


def api_response(
    data=None,
    message=None,
    status_code=200,
    meta=None
):
    response = {
        "error": False,
        "message": message,
        "statusCode": status_code,
        "data": data,
    }

    if meta:
        response["meta"] = meta

    return JSONResponse(
        content=response,
        status_code=status_code
    )