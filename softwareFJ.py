import logging
import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from itertools import count
import tkinter as tkinter
from tkinter import messagebox, tkinter


#Se incluyen las excepciones personalizadas

# Permiten distinguir los errores del dominio de los errores generales de Python.
class SoftwareFJError(Exception):


class ClienteInvalidoError(SoftwareFJError):


class ServicioInvalidoError(SoftwareFJError):


class ParametroFaltanteError(SoftwareFJError):


class ServicioNoDisponibleError(SoftwareFJError):


class CalculoInconsistenteError(SoftwareFJError):


class OperacionNoPermitidaError(SoftwareFJError):

 
#El logger que es para los archivos de logs

# El archivo de registro se configura una sola vez para evitar duplicar mensajes.
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__))),"software_fj.log"

logger = logging.getLogger("software_fj")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    _h = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    _h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s" ))
    logger.addHandler(_h)

#Esta es la clase abstracta de las entidades generales

class EntidadBase(ABC):

# El contador compartido asigna identificadores consecutivos a todas las entidades.
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
# Estas expresiones regulares definen los formatos aceptados para el correo y el nombre.
_RE_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
_RE_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÚú]+([A-Za-zÁÉÍÓÚáéíóúÑñÚú]+)*$")


class Cliente(EntidadBase):
    def__init__(self, nombre, documento, correo, telefono):
        super().__init__()
        try:
            # La asignación mediante propiedades centraliza la validación de cada dato.
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
            # Rechaza valores vacíos antes de aplicar las reglas específicas de cada campo.
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

# Porcentaje de IVA usado por el método de cálculo de conveniencia.
IVA = 0.19 

# Clase base para los servicios; las subclases concretas definen sus reglas de uso
# y la forma de calcular el costo según la duración.
class Servicio(EntidadBase):
        """Abstraccion de un servicio ofrecido por softwareFJ. Cada servicio tiene un nombre, un precio base y un estado de disponibilidad."""

        def __init__(self, nombre, tarifa_base, disponible=True):
            super().__init__()
            # Se validan los datos comunes antes de guardar el servicio.
            if nombre is None or not str(nombre).strip():
                raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
            if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool) or tarifa_base <= 0:
                raise ServicioInvalidoError(f"Tarifa base invalida: {tarifa_base!r}")
            self.nombre = str(nombre).strip()
            self.tarifa_base = float(tarifa_base)
            self.disponible = bool(disponible)

            @property
            def nombre(self):
                return self._nombre
            
            @property
            def tarifa_base(self):
                return self._tarifa_base

            @property
            def disponible(self):
                return self._disponible
            
            def activar(self):
                # Habilita nuevamente el servicio para que pueda ser utilizado.
                self._disponible = True
            
            def desactivar(self):
                # Conserva el servicio, pero impide su uso mientras esté desactivado.
                self._disponible = False
            
            # Cada subclase debe proporcionar el costo antes de aplicar impuestos o descuentos.
            @abstractmethod
            def _costo_base(self, duracion: float) -> float:
                """Costo sin impuestos ni descuentos, según la duración del servicio."""
            
            # La descripción permite mostrar la información propia de cada tipo de servicio.
            @abstractmethod
            def describir(self) -> str:
                """Descripción específica del servicio."""

            # La implementación concreta decide qué duraciones son válidas para el servicio.
            @abstractmethod
            def validar_duracion(self, duracion: float) -> bool:
                """Valida los parámetros de uso; lanza ServicioNoDisponibleError si no es válido."""
            
            def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0):
                """variantes:
                calcular_costo(2)                                   -> Costo base
                calcular_costo(2, impuesto=0.19)                    -> con impuesto
                calcular_costo(2, impuesto=0.19, descuento=0.1)     -> con impuesto y descuento
                calcular_costo(2, descuento=0.1)                    -> solo descuento
                
                """

                try:
                    # Se comprueba disponibilidad y duración antes de calcular el importe.
                    self.verificar_disponible()
                    self.validar_parametros(duracion)
                    if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
                        raise CalculoInsconsistenteError(f"Impuesto debe estar entre 0 y 1")
                    # El descuento reduce el costo base y luego se aplica el impuesto.
                    total = self._costo_base(duracion) * (1 - descuento) * (1 + impuesto)
                    if total < 0:
                        raise CalculoInsconsistenteError(f"El costo calculado no es valido: {total}")
                    
                except (ServicioInvalidoError, ServicioNoDisponibleError, CalculoInsconsistenteError) as e:
                    logger.error("Error al calcular el costo de'%s': %s", self.nombre, e)
                    raise
                else:
                    logger.info("Costo '%s' (%s): %.2f", self.nombre, duracion, total)
                    return round(total, 2)
                finally:
                    logger.info("Cálculo de costo finalizado para '%s'", self.nombre)
            
            def calcular_costo_con_iva(self, duracion):
                """Variante de conveniencia: se aplica el IVA estandar."""
                return self.calcular_costo(duracion, impuesto=IVA)
            
            def verificar_disponible(self):
                # Centraliza la verificación para evitar cobrar por un servicio inactivo.
                if not self.disponible:
                    raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible actualmente.")
                
            def descripcion(self):
                # Reutiliza la descripción específica implementada por cada subclase.
                return self.describir()

            