from datetime import UTC, datetime

from cl_forge.rest.market.schemas import TenderDetails


def test_tender_details_model_validates_nested_market_response():
    detail = {
        "Cantidad": 1,
        "FechaCreacion": "2026-04-17T00:20:15.4377723Z",
        "Version": "v1",
        "Listado": [
            {
                "CodigoExterno": "1057417-445-LP25",
                "Nombre": "COMPRA DE SERVICIOS TOMA E INFORME DE TAC",
                "CodigoEstado": 5,
                "Descripcion": (
                    "La presente licitación tiene como objeto la contratación "
                    "de servicios TAC."
                ),
                "FechaCierre": None,
                "Estado": "Publicada",
                "Comprador": {
                    "CodigoOrganismo": "7375",
                    "NombreOrganismo": (
                        "COMPLEJO ASISTENCIAL DR.VICTOR RIOS RUIZ"
                    ),
                    "RutUnidad": "61.607.301-K",
                    "CodigoUnidad": "1057417",
                    "NombreUnidad": "Bienes y Servicios",
                    "DireccionUnidad": "Av. Ricardo Vicuña N°147",
                    "ComunaUnidad": "Los Angeles",
                    "RegionUnidad": "Región del Biobío ",
                    "RutUsuario": "",
                    "CodigoUsuario": "1421191",
                    "NombreUsuario": "Karen Daniela Cid Burgos",
                    "CargoUsuario": "Profesional Administración de Contratos ",
                },
                "DiasCierreLicitacion": "20",
                "Informada": 0,
                "CodigoTipo": 1,
                "Tipo": "LP",
                "TipoConvocatoria": "1",
                "Moneda": "CLP",
                "Etapas": 1,
                "EstadoEtapas": "0",
                "TomaRazon": "0",
                "EstadoPublicidadOfertas": 1,
                "JustificacionPublicidad": "",
                "Contrato": "0",
                "Obras": "0",
                "CantidadReclamos": 875,
                "Fechas": {
                    "FechaCreacion": "2025-10-27T07:43:50.77",
                    "FechaCierre": "2026-05-06T15:30:00",
                    "FechaInicio": "2026-04-16T18:00:00",
                    "FechaFinal": "2026-04-19T18:00:00",
                    "FechaPubRespuestas": "2026-04-21T18:00:00",
                    "FechaActoAperturaTecnica": "2026-05-06T15:31:00",
                    "FechaActoAperturaEconomica": "2026-05-06T15:31:00",
                    "FechaPublicacion": "2026-04-16T10:56:06.94",
                    "FechaAdjudicacion": "2026-06-22T18:00:00",
                    "FechaEstimadaAdjudicacion": "2026-06-22T18:00:00",
                    "FechaSoporteFisico": None,
                    "FechaTiempoEvaluacion": None,
                    "FechaEstimadaFirma": None,
                    "FechasUsuario": None,
                    "FechaVisitaTerreno": None,
                    "FechaEntregaAntecedentes": None,
                },
                "UnidadTiempoEvaluacion": 1,
                "DireccionVisita": "",
                "DireccionEntrega": "",
                "Estimacion": 2,
                "FuenteFinanciamiento": (
                    "Complejo Asistencial Dr. Víctor Ríos Ruiz"
                ),
                "VisibilidadMonto": 0,
                "MontoEstimado": None,
                "Tiempo": "12",
                "UnidadTiempo": "1",
                "Modalidad": 1,
                "TipoPago": "1",
                "NombreResponsablePago": "Rodolfo Gonzalez Araneda",
                "EmailResponsablePago": "",
                "NombreResponsableContrato": "Fernando Cano San Martin",
                "EmailResponsableContrato": "",
                "FonoResponsableContrato": "",
                "ProhibicionContratacion": "",
                "SubContratacion": "0",
                "UnidadTiempoDuracionContrato": 4,
                "TiempoDuracionContrato": "12",
                "TipoDuracionContrato": " ",
                "JustificacionMontoEstimado": "",
                "ObservacionContract": None,
                "ExtensionPlazo": 0,
                "EsBaseTipo": 0,
                "UnidadTiempoContratoLicitacion": "2",
                "ValorTiempoRenovacion": "0",
                "PeriodoTiempoRenovacion": " ",
                "EsRenovable": 0,
                "CodigoBIP": None,
                "Adjudicacion": None,
                "Items": {
                    "Cantidad": 1,
                    "Listado": [
                        {
                            "Correlativo": 1,
                            "CodigoProducto": 85122201,
                            "CodigoCategoria": "85122200",
                            "Categoria": "Categoria",
                            "NombreProducto": "Exámenes médicos",
                            "Descripcion": "403001 Tomografía",
                            "UnidadMedida": "Unidad",
                            "Cantidad": 1.0,
                            "Adjudicacion": None,
                        }
                    ],
                },
            }
        ],
    }

    model = TenderDetails.model_validate(detail)

    assert model.quantity == 1
    assert model.created_at == datetime(
        2026, 4, 17, 0, 20, 15, 437772, tzinfo=UTC
    )
    assert model.entries[0].closing_days == 20
    assert model.entries[0].buyer.unit_code == 1_057_417
    assert model.entries[0].dates.closing_at == datetime(2026, 5, 6, 15, 30)
    assert model.entries[0].items.entries[0].category_code == "85122200"
    assert model.entries[0].items.entries[0].quantity == 1.0
    assert model.entries[0].is_renewable == 0
