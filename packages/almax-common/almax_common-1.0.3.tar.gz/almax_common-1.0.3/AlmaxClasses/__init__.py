from AlmaxClasses.Result import *;

from __future__ import annotations;

class Example:
    def __init__(self, moinvId: str):
        self.__Id = f"MOINV_{moinvId.strip("0")}";
        self.__Observations = [];
   
    @staticmethod
    def fromLine(line: list) -> Example:
        return Example(f"{line[3:5]}");
   
    @property
    def Id(self) -> str:
        return self.__Id;

    @property
    def Observations(self) -> list:
        return self.__Observations;

    @Observations.setter
    def Observations(self, value):
        self.__Observations = value;

    @property
    def LastObsID(self) -> str:
        return (len(self.__Observations) - 1);

    @classmethod
    def addObservation(self, line: str):
        newObs = f"{int(line[3:5])}";
        self.__Observations.append(newObs);

    @classmethod
    def CheckIfIdIsSame(self, line: str) -> bool:
        newCubo = Example.fromLine(line);
        return self.Id == newCubo.Id;