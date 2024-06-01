from datetime import date

from loguru import logger

from woningwaardering.stelsels.stelsel import Stelsel
from woningwaardering.stelsels import utils
from woningwaardering.vera.bvg.generated import (
    EenhedenEenheid,
)
from woningwaardering.vera.referentiedata import (
    Woningwaarderingstelsel,
)


class ZelfstandigeWoonruimten(Stelsel):
    def __init__(self, peildatum: date = date.today()) -> None:
        super().__init__(
            stelsel=Woningwaarderingstelsel.zelfstandige_woonruimten,
            peildatum=peildatum,
        )


if __name__ == "__main__":
    logger.enable("woningwaardering")

    zelfstandige_woonruimten = ZelfstandigeWoonruimten()
    file = open(
        "./tests/data/input/generiek/37101000032.json",
        "r+",
    )
    eenheid = EenhedenEenheid.model_validate_json(file.read())
    woningwaardering_resultaat = zelfstandige_woonruimten.bereken(eenheid)
    print(
        woningwaardering_resultaat.model_dump_json(
            by_alias=True, indent=2, exclude_none=True
        )
    )

    tabel = utils.naar_tabel(woningwaardering_resultaat)

    print(tabel)
