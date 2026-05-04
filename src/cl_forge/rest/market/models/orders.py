from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, Field, RootModel


class OrderRecord(BaseModel):
    code: str = Field(alias="Codigo")
    name: str = Field(alias="Nombre")
    status_code: int = Field(alias="CodigoEstado")


class OrderCollection(RootModel[list[OrderRecord]]): ...


class Order(BaseModel):
    quantity: int = Field(alias="Cantidad")
    created_at: str = Field(alias="FechaCreacion")
    version: str = Field(alias="Version")
    records: OrderCollection = Field(alias="Listado")


class OrderDates(BaseModel):
    created_at: datetime = Field(alias="FechaCreacion")
    sent_at: datetime | None = Field(alias="FechaEnvio")
    accepted_at: datetime | None = Field(alias="FechaAceptacion")
    cancelled_at: datetime | None = Field(alias="FechaCancelacion")
    last_modified_at: datetime | None = Field(alias="FechaUltimaModificacion")


class OrderBuyer(BaseModel):
    code: int = Field(alias="CodigoOrganismo")
    name: str = Field(alias="NombreOrganismo")
    unit_rut: str = Field(alias="RutUnidad")
    unit_code: int = Field(alias="CodigoUnidad")
    unit_name: str = Field(alias="NombreUnidad")
    activity: str = Field(alias="Actividad")
    unit_address: str = Field(alias="DireccionUnidad")
    unit_commune: str = Field(alias="ComunaUnidad")
    unit_region: str = Field(alias="RegionUnidad")
    country: str = Field(alias="Pais")
    contact_name: str = Field(alias="NombreContacto")
    contact_job_title: str = Field(alias="CargoContacto")
    contact_phone: str | None = Field(alias="FonoContacto")
    contact_email: str | None = Field(alias="MailContacto")


class OrderSupplier(BaseModel):
    code: int = Field(alias="Codigo")
    name: str = Field(alias="Nombre")
    activity: str = Field(alias="Actividad")
    branch_code: int = Field(alias="CodigoSucursal")
    branch_name: str = Field(alias="NombreSucursal")
    branch_rut: str = Field(alias="RutSucursal")
    address: str = Field(alias="Direccion")
    commune: str = Field(alias="Comuna")
    region: str = Field(alias="Region")
    country: str = Field(alias="Pais")
    contact_name: str = Field(alias="NombreContacto")
    contact_job_title: str = Field(alias="CargoContacto")
    contact_phone: str | None = Field(alias="FonoContacto")
    contact_email: str | None = Field(alias="MailContacto")


class OrderItemsRecord(BaseModel):
    correlative: int = Field(alias="Correlativo")
    category_code: int = Field(alias="CodigoCategoria")
    category: str = Field(alias="Categoria")
    product_code: int = Field(alias="CodigoProducto")
    product: str = Field(alias="Producto")
    buyer_specification: str = Field(alias="EspecificacionComprador")
    supplier_specification: str = Field(alias="EspecificacionProveedor")
    quantity: int = Field(alias="Cantidad")
    unit: str | None = Field(alias="Unidad")
    currency: str = Field(alias="Moneda")
    net_price: float = Field(alias="PrecioNeto")
    total_charges: float = Field(alias="TotalCargos")
    total_discounts: float = Field(alias="TotalDescuentos")
    total_taxes: float = Field(alias="TotalImpuestos")
    total: float = Field(alias="Total")


class OrderItemsCollection(RootModel[list[OrderItemsRecord]]): ...


class OrderItems(BaseModel):
    quantity: int = Field(alias="Cantidad")
    records: OrderItemsCollection = Field(alias="Listado")


class OrderDetailsRecord(BaseModel):
    code: str = Field(alias="Codigo")
    name: str = Field(alias="Nombre")
    status_code: int = Field(alias="CodigoEstado")
    status: str = Field(alias="Estado")
    tender_code: str = Field(alias="CodigoLicitacion")
    description: str = Field(alias="Descripcion")
    type_code: int = Field(alias="CodigoTipo")
    type: str = Field(alias="Tipo")
    currency_type: str = Field(alias="TipoMoneda")
    supplier_status_code: int = Field(alias="CodigoEstadoProveedor")
    supplier_status: str = Field(alias="EstadoProveedor")
    has_items: int = Field(alias="TieneItems")
    average_rating: float = Field(alias="PromedioCalificacion")
    evaluation_quantity: int = Field(alias="CantidadEvaluacion")
    discounts: float = Field(alias="Descuentos")
    charges: float = Field(alias="Cargos")
    net_total: float = Field(alias="TotalNeto")
    vat_percentage: float = Field(alias="PorcentajeIva")
    taxes: float = Field(alias="Impuestos")
    total: float = Field(alias="Total")
    funding: str = Field(alias="Financiamiento")
    country: str = Field(alias="Pais")
    dispatch_type: int = Field(alias="TipoDespacho")
    payment_method: int = Field(alias="FormaPago")
    dates: OrderDates = Field(alias="Fechas")
    buyer: OrderBuyer = Field(alias="Comprador")
    supplier: OrderSupplier = Field(alias="Proveedor")
    items: OrderItems = Field(alias="Items")


class OrderDetailsCollection(RootModel[list[OrderDetailsRecord]]): ...


class OrderDetails(BaseModel):
    quantity: int = Field(alias="Cantidad")
    created_at: str = Field(alias="FechaCreacion")
    version: str = Field(alias="Version")
    records: OrderDetailsCollection = Field(alias="Listado")
