from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, RootModel


class TenderRecord(BaseModel):
    """Summary information for one public tender."""

    code: str = Field(validation_alias="CodigoExterno")
    name: str = Field(validation_alias="Nombre")
    status_code: int = Field(validation_alias="CodigoEstado")
    closing_at: datetime | None = Field(default=None, validation_alias="FechaCierre")


class TenderList(RootModel[list[TenderRecord]]):
    """A list of public-tender summaries."""


class TenderResult(BaseModel):
    """Envelope returned by public-tender list queries."""

    quantity: int = Field(validation_alias="Cantidad")
    created_at: datetime = Field(validation_alias="FechaCreacion")
    version: str = Field(validation_alias="Version")
    records: TenderList = Field(validation_alias="Listado")


class TenderBuyer(BaseModel):
    code: int = Field(validation_alias="CodigoOrganismo")
    name: str = Field(validation_alias="NombreOrganismo")
    unit_rut: str = Field(validation_alias="RutUnidad")
    unit_code: int = Field(validation_alias="CodigoUnidad")
    unit_name: str = Field(validation_alias="NombreUnidad")
    unit_address: str = Field(validation_alias="DireccionUnidad")
    unit_commune: str = Field(validation_alias="ComunaUnidad")
    unit_region: str = Field(validation_alias="RegionUnidad")
    user_rut: str = Field(validation_alias="RutUsuario")
    user_code: int = Field(validation_alias="CodigoUsuario")
    user_name: str = Field(validation_alias="NombreUsuario")
    user_position: str = Field(validation_alias="CargoUsuario")


class TenderDates(BaseModel):
    created_at: datetime = Field(validation_alias="FechaCreacion")
    closing_at: datetime | None = Field(validation_alias="FechaCierre")
    starts_at: datetime | None = Field(validation_alias="FechaInicio")
    ends_at: datetime | None = Field(validation_alias="FechaFinal")
    answers_published_at: datetime | None = Field(validation_alias="FechaPubRespuestas")
    technical_opening_at: datetime | None = Field(validation_alias="FechaActoAperturaTecnica")
    economic_opening_at: datetime | None = Field(validation_alias="FechaActoAperturaEconomica")
    published_at: datetime | None = Field(validation_alias="FechaPublicacion")
    awarded_at: datetime | None = Field(validation_alias="FechaAdjudicacion")
    estimated_awarded_at: datetime | None = Field(validation_alias="FechaEstimadaAdjudicacion")
    physical_support_at: datetime | None = Field(validation_alias="FechaSoporteFisico")
    evaluation_at: datetime | None = Field(validation_alias="FechaTiempoEvaluacion")
    estimated_signed_at: datetime | None = Field(validation_alias="FechaEstimadaFirma")
    user_dates: Any | None = Field(validation_alias="FechasUsuario")
    site_visit_at: datetime | None = Field(validation_alias="FechaVisitaTerreno")
    antecedents_delivery_at: datetime | None = Field(validation_alias="FechaEntregaAntecedentes")


class TenderItemAward(BaseModel):
    supplier_rut: str = Field(validation_alias="RutProveedor")
    supplier_name: str = Field(validation_alias="NombreProveedor")
    quantity: float = Field(validation_alias="Cantidad")
    unit_amount: float = Field(validation_alias="MontoUnitario")


class TenderItemRecord(BaseModel):
    correlative: int = Field(validation_alias="Correlativo")
    product_code: int = Field(validation_alias="CodigoProducto")
    category_code: str = Field(validation_alias="CodigoCategoria")
    category: str = Field(validation_alias="Categoria")
    product_name: str = Field(validation_alias="NombreProducto")
    description: str = Field(validation_alias="Descripcion")
    measure_unit: str = Field(validation_alias="UnidadMedida")
    quantity: float = Field(validation_alias="Cantidad")
    awarded: TenderItemAward | dict[str, Any] | None = Field(
        default=None,
        validation_alias="Adjudicacion",
    )


class TenderItemList(RootModel[list[TenderItemRecord]]):
    """A list of line items in a tender."""


class TenderItems(BaseModel):
    quantity: int = Field(validation_alias="Cantidad")
    records: TenderItemList = Field(validation_alias="Listado")

    @property
    def entries(self) -> list[TenderItemRecord]:
        """Compatibility view of the underlying item list."""
        return self.records.root


class TenderAward(BaseModel):
    type: int = Field(validation_alias="Tipo")
    date: datetime = Field(validation_alias="Fecha")
    number: str = Field(validation_alias="Numero")
    url: HttpUrl = Field(validation_alias="UrlActa")


class TenderDetailsRecord(BaseModel):
    code: str = Field(validation_alias="CodigoExterno")
    name: str = Field(validation_alias="Nombre")
    status_code: int = Field(validation_alias="CodigoEstado")
    description: str = Field(validation_alias="Descripcion")
    closing_at: datetime | None = Field(validation_alias="FechaCierre")
    status: str = Field(validation_alias="Estado")
    closing_days: int = Field(validation_alias="DiasCierreLicitacion")
    informed: int = Field(validation_alias="Informada")
    type_code: int = Field(validation_alias="CodigoTipo")
    tender_type: str = Field(validation_alias="Tipo")
    call_type: int = Field(validation_alias="TipoConvocatoria")
    currency: str = Field(validation_alias="Moneda")
    stages: int = Field(validation_alias="Etapas")
    stages_status: int = Field(validation_alias="EstadoEtapas")
    requires_review: int = Field(validation_alias="TomaRazon")
    offers_visible: int = Field(validation_alias="EstadoPublicidadOfertas")
    offers_visible_reason: str = Field(validation_alias="JustificacionPublicidad")
    contract: int = Field(validation_alias="Contrato")
    public_work: int = Field(validation_alias="Obras")
    claims_number: int = Field(validation_alias="CantidadReclamos")
    evaluation_time_unit: int | None = Field(validation_alias="UnidadTiempoEvaluacion")
    visit_address: str = Field(validation_alias="DireccionVisita")
    delivery_address: str = Field(validation_alias="DireccionEntrega")
    estimation: int | None = Field(validation_alias="Estimacion")
    funding_source: str = Field(validation_alias="FuenteFinanciamiento")
    amount_visibility: int = Field(validation_alias="VisibilidadMonto")
    estimated_amount: float | None = Field(validation_alias="MontoEstimado")
    time: int | None = Field(validation_alias="Tiempo")
    time_unit: int = Field(validation_alias="UnidadTiempo")
    mode: int = Field(validation_alias="Modalidad")
    payment_type: int = Field(validation_alias="TipoPago")
    payment_responsible_name: str = Field(validation_alias="NombreResponsablePago")
    payment_responsible_email: str = Field(validation_alias="EmailResponsablePago")
    contract_responsible_name: str = Field(validation_alias="NombreResponsableContrato")
    contract_responsible_email: str = Field(validation_alias="EmailResponsableContrato")
    contract_responsible_phone: str = Field(validation_alias="FonoResponsableContrato")
    hiring_ban: str = Field(validation_alias="ProhibicionContratacion")
    subcontracting: int = Field(validation_alias="SubContratacion")
    contract_duration_time_unit: int = Field(validation_alias="UnidadTiempoDuracionContrato")
    contract_duration_time: int = Field(validation_alias="TiempoDuracionContrato")
    contract_duration_type: str = Field(validation_alias="TipoDuracionContrato")
    amount_estimate_justification: str = Field(validation_alias="JustificacionMontoEstimado")
    contract_observation: str | None = Field(validation_alias="ObservacionContract")
    term_extension: int = Field(validation_alias="ExtensionPlazo")
    is_base_type: int = Field(validation_alias="EsBaseTipo")
    tender_contract_time_unit: int = Field(validation_alias="UnidadTiempoContratoLicitacion")
    renewal_time_value: int = Field(validation_alias="ValorTiempoRenovacion")
    renewal_time_period: str = Field(validation_alias="PeriodoTiempoRenovacion")
    is_renewable: int = Field(validation_alias="EsRenovable")
    bip_code: str | None = Field(validation_alias="CodigoBIP")
    awarded: TenderAward | dict[str, Any] | None = Field(
        default=None,
        validation_alias="Adjudicacion",
    )
    dates: TenderDates = Field(validation_alias="Fechas")
    buyer: TenderBuyer = Field(validation_alias="Comprador")
    items: TenderItems = Field(validation_alias="Items")


class TenderDetailsList(RootModel[list[TenderDetailsRecord]]):
    """A list containing detailed tender records."""


class TenderDetailsResult(BaseModel):
    """Envelope returned by a tender detail query."""

    quantity: int = Field(validation_alias="Cantidad")
    created_at: datetime = Field(validation_alias="FechaCreacion")
    version: str = Field(validation_alias="Version")
    records: TenderDetailsList = Field(validation_alias="Listado")

    @property
    def entries(self) -> list[TenderDetailsRecord]:
        """Compatibility view of the underlying detail list."""
        return self.records.root


__all__ = (
    "TenderAward",
    "TenderBuyer",
    "TenderDates",
    "TenderDetailsList",
    "TenderDetailsRecord",
    "TenderDetailsResult",
    "TenderItemAward",
    "TenderItemList",
    "TenderItemRecord",
    "TenderItems",
    "TenderList",
    "TenderRecord",
    "TenderResult",
)
