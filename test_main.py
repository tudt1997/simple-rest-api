from fastapi.testclient import TestClient
from main import app, Endpoints, Messages, Pool


client = TestClient(app)

def test_api():
    response = client.post(Endpoints.INSERT_POOL, json={"poolId": 0, "poolValues": []})
    assert response.status_code == 400
    assert response.json() == {"detail": Messages.CANT_INSERT_POOL_WITH_EMPTY_VALUES}

    response = client.post(Endpoints.CALCULATE_QUANTILE, json={"poolId": 0, "percentile": 0.0})
    assert response.status_code == 404
    assert response.json() == {"detail": Messages.POOL_DOES_NOT_EXIST}

    response = client.post(Endpoints.INSERT_POOL, json={"poolId": 0, "poolValues": [1]})
    assert response.status_code == 200
    assert response.json() == {"status": "inserted"}
    
    response = client.post(Endpoints.INSERT_POOL, json={"poolId": 0, "poolValues": [0]})
    assert response.status_code == 200
    assert response.json() == {"status": "appended"}

    response = client.post(Endpoints.CALCULATE_QUANTILE, json={"poolId": 0, "percentile": 0.0})
    assert response.status_code == 200
    assert response.json() == {
        "quantile": 0,
        "totalCount": 2
    }

    response = client.post(Endpoints.CALCULATE_QUANTILE, json={"poolId": 0, "percentile": 50.0})
    assert response.status_code == 200
    assert response.json() == {
        "quantile": 0.5,
        "totalCount": 2
    }

    response = client.post(Endpoints.CALCULATE_QUANTILE, json={"poolId": 0, "percentile": 100.0})
    assert response.status_code == 200
    assert response.json() == {
        "quantile": 1,
        "totalCount": 2
    }
