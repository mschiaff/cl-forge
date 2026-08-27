import asyncio
from dataclasses import dataclass
from typing import cast

from httpx2 import AsyncClient, Client, MockTransport, Request, Response
from pydantic import SecretStr

from cl_forge.rest.client.route import ClientRoute
from cl_forge.rest.market import AsyncMarketClient, MarketClient
from cl_forge.rest.market.models.directory import BuyerResult, SupplierRecord
from cl_forge.rest.market.models.orders import OrderResult
from cl_forge.rest.market.models.tenders import TenderResult
from cl_forge.rest.market.provider import MARKET_V1, MARKET_V2
from cl_forge.rest.market.resources.directory import (
    AsyncBuyerResource,
    AsyncSupplierResource,
    BuyerResource,
    SupplierResource,
)
from cl_forge.rest.market.resources.orders import AsyncOrderResource, OrderResource
from cl_forge.rest.market.resources.raw import AsyncRawResource, RawResource
from cl_forge.rest.market.resources.tenders import AsyncTenderResource, TenderResource
from cl_forge.rest.market.resources.types import (
    OrderStatusCode,
    TenderStatusCode,
    normalize_rut,
    serialize_date,
)

TENDER_DATA = {
    "Cantidad": 1,
    "FechaCreacion": "2026-08-27T10:00:00Z",
    "Version": "v1",
    "Listado": [
        {
            "CodigoExterno": "1000-1-L126",
            "Nombre": "Tender",
            "CodigoEstado": 5,
            "FechaCierre": "2026-08-28T10:00:00Z",
        }
    ],
}

ORDER_DATA = {
    "Cantidad": 1,
    "FechaCreacion": "2026-08-27T10:00:00Z",
    "Version": "v1",
    "Listado": [{"Codigo": "1000-1-SE26", "Nombre": "Order", "CodigoEstado": 6}],
}

SUPPLIER_DATA = {
    "Cantidad": 1,
    "FechaCreacion": "2026-08-27T10:00:00Z",
    "listaEmpresas": [{"CodigoEmpresa": 17793, "NombreEmpresa": "Supplier"}],
}

BUYER_DATA = {
    "Cantidad": 2,
    "FechaCreacion": "2026-08-27T10:00:00Z",
    "listaEmpresas": [
        {"CodigoEmpresa": 10, "NombreEmpresa": "Universidad de Chile"},
        {"CodigoEmpresa": 20, "NombreEmpresa": "Municipalidad de Santiago"},
    ],
}


@dataclass
class StubRoute:
    client: Client
    aclient: AsyncClient
    requests: list[Request]


def _response(request: Request) -> Response:
    path = request.url.path
    if path.endswith("/licitaciones.json"):
        return Response(200, json=TENDER_DATA)
    if path.endswith("/OrdenesDeCompra.json"):
        return Response(200, json=ORDER_DATA)
    if path.endswith("/Empresas/BuscarProveedor"):
        return Response(200, json=SUPPLIER_DATA)
    if path.endswith("/Empresas/BuscarComprador"):
        return Response(200, json=BUYER_DATA)
    if path.endswith("/custom.json"):
        return Response(200, json={"ok": True})
    if path.endswith("/custom.xml"):
        return Response(200, text="<ok />")
    if path.endswith("/v2/compra-agil"):
        return Response(200, json={"success": "OK", "payload": {}})
    return Response(404, json={"error": path})


def _routes() -> tuple[StubRoute, StubRoute]:
    requests: list[Request] = []

    def record(request: Request) -> Response:
        requests.append(request)
        return _response(request)

    transport = MockTransport(record)
    v1 = StubRoute(
        Client(base_url=MARKET_V1.base_url, transport=transport),
        AsyncClient(base_url=MARKET_V1.base_url, transport=transport),
        requests,
    )
    v2 = StubRoute(
        Client(base_url=MARKET_V2.base_url, transport=transport),
        AsyncClient(base_url=MARKET_V2.base_url, transport=transport),
        requests,
    )
    return v1, v2


def _as_route(route: StubRoute) -> ClientRoute:
    return cast("ClientRoute", route)


def test_market_client_uses_credentials_and_singular_resources() -> None:
    client = MarketClient(SecretStr(" ticket "))
    aclient = AsyncMarketClient("ticket")

    assert client.credentials.value == "ticket"
    assert client.provider.value == "market"
    assert client.base_url == MARKET_V1.base_url
    assert "ticket" not in repr(client)
    assert isinstance(client.tender, TenderResource)
    assert isinstance(client.order, OrderResource)
    assert isinstance(client.supplier, SupplierResource)
    assert isinstance(client.buyer, BuyerResource)
    assert isinstance(client.raw, RawResource)
    assert isinstance(aclient.tender, AsyncTenderResource)
    assert isinstance(aclient.order, AsyncOrderResource)


def test_market_query_helpers_and_current_status_codes() -> None:
    assert serialize_date("2024-01-02") == "02012024"
    assert normalize_rut("70017820-k") == "70.017.820-K"
    assert TenderStatusCode.REVOKED == 18
    assert TenderStatusCode.SUSPENDED == 19
    assert OrderStatusCode.PENDING == 13
    assert OrderStatusCode.PARTIAL == 14
    assert OrderStatusCode.INCOMPLETE == 15


def test_sync_market_resources_build_requests_and_parse_models() -> None:
    v1, v2 = _routes()
    route = _as_route(v1)

    tender = TenderResource(route).by_status("Adjudicada", date="2024-01-02")
    order = OrderResource(route).all(date="2024-01-02")
    supplier = SupplierResource(route).search("70017820-k", only_record=True)
    buyers = BuyerResource(route).search()
    raw = RawResource(route, _as_route(v2))

    assert isinstance(tender, TenderResult)
    assert tender.records.root[0].code == "1000-1-L126"
    assert isinstance(order, OrderResult)
    assert isinstance(supplier, SupplierRecord)
    assert supplier.code == 17793
    assert isinstance(buyers, BuyerResult)
    assert buyers.contains("Universidad").root[0].code == 10
    assert buyers.by_code(20).name == "Municipalidad de Santiago"
    assert raw.json.get("/custom") == {"ok": True}
    assert raw.xml.get("/custom") == "<ok />"
    assert raw.v2.get("/compra-agil")["success"] == "OK"

    tender_request = next(
        request for request in v1.requests if request.url.path.endswith("/licitaciones.json")
    )
    assert tender_request.url.params["Estado"] == "adjudicada"
    assert tender_request.url.params["Fecha"] == "02012024"

    v1.client.close()
    v2.client.close()


def test_async_market_resources_match_sync_surface() -> None:
    async def run() -> None:
        v1, v2 = _routes()
        route = _as_route(v1)
        raw = AsyncRawResource(route, _as_route(v2))

        tender = await AsyncTenderResource(route).by_supplier(17793, date="2024-01-02")
        order = await AsyncOrderResource(route).by_date("2024-01-02")
        supplier = await AsyncSupplierResource(route).search(70_017_820, only_record=True)
        buyers = await AsyncBuyerResource(route).search()

        assert isinstance(tender, TenderResult)
        assert isinstance(order, OrderResult)
        assert isinstance(supplier, SupplierRecord)
        assert buyers.by_code(10).name == "Universidad de Chile"
        assert await raw.json.get("/custom") == {"ok": True}
        assert await raw.xml.get("/custom") == "<ok />"
        assert (await raw.v2.get("/compra-agil"))["success"] == "OK"

        await v1.aclient.aclose()
        await v2.aclient.aclose()
        v1.client.close()
        v2.client.close()

    asyncio.run(run())


def test_market_resources_reject_ticket_override_case_insensitively() -> None:
    v1, _ = _routes()
    resource = RawResource(_as_route(v1), _as_route(v1))

    try:
        resource.json.get("/custom", params={" Ticket ": "override"})
    except ValueError as error:
        assert "Ticket" in str(error)
    else:
        raise AssertionError("Expected reserved ticket parameter to be rejected")
