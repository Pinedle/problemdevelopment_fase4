import logging
import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from itertools import count
import tkinter as tkinter
from tkinter import messagebox, tkinter


#Se incluyen las excepciones personalizadas

class SoftwareFJError(Exception):


class ClienteInvalidoError(SoftwareFJError):


class ServicioInvalidoError(SoftwareFJError):


class ParametroFaltanteError(SoftwareFJError):


class ServicioNoDisponibleError(SoftwareFJError):


class CalculoInconsistenteError(SoftwareFJError):


class OperacionNoPermitidaError(SoftwareFJError):

 
#El logger que es para los archivos de logs

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__))),"software_fj.log"

logger = logging.getLogger("software_fj")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    _h = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    _h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s" ))
    logger.addHandler(_h)

#Esta es la clase abstracta de las entidades generales

class EntidadBase(ABC):

_contador_id = count(1)

def __init__(self)
    self._id = next(EntidadBase._contador)
    self._fecha_creacion = datetime.now()

@property
def id(self) -> int:
    return self._id

@property
def fecha_creacion(self) -> datetime:
    return self._fecha_creacion

@abstractmethod
def descripcion(self) -> str:
    """En la entidad cada una de ellas se  debe describir a sí misma, por lo que este método es abstracto y debe ser implementado en las subclases."""

def __str__(self) -> str:
    return f"[{self.__class__.__name__} #{self._id}] {self.descripcion()}"


#Esta es la clase abstracta del cliente
_RE_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
_RE_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÚú]+([A-Za-zÁÉÍÓÚáéíóúÑñÚú]+)*$")


class Cliente(EntidadBase):
    def__init__(self, nombre, documento, correo, telefono):
        super().__init__()
        try:
            self.nombre = nombre
            self.documento = documento
            self.correo = correo
            self.telefono = telefono
        except clienteInvalidoError as e:
            logger.error("Fallo al crear el cliente: %s", e)
            raise
        else:
            logger.info("Cliente creado exitosamente: %s (Doc: %s)", self.nombre, self.documento)
        
        @staticmethod
        def _requerido(valor, campo):
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                raise ParametroFaltanteError(f"El campo '{campo}' es obligatorio.")
            return valor

        @property
        def nombre(self):
            return self._nombre
        
        @nombre.setter
        def nombre(self, valor):
           try:
                valor = self._requerido(valor, "nombre")
                if not isinstance(valor, str) or not _RE_NOMBRE.match(valor.strip()) or len(valor.strip()) < 3:
                    raise valueError(f"Nombre invalido: {valor!r}")
            except (ParametroFaltanteError, ValueError) as e:
               raise ClienteInvalidoError(f"Nombre del cliente invalido") from e
            self._nombre = valor.strip().title()

        @property
        def documento(self):
            return self._documento
        @documento.setter
        def documento(self, valor):
            try:
                valor = str(self._requerido(valor, "documento")).strip()
                if not valor.isdigit() or not 6 <= len(valor) <= 12:
                    raise ValueError(f"Documento debe tener entre 6 y 12 dígitos: {valor!r}")
            except (ParametroFaltanteError, ValueError) as e:
                raise ClienteInvalidoError(f"Documento del cliente invalido") from e
            self._documento = valor
        
        @property
        def correo(self):
            return self._correo

        @correo.setter
        def correo(self, valor):
            try:
                valor = self._requerido(valor, "correo")
                if not isinstance(valor, str) or not _RE_CORREO.match(valor.strip()):
                    raise ValueError(f"Formato de correo invalido: {valor!r}")
            except (ParametroFaltanteError, ValueError) as e:
                raise ClienteInvalidoError(f"Correo del cliente invalido") from e
            self._correo = valor.lower()
        
        @property
        def telefono(self):
            return self._telefono
        
        @telefono.setter
        def telefono(self, valor):
            try:
                valor = str(self._requerido(valor, "telefono")).strip()
                if not valor.isdigit() or len(valor) != 10:
                    raise ValueError(f"Telefono debe tener 10 dígitos: {valor!r}")
            except (ParametroFaltanteError, ValueError) as e:
                raise ClienteInvalidoError(f"Telefono del cliente invalido") from e
            self._telefono = valor

        def descripcion(self) -> str:
            return f"{self.nombre} | Doc: {self.documento} | Correo: {self.correo} | Tel: {self.telefono}"

#Esta es la clase abstracta del servicio y los tres servicio especializados

class Servicio(EntidadBase):