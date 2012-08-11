# UpdateGeoIP Plugin

__version__ = '1.3'
__author__  = 'PtitBigorneau www.ptitbigorneau.fr'

import b3
import gzip
import urllib
import urllib2
import time
import calendar
import b3.cron
import os

#--------------------------------------------------------------------------------------------------
class UpdategeoipPlugin(b3.plugin.Plugin):

    _adminPlugin = None
    _cronTab = None
    _updatetest = None

    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
      
        self._adminPlugin.registerCommand(self, 'updategeoip',self._updategeoiplevel, self.cmd_updategeoip, 'ugeoip')
        self._adminPlugin.registerCommand(self, 'verifgeoip',self._updategeoiplevel, self.cmd_verifgeoip, 'vgeoip')
      
        if self._cronTab:
        
            self.console.cron - self._cronTab

        self._cronTab = b3.cron.PluginCronTab(self, self.update, hour='*/1')
        self.console.cron + self._cronTab
   
    def onLoadConfig(self):
   
        self._adminPlugin.registerCommand(self, 'updategeoip',self._updategeoiplevel, self.cmd_updategeoip, 'ugeoip')
        self._adminPlugin.registerCommand(self, 'verifgeoip',self._updategeoiplevel, self.cmd_verifgeoip, 'vgeoip')
          
    def update(self):
        
        time_epoch = time.time() 
        time_struct = time.gmtime(time_epoch)
        date = time.strftime('%d', time_struct)
        mdate = int(date)
        
        if mdate != self._updateday:
      
            self._updatetest = None
      
        if (mdate == self._updateday) and (self._updatetest == None):
      
            req = urllib2.Request(self._geoipurl)

            try:
       
                handle = urllib2.urlopen(req)

            except IOError:
         
                self.error('Update GeoIP Error url')

            else:
         
                urllib.urlretrieve(self._geoipurl, self._geoippath + 'GeoIP.dat.gz')

                zfile = gzip.GzipFile(self._geoippath + 'GeoIP.dat.gz','rb')
                content = zfile.read()
                zfile.close()
                self.info('GeoIP.dat file has been updated')
                fichier = open(self._geoippath + 'GeoIP.dat', 'wb')
                fichier.write(content)
                fichier.close()
                self._updatetest = "ok"
          
    def cmd_updategeoip(self, data, client, cmd=None):
        
        """\
        updated GeoIP.dat file
        """

        req = urllib2.Request(self._geoipurl)

        try:
       
            handle = urllib2.urlopen(req)

        except IOError:

            client.message ('^1B3 can not access')
            client.message ('^5%s !'% (self._geoipurl))

        else:
          
            urllib.urlretrieve(self._geoipurl, self._geoippath + 'GeoIP.dat.gz')

            zfile = gzip.GzipFile(self._geoippath + 'GeoIP.dat.gz','rb')
            content = zfile.read()
            zfile.close()

            fichier = open(self._geoippath + 'GeoIP.dat', 'wb')
            fichier.write(content)
            fichier.close()
      
      
            client.message('^1GeoIP.dat ^3file has been updated')
         
    def cmd_verifgeoip(self, data, client, cmd=None):
        
        """  
        return the last modified time of the GeoIP.dat file
        """
        
        dategeoip = os.stat("%s" % (self._geoippath + 'GeoIP.dat'))[8]
        dategeoip = int(dategeoip)
        time_struct = time.localtime(dategeoip)
        dategeoip = time.strftime('%Y-%m-%d %H:%M', time_struct)
      
        client.message('^1GeoIP.dat ^5%s' %(dategeoip))

