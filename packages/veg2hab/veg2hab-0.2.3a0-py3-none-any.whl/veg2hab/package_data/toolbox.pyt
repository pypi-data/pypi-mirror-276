# -*- coding: utf-8 -*-
from typing import Type, Union

import veg2hab.io.arcgis
import veg2hab.main
import veg2hab.constants
import logging

SUPPORTED_VERSIONS = ["0.1.0", "0.1.1", "0.2.1", "0.2.3a0"]

# this instantiates the arcgis interface and configures the logging
veg2hab.io.arcgis.ArcGISInterface.get_instance().instantiate_loggers()

class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "veg2hab"
        self.alias = "veg2hab toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool1, Tool2]


class BaseTool:
    def __init__(
        self,
        param_type: Union[
            Type[veg2hab.io.arcgis.ArcGISAccessDBInputs],
            Type[veg2hab.io.arcgis.ArcGISShapefileInputs],
        ],
    ) -> None:
        self.param_type = param_type
        self.label = param_type.label
        self.description = param_type.description

    def getParameterInfo(self):
        """Define the tool parameters."""
        return self.param_type.to_parameter_list()

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        # TODO: we could do some more validation here
        # and or make some parameters dependent on others
        # validate that the column exists
        # if parameters[0].altered:
        #     try:
        #         layer = parameters[0].valueAsText
        #         fields = [f.name for f in arcpy.ListFields(layer)]
        #         parameters[1].filter.list = fields
        #     except Exception as e:
        #         # hmm, dit doet het nog niet helemaal..
        #         logging.error(e)

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""

    def execute(self, parameters, messages):
        """The source code of the tool."""
        if veg2hab.__version__ not in SUPPORTED_VERSIONS:
            logging.warning(
                "Deze versie van de toolbox is niet getest met deze versie van de software.\n"
                "Gelieve de toolbox opnieuw toe te voegen aan ArcGIS, zie installatie instructies.\n"
                f"De locatie van toolbox.pyt is: {veg2hab.constants.TOOLBOX_PYT_PATH}"
            )

        input_params = self.param_type.from_parameter_list(parameters)
        veg2hab.main.run(input_params)

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""


class Tool1(BaseTool):
    def __init__(self):
        super().__init__(veg2hab.io.arcgis.ArcGISAccessDBInputs)


class Tool2(BaseTool):
    def __init__(self):
        super().__init__(veg2hab.io.arcgis.ArcGISShapefileInputs)
