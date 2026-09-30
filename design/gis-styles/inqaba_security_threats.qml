<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.40.0" styleCategories="Symbology">
  <renderer-v2 type="categorizedSymbol" attr="threat_level" symbollevels="0" enableorderby="0">
    <categories>
      <category symbol="0" value="CRITICAL THREAT" label="Critical Threat (CAS / Stoppage)" render="true"/>
      <category symbol="1" value="ELEVATED RISK" label="Elevated Risk (Sabotage / Vandalism)" render="true"/>
      <category symbol="2" value="NOMINAL / SECURE" label="Nominal / Secure Execution" render="true"/>
    </categories>
    <symbols>
      <!-- 0: CRITICAL THREAT -->
      <symbol type="marker" name="0" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleMarker" locked="0" enabled="1" pass="0">
          <prop k="color" v="220,38,38,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.6"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="size" v="3.8"/>
          <prop k="size_unit" v="MM"/>
          <prop k="shape" v="circle"/>
        </layer>
      </symbol>
      <!-- 1: ELEVATED RISK -->
      <symbol type="marker" name="1" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleMarker" locked="0" enabled="1" pass="0">
          <prop k="color" v="217,119,6,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.5"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="size" v="3.0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="shape" v="circle"/>
        </layer>
      </symbol>
      <!-- 2: NOMINAL / SECURE -->
      <symbol type="marker" name="2" alpha="1" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleMarker" locked="0" enabled="1" pass="0">
          <prop k="color" v="13,148,136,255"/>
          <prop k="outline_color" v="255,255,255,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.4"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="size" v="2.4"/>
          <prop k="size_unit" v="MM"/>
          <prop k="shape" v="circle"/>
        </layer>
      </symbol>
    </symbols>
  </renderer-v2>
</qgis>
