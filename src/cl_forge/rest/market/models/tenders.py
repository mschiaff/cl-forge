from __future__ import annotations

from datetime import datetime  # noqa: TC003
from typing import Any

from pydantic import BaseModel, Field, RootModel

__all__ = ("Tender", "TenderDetails",)


class TenderRecord(BaseModel):
    code:           str         = Field(alias="CodigoExterno")
    name:           str         = Field(alias="Nombre")
    status_code:    int         = Field(alias="CodigoEstado")
    closing_date:   str | None  = Field(default=None, alias="FechaCierre")


class TenderCollection(RootModel[list[TenderRecord]]): ...


class Tender(BaseModel):
    quantity:       int                 = Field(alias="Cantidad")
    created_at:     str                 = Field(alias="FechaCreacion")
    version:        str                 = Field(alias="Version")
    records:        TenderCollection    = Field(alias="Listado")


class TenderBuyer(BaseModel):
    code:           int = Field(alias="CodigoOrganismo")
    name:           str = Field(alias="NombreOrganismo")
    unit_rut:       str = Field(alias="RutUnidad")
    unit_code:      int = Field(alias="CodigoUnidad")
    unit_name:      str = Field(alias="NombreUnidad")
    unit_address:   str = Field(alias="DireccionUnidad")
    unit_commune:   str = Field(alias="ComunaUnidad")
    unit_region:    str = Field(alias="RegionUnidad")
    user_rut:       str = Field(alias="RutUsuario")
    user_code:      int = Field(alias="CodigoUsuario")
    user_name:      str = Field(alias="NombreUsuario")
    user_position:  str = Field(alias="CargoUsuario")


class TenderDates(BaseModel):
    created_at:                 datetime            = Field(alias="FechaCreacion")
    closing_at:                 datetime | None     = Field(alias="FechaCierre")
    starts_at:                  datetime | None     = Field(alias="FechaInicio")
    ends_at:                    datetime | None     = Field(alias="FechaFinal")
    answers_published_at:       datetime | None     = Field(alias="FechaPubRespuestas")
    technical_opening_at:       datetime | None     = Field(alias="FechaActoAperturaTecnica")
    economic_opening_at:        datetime | None     = Field(alias="FechaActoAperturaEconomica")
    published_at:               datetime | None     = Field(alias="FechaPublicacion")
    awarded_at:                 datetime | None     = Field(alias="FechaAdjudicacion")
    estimated_awarded_at:       datetime | None     = Field(alias="FechaEstimadaAdjudicacion")
    physical_support_at:        datetime | None     = Field(alias="FechaSoporteFisico")
    evaluation_at:              datetime | None     = Field(alias="FechaTiempoEvaluacion")
    estimated_signed_at:        datetime | None     = Field(alias="FechaEstimadaFirma")
    user_dates:                 Any | None          = Field(alias="FechasUsuario")
    site_visit_at:              datetime | None     = Field(alias="FechaVisitaTerreno")
    antecedents_delivery_at:    datetime | None     = Field(alias="FechaEntregaAntecedentes")


class TenderItemRecord(BaseModel):
    correlative:    int        = Field(alias="Correlativo")
    product_code:   int        = Field(alias="CodigoProducto")
    category_code:  str        = Field(alias="CodigoCategoria")
    category:       str        = Field(alias="Categoria")
    product_name:   str        = Field(alias="NombreProducto")
    description:    str        = Field(alias="Descripcion")
    measure_unit:   str        = Field(alias="UnidadMedida")
    quantity:       float      = Field(alias="Cantidad")
    award:          Any | None = Field(alias="Adjudicacion")


class TenderItemsCollection(RootModel[list[TenderItemRecord]]): ...


class TenderItems(BaseModel):
    quantity: int                   = Field(alias="Cantidad")
    records:  TenderItemsCollection = Field(alias="Listado")


class TenderDetailsRecord(BaseModel):
    code:                           str                 = Field(alias="CodigoExterno")
    name:                           str                 = Field(alias="Nombre")
    status_code:                    int                 = Field(alias="CodigoEstado")
    description:                    str                 = Field(alias="Descripcion")
    closing_at:                     datetime | None     = Field(alias="FechaCierre")
    status:                         str                 = Field(alias="Estado")
    closing_days:                   int                 = Field(alias="DiasCierreLicitacion")
    informed:                       int                 = Field(alias="Informada")
    type_code:                      int                 = Field(alias="CodigoTipo")
    tender_type:                    str                 = Field(alias="Tipo")
    call_type:                      int                 = Field(alias="TipoConvocatoria")
    currency:                       str                 = Field(alias="Moneda")
    stages:                         int                 = Field(alias="Etapas")
    stages_status:                  int                 = Field(alias="EstadoEtapas")
    requires_review:                int                 = Field(alias="TomaRazon")
    offers_visible:                 int                 = Field(alias="EstadoPublicidadOfertas")
    offers_visible_reason:          str                 = Field(alias="JustificacionPublicidad")
    contract:                       int                 = Field(alias="Contrato")
    public_work:                    int                 = Field(alias="Obras")
    claims_number:                  int                 = Field(alias="CantidadReclamos")
    evaluation_time_unit:           int                 = Field(alias="UnidadTiempoEvaluacion")
    visit_address:                  str                 = Field(alias="DireccionVisita")
    delivery_address:               str                 = Field(alias="DireccionEntrega")
    estimation:                     int | None          = Field(alias="Estimacion")
    funding_source:                 str                 = Field(alias="FuenteFinanciamiento")
    amount_visibility:              int                 = Field(alias="VisibilidadMonto")
    estimated_amount:               float | None        = Field(alias="MontoEstimado")
    time:                           int | None          = Field(alias="Tiempo")
    time_unit:                      int                 = Field(alias="UnidadTiempo")
    mode:                           int                 = Field(alias="Modalidad")
    payment_type:                   int                 = Field(alias="TipoPago")
    payment_responsible_name:       str                 = Field(alias="NombreResponsablePago")
    payment_responsible_email:      str                 = Field(alias="EmailResponsablePago")
    contract_responsible_name:      str                 = Field(alias="NombreResponsableContrato")
    contract_responsible_email:     str                 = Field(alias="EmailResponsableContrato")
    contract_responsible_phone:     str                 = Field(alias="FonoResponsableContrato")
    hiring_ban:                     str                 = Field(alias="ProhibicionContratacion")
    subcontracting:                 int                 = Field(alias="SubContratacion")
    contract_duration_time_unit:    int                 = Field(alias="UnidadTiempoDuracionContrato")  # noqa: E501
    contract_duration_time:         int                 = Field(alias="TiempoDuracionContrato")
    contract_duration_type:         str                 = Field(alias="TipoDuracionContrato")
    amount_estimate_justification:  str                 = Field(alias="JustificacionMontoEstimado")
    contract_observation:           str | None          = Field(alias="ObservacionContract")
    term_extension:                 int                 = Field(alias="ExtensionPlazo")
    is_base_type:                   int                 = Field(alias="EsBaseTipo")
    tender_contract_time_unit:      int                 = Field(alias="UnidadTiempoContratoLicitacion")  # noqa: E501
    renewal_time_value:             int                 = Field(alias="ValorTiempoRenovacion")
    renewal_time_period:            str                 = Field(alias="PeriodoTiempoRenovacion")
    is_renewable:                   int                 = Field(alias="EsRenovable")
    bip_code:                       str | None          = Field(alias="CodigoBIP")
    award:                          Any | None          = Field(alias="Adjudicacion")
    dates:                          TenderDates         = Field(alias="Fechas")
    buyer:                          TenderBuyer         = Field(alias="Comprador")
    items:                          TenderItems         = Field(alias="Items")


class TenderDetailsCollection(RootModel[list[TenderDetailsRecord]]): ...


class TenderDetails(BaseModel):
    quantity:   int                     = Field(alias="Cantidad")
    created_at: datetime                = Field(alias="FechaCreacion")
    version:    str                     = Field(alias="Version")
    records:    TenderDetailsCollection = Field(alias="Listado")
