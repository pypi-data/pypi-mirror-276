from abc import ABC, abstractmethod
from functools import cached_property
from typing import Optional, Union

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseComposite, BaseModel
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="base_reducer.mod", bind="base_reducer")


class BaseReducer(BaseModel, ABC):
    """Classe de base pour implémenter un reducer.
    Il adopte le design pattern du constructeur:
    - il existe un produit "summary" à construire (ici un dictionnaire)
    - une méthode "reset" qui permet de recommencer le processus de construction
    - un ensemble de méthode qui permettent d'ajouter des caractéristiques au "summary"
    - une méthode "compute" qui exécute l'ensemble des étapes et renvoie le "summary"

    '/!\' Dans les classes héritant de BaseReducer,
    il est impératif de détailler au niveau de cette docstring principale
    le schéma du dictionnaire de résumé issu de la méthode "compute".
    """

    data: dict = {}
    geo_id: Optional[str] = None
    reduction: Optional[dict] = None
    composite: Optional[BaseComposite] = None

    @cached_property
    def composite_data(self) -> Optional[Union[xr.DataArray, xr.Dataset]]:
        return self.composite.compute(geo_id=self.geo_id, force=True)

    @abstractmethod
    def _compute(self) -> dict:
        """
        Make computation and returns the reduced data.

        Returns:
            dict: Reduced data
        """

    def compute(self) -> dict:
        """Méthode permettant d'exécuter toutes les étapes de construction

        Args:
            compo (Composite): Composant sur lequel on se base pour produire le texte
        Returns:
            dict: Dictionnaire résumant les infos contenues dans le risk_component
        """
        self.reduction = {}
        self.reduction = self._compute()

        self.post_process()

        return self.reduction

    def post_process(self):
        """Make a post-process operation in the reduction."""
