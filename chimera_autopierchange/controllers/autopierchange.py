import time

from chimera.core.callback import callback
from chimera.core.chimeraobject import ChimeraObject
from chimera.core.constants import SYSTEM_CONFIG_DEFAULT_FILENAME
from chimera.core.manager import Manager
from chimera.core.systemconfig import SystemConfig
from chimera.interfaces.telescope import TelescopeStatus, TelescopePierSide
from chimera.util.coord import CoordUtil


class AutoPierChange(ChimeraObject):
    __config__ = {
        "site": "/Site/0",
        "telescope": "/Telescope/0",
        "dome": None,
        "ha_flip": 0,
        "check_interval": 2,  # seconds
        "chimera_config": SYSTEM_CONFIG_DEFAULT_FILENAME
    }

    def __init__(self):
        ChimeraObject.__init__(self)

    def __start__(self):

        self.setHz(1. / self["check_interval"])

        self.sysconfig = SystemConfig.fromFile(self['chimera_config'])

        self.localManager = Manager(self.sysconfig.chimera["host"], 9090)
        self.site = self.getManager().getProxy(self["site"])
        if self["dome"] is not None:
            self.dome = self.getManager().getProxy(self["dome"])
        else:
            self.dome = None
        self.pierPos = TelescopePierSide.UNKNOWN

        @callback(self.localManager)
        def slewComplete(position, status):
            if status == TelescopeStatus.OK:
                ha = CoordUtil.raToHa(position.ra, self.site.LST()).H
                if ha < self["ha_flip"]:
                    self.pierPos = TelescopePierSide.EAST
                else:
                    self.pierPos = TelescopePierSide.WEST
                self.log.debug("Telescope moved to %s, LST is %s, HA is %s.", str(self.pierPos),
                               str(self.site.LST()), str(position))

        self.telescope = self.getManager().getProxy(self["telescope"])
        self.telescope.slewComplete += slewComplete

    def control(self):
        if self.telescope.isTracking():
            if self.pierPos == TelescopePierSide.EAST:
                ha = CoordUtil.raToHa(self.telescope.getRa(), self.site.LST()).H
                if ha >= self["ha_flip"]:
                    self.log.debug("Flipping telescope pier...")
                    t0 = time.time()
                    self.telescope.slewToRaDec(self.telescope.getPositionRaDec())
                    if self.dome is not None:
                        self.log.debug("Syncing dome...")
                        self.dome.syncWithTel()
                    self.log.debug("Flipping telescope pier: took %3.2f s.", time.time() - t0)

        return True
