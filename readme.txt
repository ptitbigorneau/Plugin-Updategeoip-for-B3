# updategeoip plugin
# Plugin for B3 (www.bigbrotherbot.com)
# www.ptitbigorneau.fr

updategeoip plugin (v1.4.1) for B3

Installation:

1. Place the updategeoip.py in your ../b3/extplugins and the 
updategeoip.ini in your ../b3/extplugins/conf folders.

2. Open updategeoip.ini

modify <set name="geoippath">/PATH/GeoIP/</set> for your config ex (<set name="geoippath">b3/extplugins/GeoIP/</set>

3. Open your B3.xml file (default in b3/conf) and add the next line in the
<plugins> section of the file:

<plugin name="updategeoip" config="@b3/extplugins/conf/updategeoip.ini"/>


