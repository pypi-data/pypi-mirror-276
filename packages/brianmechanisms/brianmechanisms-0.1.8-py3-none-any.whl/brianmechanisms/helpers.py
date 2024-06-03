
import numpy as np

thetaRotations = {
    # add more values < -0.25
    "-0.1667": 38, # todo: check this value
    "-0.2":0,
    "-0.25":90,
    "-0.3333":45,
    "-0.5":90,
    "-2": 90,
    "-3":45,
    "-4":90,
    "-5":0,
    "-6":38, # todo: check this value
    # todo: add more values < -6
}

shapeParams={
    "1": {
        "name": "Straight Line",
        "options":[
            {
               "len_factor": 1,
                "speed_factor": -1,
            },
            {
                "len_factor": 4, # todo: check this value
                "speed_factor": -0.5,
                # "thetaMax": 180
                "thetaMax": 180-50
            },
        ]
    },
    "3":{
        "name": "Triangle",
        "options":[
            {
                "len_factor": 0.25,
                "speed_factor": -2
            },
            {
                "len_factor": 4, # todo: check this value
                "speed_factor": -0.5
            },
        ]
    },
    "4": {
        "name": "Square",
        "options":[
            {
                "len_factor": 0.135, # todo: check this value
                "speed_factor": -3
            },
            {
                "len_factor": 1/0.135,
                "speed_factor": -1/3
            },
        ]
    },
    # todo: add more shapes
}

class helpers:
    def __init__(self):
        pass

    @staticmethod
    def shapeParams(numSides):
        return shapeParams[f"{numSides}"] if f"{numSides}" in shapeParams else None
    @staticmethod
    def create2linksForBar(numBars=1, speed_factor=None, len_factor=None, numLinks=None, numSides=None, shapeOption=0, theta0=0):
        thetaMax = None
        if numSides is not None:
            shapeParam = helpers.shapeParams(numSides)
            if shapeParam is None:
                # throw error
                raise ValueError(f"Shape with {numSides} sides not found")
            len_factor = shapeParam["options"][shapeOption]["len_factor"]
            speed_factor = shapeParam["options"][shapeOption]["speed_factor"]
            thetaMax = shapeParam["options"][shapeOption]["thetaMax"] if "thetaMax" in shapeParam["options"][shapeOption] else None
        alphaBetLetters = [chr(i) for i in range(65, 65+numBars*2)]
        oddNumbers = [i for i in range(1, numBars*2+1, 2)]
        if thetaMax is None:
            if abs(speed_factor) < 1:
                thetaMax = 360/np.abs(speed_factor)
            else:
                thetaMax = 360
        
        links = []
        angle = thetaMax/numBars
        for i in range(1, numBars+1):
            link1 = {
                "points": {
                    f"O{i}": 0, f"A{i}":1
                },
                "speed": 1,
                "equation": "np.cos(x), np.sin(x)",
                "origin": "{0,0}",
                "theta0": angle*(i-1),
            }
            link2 = {
                "points": {
                    f"A{i}":0, f"B{i}":1
                },
                "len_factor": len_factor,
                "speed_factor": speed_factor,
                "speed_source": f"link1.speed",
                "equation": "np.cos(speed_factor * speed_source * x), np.sin(speed_factor * speed_source * x)",
                "origin": f"link{oddNumbers[i-1]}.A{i}",
                "theta0": angle*(i-1)+theta0,
                "output": f"B{i}"
            }
            links.append(link1)
            links.append(link2)
        linksTemplate = {}
        if numLinks is None:
            numLinks = numBars * 2
        for i in range(1, numLinks+1):
            linksTemplate[f"link{i}"] =links[i-1].copy()

        thetaRotationIndex = f"{speed_factor}" if speed_factor <-1 else f"{speed_factor:.4f}"
        while thetaRotationIndex[-1] == "0":
            thetaRotationIndex = thetaRotationIndex[:-1]
        if f"{thetaRotationIndex}" in thetaRotations:
            thetaRotation = thetaRotations[f"{thetaRotationIndex}"]
        else:
            thetaRotation = 0

        
        return linksTemplate, thetaMax, thetaRotation