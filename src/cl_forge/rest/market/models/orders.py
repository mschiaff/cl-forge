from datetime import datetime

from pydantic import BaseModel, Field, RootModel


class OrderRecord(BaseModel):
    """Summary information for one purchase order."""

    code: str = Field(validation_alias="Codigo")
    name: str = Field(validation_alias="Nombre")
    status_code: int = Field(validation_alias="CodigoEstado")


class OrderList(RootModel[list[OrderRecord]]):
    """A list of purchase-order summaries."""


class OrderResult(BaseModel):
    """Envelope returned by purchase-order list queries."""

    quantity: int = Field(validation_alias="Cantidad")
    created_at: datetime = Field(validation_alias="FechaCreacion")
    version: str = Field(validation_alias="Version")
    records: OrderList = Field(validation_alias="Listado")


class OrderDates(BaseModel):
    created_at: datetime = Field(validation_alias="FechaCreacion")
    sent_at: datetime | None = Field(validation_alias="FechaEnvio")
    accepted_at: datetime | None = Field(validation_alias="FechaAceptacion")
    cancelled_at: datetime | None = Field(validation_alias="FechaCancelacion")
    last_modified_at: datetime | None = Field(validation_alias="FechaUltimaModificacion")


class OrderBuyer(BaseModel):
    code: int = Field(validation_alias="CodigoOrganismo")
    name: str = Field(validation_alias="NombreOrganismo")
    unit_rut: str = Field(validation_alias="RutUnidad")
    unit_code: int = Field(validation_alias="CodigoUnidad")
    unit_name: str = Field(validation_alias="NombreUnidad")
    activity: str = Field(validation_alias="Actividad")
    unit_address: str = Field(validation_alias="DireccionUnidad")
    unit_commune: str = Field(validation_alias="ComunaUnidad")
    unit_region: str = Field(validation_alias="RegionUnidad")
    country: str = Field(validation_alias="Pais")
    contact_name: str = Field(validation_alias="NombreContacto")
    contact_job_title: str = Field(validation_alias="CargoContacto")
    contact_phone: str | None = Field(validation_alias="FonoContacto")
    contact_email: str | None = Field(validation_alias="MailContacto")


class OrderSupplier(BaseModel):
    code: int = Field(validation_alias="Codigo")
    name: str = Field(validation_alias="Nombre")
    activity: str = Field(validation_alias="Actividad")
    branch_code: int = Field(validation_alias="CodigoSucursal")
    branch_name: str = Field(validation_alias="NombreSucursal")
    branch_rut: str = Field(validation_alias="RutSucursal")
    address: str = Field(validation_alias="Direccion")
    commune: str = Field(validation_alias="Comuna")
    region: str = Field(validation_alias="Region")
    country: str = Field(validation_alias="Pais")
    contact_name: str = Field(validation_alias="NombreContacto")
    contact_job_title: str = Field(validation_alias="CargoContacto")
    contact_phone: str | None = Field(validation_alias="FonoContacto")
    contact_email: str | None = Field(validation_alias="MailContacto")


class OrderItemRecord(BaseModel):
    correlative: int = Field(validation_alias="Correlativo")
    category_code: int = Field(validation_alias="CodigoCategoria")
    category: str = Field(validation_alias="Categoria")
    product_code: int = Field(validation_alias="CodigoProducto")
    product: str = Field(validation_alias="Producto")
    buyer_specification: str | None = Field(validation_alias="EspecificacionComprador")
    supplier_specification: str | None = Field(validation_alias="EspecificacionProveedor")
    quantity: float = Field(validation_alias="Cantidad")
    unit: str | None = Field(validation_alias="Unidad")
    currency: str = Field(validation_alias="Moneda")
    net_price: float = Field(validation_alias="PrecioNeto")
    total_charges: float = Field(validation_alias="TotalCargos")
    total_discounts: float = Field(validation_alias="TotalDescuentos")
    total_taxes: float = Field(validation_alias="TotalImpuestos")
    total: float = Field(validation_alias="Total")


class OrderItemList(RootModel[list[OrderItemRecord]]):
    """A list of purchase-order line items."""


class OrderItems(BaseModel):
    quantity: int = Field(validation_alias="Cantidad")
    records: OrderItemList = Field(validation_alias="Listado")


class OrderDetailsRecord(BaseModel):
    code: str = Field(validation_alias="Codigo")
    name: str = Field(validation_alias="Nombre")
    status_code: int = Field(validation_alias="CodigoEstado")
    status: str = Field(validation_alias="Estado")
    tender_code: str = Field(validation_alias="CodigoLicitacion")
    description: str = Field(validation_alias="Descripcion")
    type_code: int = Field(validation_alias="CodigoTipo")
    type: str = Field(validation_alias="Tipo")
    currency_type: str = Field(validation_alias="TipoMoneda")
    supplier_status_code: int = Field(validation_alias="CodigoEstadoProveedor")
    supplier_status: str = Field(validation_alias="EstadoProveedor")
    has_items: int = Field(validation_alias="TieneItems")
    average_rating: float = Field(validation_alias="PromedioCalificacion")
    evaluation_quantity: int = Field(validation_alias="CantidadEvaluacion")
    discounts: float = Field(validation_alias="Descuentos")
    charges: float = Field(validation_alias="Cargos")
    net_total: float = Field(validation_alias="TotalNeto")
    vat_percentage: float = Field(validation_alias="PorcentajeIva")
    taxes: float = Field(validation_alias="Impuestos")
    total: float = Field(validation_alias="Total")
    funding: str = Field(validation_alias="Financiamiento")
    country: str = Field(validation_alias="Pais")
    dispatch_type: int = Field(validation_alias="TipoDespacho")
    payment_method: int = Field(validation_alias="FormaPago")
    dates: OrderDates = Field(validation_alias="Fechas")
    buyer: OrderBuyer = Field(validation_alias="Comprador")
    supplier: OrderSupplier = Field(validation_alias="Proveedor")
    items: OrderItems = Field(validation_alias="Items")


class OrderDetailsList(RootModel[list[OrderDetailsRecord]]):
    """A list containing detailed purchase-order records."""


class OrderDetailsResult(BaseModel):
    """Envelope returned by a purchase-order detail query."""

    quantity: int = Field(validation_alias="Cantidad")
    created_at: datetime = Field(validation_alias="FechaCreacion")
    version: str = Field(validation_alias="Version")
    records: OrderDetailsList = Field(validation_alias="Listado")


__all__ = (
    "OrderBuyer",
    "OrderDates",
    "OrderDetailsList",
    "OrderDetailsRecord",
    "OrderDetailsResult",
    "OrderItemList",
    "OrderItemRecord",
    "OrderItems",
    "OrderList",
    "OrderRecord",
    "OrderResult",
    "OrderSupplier",
)
