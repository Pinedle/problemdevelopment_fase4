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



#Esta es la clase abstracta del cliente

class Cliente(EntidadBase):



#Esta es la clase abstracta del servicio y los tres servicio especializados

class Servicio(EntidadBase):