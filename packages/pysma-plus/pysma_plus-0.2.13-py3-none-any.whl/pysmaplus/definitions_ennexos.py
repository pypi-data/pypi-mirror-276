"""
Definition for all enneoxOS senosrs 
"""

from .const import Identifier, SMATagList
from .sensor import Sensor

ennexosSensorProfiles = {
    "Sunny Tripower X ": [
        Sensor("Coolsys.Inverter.TmpVal.1", Identifier.temp_a, factor=1, unit="°C"),
        Sensor("Coolsys.Inverter.TmpVal.2", Identifier.temp_b, factor=1, unit="°C"),
        Sensor("Coolsys.Inverter.TmpVal.3", Identifier.temp_c, factor=1, unit="°C"),
        Sensor("DcMs.Amp.1", Identifier.pv_current_a, factor=1, unit="A"),
        Sensor("DcMs.Amp.2", Identifier.pv_current_b, factor=1, unit="A"),
        Sensor("DcMs.Amp.3", Identifier.pv_current_c, factor=1, unit="A"),
        Sensor("DcMs.TotDcEnCntWh.1", None),  # Energy released by string [A]
        Sensor("DcMs.TotDcEnCntWh.2", None, factor=1, unit=None),
        Sensor("DcMs.TotDcEnCntWh.3", None, factor=1, unit=None),
        Sensor("DcMs.Vol.1", Identifier.pv_voltage_a, factor=1, unit="V"),
        Sensor("DcMs.Vol.2", Identifier.pv_voltage_b, factor=1, unit="V"),
        Sensor("DcMs.Vol.3", Identifier.pv_voltage_c, factor=1, unit="V"),
        Sensor("DcMs.Watt.1", Identifier.pv_power_a, factor=1, unit="W"),
        Sensor("DcMs.Watt.2", Identifier.pv_power_b, factor=1, unit="W"),
        Sensor("DcMs.Watt.3", Identifier.pv_power_c, factor=1, unit="W"),
        Sensor("GridGuard.Cntry", None, factor=1, unit=None),  # Country standard set
        Sensor("GridMs.A.phsA", Identifier.current_l1, factor=1, unit="A"),
        Sensor("GridMs.A.phsB", Identifier.current_l2, factor=1, unit="A"),
        Sensor("GridMs.A.phsC", Identifier.current_l3, factor=1, unit="A"),
        Sensor("GridMs.GriTyp", None, factor=1, unit=None),  # Measurement.GridMs.GriTyp
        Sensor("GridMs.Hz", Identifier.frequency, factor=1, unit="Hz"),
        Sensor("GridMs.PhV.phsA", Identifier.voltage_l1, factor=1, unit="V"),
        Sensor(
            "GridMs.PhV.phsA2B", None, factor=1, unit=None
        ),  # Grid voltage phase L1 against L2
        Sensor("GridMs.PhV.phsB", Identifier.voltage_l2, factor=1, unit="V"),
        Sensor(
            "GridMs.PhV.phsB2C", None, factor=1, unit=None
        ),  # Grid voltage phase L2 against L3
        Sensor("GridMs.PhV.phsC", Identifier.voltage_l3, factor=1, unit="V"),
        Sensor(
            "GridMs.PhV.phsC2A", None, factor=1, unit=None
        ),  # Grid voltage phase L3 against L1
        Sensor("GridMs.TotA", Identifier.current_total, factor=1, unit="A"),
        Sensor(
            "GridMs.TotPFEEI", None, factor=1, unit=None
        ),  # EEI displacement power factor
        Sensor(
            "GridMs.TotPFExt", None, factor=1, unit=None
        ),  # Excitation type of cos φ
        Sensor(
            "GridMs.TotPFPrc", None, factor=1, unit=None
        ),  # Displacement power factor
        Sensor("GridMs.TotVA", Identifier.grid_apparent_power, factor=1, unit="VA"),
        Sensor("GridMs.TotVAr", Identifier.grid_reactive_power, factor=1, unit="var"),
        Sensor("GridMs.TotW", Identifier.grid_power, factor=1, unit="W"),
        Sensor("GridMs.TotW.Pv", Identifier.pv_power, factor=1, unit="W"),
        Sensor(
            "GridMs.VA.phsA", Identifier.grid_apparent_power_l1, factor=1, unit="VA"
        ),
        Sensor(
            "GridMs.VA.phsB", Identifier.grid_apparent_power_l2, factor=1, unit="VA"
        ),
        Sensor(
            "GridMs.VA.phsC", Identifier.grid_apparent_power_l3, factor=1, unit="VA"
        ),
        Sensor(
            "GridMs.VAr.phsA", Identifier.grid_reactive_power_l1, factor=1, unit="var"
        ),
        Sensor(
            "GridMs.VAr.phsB", Identifier.grid_reactive_power_l2, factor=1, unit="var"
        ),
        Sensor(
            "GridMs.VAr.phsC", Identifier.grid_reactive_power_l3, factor=1, unit="var"
        ),
        Sensor("GridMs.W.phsA", Identifier.power_l1, factor=1, unit="W"),
        Sensor("GridMs.W.phsB", Identifier.power_l2, factor=1, unit="W"),
        Sensor("GridMs.W.phsC", Identifier.power_l3, factor=1, unit="W"),
        Sensor("InOut.GI1", None, factor=1, unit=None),  # codespell:ignore
        Sensor("Inverter.VArModCfg.PFCtlVolCfg.Stt", None, factor=1, unit=None),
        Sensor(
            "Isolation.FltA",
            Identifier.insulation_residual_current,
            factor=1000,
            unit="mA",
        ),
        Sensor(
            "Isolation.LeakRis", None, factor=1, unit="kOhm"
        ),  # TODO "pv_isolation_resistance"
        Sensor("Metering.TotFeedTms", None),
        Sensor("Metering.TotOpTms", None),
        Sensor("Metering.TotWhOut", Identifier.total_yield, factor=1000, unit="kWh"),
        Sensor(
            "Metering.TotWhOut.Pv", Identifier.pv_gen_meter, factor=1000, unit="kWh"
        ),
        Sensor("Operation.BckStt", None, factor=1, unit=None),
        Sensor("Operation.DrtStt", None, factor=1, unit=None),
        Sensor("Operation.Evt.Dsc", None, factor=1, unit=None),
        Sensor("Operation.Evt.EvtNo", None, factor=1, unit=None),
        Sensor("Operation.Evt.Msg", None, factor=1, unit=None),
        Sensor("Operation.EvtCntIstl", None, factor=1, unit=None),
        Sensor("Operation.EvtCntUsr", None, factor=1, unit=None),
        Sensor("Operation.GriSwCnt", None, factor=1, unit=None),
        Sensor(
            "Operation.GriSwStt",
            Identifier.grid_relay_status,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor(
            "Operation.Health",
            Identifier.status,
            factor=1,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor("Operation.HealthStt.Alm", None, factor=1, unit=None),
        Sensor("Operation.HealthStt.Ok", None, factor=1, unit=None),
        Sensor("Operation.HealthStt.Wrn", None, factor=1, unit=None),
        Sensor(
            "Operation.OpStt",
            Identifier.operating_status_genereal,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor("Operation.PvGriConn", None, factor=1, unit=None),
        Sensor("Operation.RstrLokStt", None, factor=1, unit=None),
        Sensor("Operation.RunStt", None, factor=1, unit=None),
        Sensor("Operation.StandbyStt", None, factor=1, unit=None),
        Sensor("Operation.VArCtl.VArModAct", None, factor=1, unit=None),
        Sensor("Operation.VArCtl.VArModStt", None, factor=1, unit=None),
        Sensor("Operation.WMaxLimSrc", None, factor=1, unit=None),
        Sensor("Operation.WMinLimSrc", None, factor=1, unit=None),
        Sensor("PvGen.PvW", None, factor=1, unit=None),  #  PV generation power
        Sensor(
            "PvGen.PvWh", None, factor=1, unit=None
        ),  # Meter count and PV gen. meter
        Sensor(
            "Spdwr.ComSocA.Stt", None, factor=1, unit=None
        ),  # Speedwire connection status of SMACOM A
        Sensor(
            "SunSpecSig.SunSpecTx.1", None, factor=1, unit=None
        ),  # SunSpec life sign [1]
        Sensor("Upd.Stt", None, factor=1, unit=None),
        Sensor(
            "WebConn.Stt", None, factor=1, unit=None
        ),  #  Status of the Webconnect functionality
        Sensor("Wl.AcqStt", None, factor=1, unit=None),  # Status of WiFi scan
        Sensor("Wl.AntMod", None, factor=1, unit=None),  #  WiFi antenna type
        Sensor("Wl.ConnStt", None, factor=1, unit=None),  # WiFi connection status
        Sensor(
            "Wl.SigPwr", None, factor=1, unit=None
        ),  # Signal strength of the selected network
        Sensor(
            "Wl.SoftAcsConnStt", None, factor=1, unit=None
        ),  # Soft Access Point status
        Sensor(
            "Setpoint.PlantControl.InOut.GO1",  # codespell:ignore
            None,
            factor=1,
            unit=None,
        ),
        Sensor("Inverter.WMax", Identifier.inverter_power_limit, factor=1, unit="W"),
    ],
    "^(SMA EV Charger |EVC22-3AC-10)": [
        Sensor("ChaSess.WhIn", None, factor=1, unit=None),  # charging_session_energy
        Sensor(
            "Chrg.ModSw", None, factor=1, unit=None, mapper=SMATagList
        ),  # position_of_rotary_switch 4950 or 4718
        Sensor(
            "GridMs.A.phsA", Identifier.current_l1, factor=1, unit="A"
        ),  # Netzstrom Phase L1
        Sensor("GridMs.A.phsB", Identifier.current_l2, factor=1, unit="A"),
        Sensor("GridMs.A.phsC", Identifier.current_l3, factor=1, unit="A"),
        Sensor("GridMs.Hz", Identifier.frequency, factor=1, unit="Hz"),
        Sensor(
            "GridMs.PhV.phsA", Identifier.voltage_l1, factor=1, unit="V"
        ),  # Netzspannung Phase L1
        Sensor("GridMs.PhV.phsB", Identifier.voltage_l2, factor=1, unit="V"),
        Sensor("GridMs.PhV.phsC", Identifier.voltage_l3, factor=1, unit="V"),
        Sensor("GridMs.TotPF", None, factor=1, unit=None),
        Sensor("GridMs.TotVA", Identifier.grid_apparent_power, factor=1, unit="VA"),
        Sensor("GridMs.TotVAr", Identifier.grid_reactive_power, factor=1, unit="var"),
        Sensor("InOut.GI1", None, factor=1, unit=None),  # codespell:ignore
        Sensor(
            "Metering.GridMs.TotWIn",
            Identifier.metering_power_absorbed,
            factor=1,
            unit="W",
        ),  #
        Sensor(
            "Metering.GridMs.TotWIn.ChaSta", None, factor=1, unit=None
        ),  # same as Metering.GridMs.TotWIn
        Sensor(
            "Metering.GridMs.TotWhIn",
            Identifier.metering_total_absorbed,
            factor=1000,
            unit="kWh",
        ),  # charging_station_meter_reading
        Sensor(
            "Metering.GridMs.TotWhIn.ChaSta", None, factor=1, unit=None
        ),  # same as Metering.GridMs.TotWhIn
        Sensor(
            "Operation.EVeh.ChaStt",
            Identifier.operating_status,
            factor=1,
            unit=None,
            mapper=SMATagList,
        ),  # charging_session_status
        Sensor(
            "Operation.EVeh.Health",
            Identifier.status,
            factor=1,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor("Operation.Evt.Msg", None, factor=1, unit=None),
        Sensor("Operation.Health", None, factor=1, unit=None),  # same as EVeh.Health?
        Sensor("Operation.WMaxLimNom", None, factor=1, unit=None),
        Sensor("Operation.WMaxLimSrc", None, factor=1, unit=None),
        Sensor("Wl.AcqStt", None, factor=1, unit=None),
        Sensor("Wl.ConnStt", None, factor=1, unit=None),
        Sensor("Wl.SigPwr", None, factor=1, unit=None),
        Sensor("Wl.SoftAcsConnStt", None, factor=1, unit=None),
    ],
    "Sunny Boy Smart Energy ": [
        Sensor("Coolsys.Inverter.TmpVal.1", Identifier.temp_a, factor=1, unit="°C"),
        Sensor("DcMs.Amp.1", Identifier.pv_current_a, factor=1, unit="A"),
        Sensor("DcMs.Amp.2", Identifier.pv_current_b, factor=1, unit="A"),
        Sensor("DcMs.Amp.3", Identifier.pv_current_c, factor=1, unit="A"),
        Sensor("DcMs.TotDcEnCntWh.1", None),  # Energy released by string [A]
        Sensor("DcMs.TotDcEnCntWh.2", None, factor=1, unit=None),
        Sensor("DcMs.TotDcEnCntWh.3", None, factor=1, unit=None),
        Sensor("DcMs.Vol.1", Identifier.pv_voltage_a, factor=1, unit="V"),
        Sensor("DcMs.Vol.2", Identifier.pv_voltage_b, factor=1, unit="V"),
        Sensor("DcMs.Vol.3", Identifier.pv_voltage_c, factor=1, unit="V"),
        Sensor("DcMs.Watt.1", Identifier.pv_power_a, factor=1, unit="W"),
        Sensor("DcMs.Watt.2", Identifier.pv_power_b, factor=1, unit="W"),
        Sensor("DcMs.Watt.3", Identifier.pv_power_c, factor=1, unit="W"),
        Sensor("GridGuard.Cntry", None, factor=1, unit=None),  # Country standard set
        Sensor("GridMs.A.phsA", Identifier.current_l1, factor=1, unit="A"),
        Sensor(
            "GridMs.A.phsA", Identifier.current_l1, factor=1, unit="A"
        ),  # Netzstrom Phase L1
        Sensor("GridMs.GriTyp", None, factor=1, unit=None),  # Measurement.GridMs.GriTyp
        Sensor("GridMs.Hz", Identifier.frequency, factor=1, unit="Hz"),
        Sensor(
            "GridMs.PhV.phsA2B", None, factor=1, unit=None
        ),  # Grid voltage phase L1 against L2
        Sensor("GridMs.PhV.phsA", Identifier.voltage_l1, factor=1, unit="V"),
        Sensor("GridMs.TotA", Identifier.current_total, factor=1, unit="A"),
        Sensor(
            "GridMs.TotPFEEI", None, factor=1, unit=None
        ),  # EEI displacement power factor
        Sensor(
            "GridMs.TotPFExt", None, factor=1, unit=None
        ),  # Excitation type of cos φ
        Sensor(
            "GridMs.TotPFPrc", None, factor=1, unit=None
        ),  # Displacement power factor
        Sensor("GridMs.TotVA", Identifier.grid_apparent_power, factor=1, unit="VA"),
        Sensor("GridMs.TotVAr", Identifier.grid_reactive_power, factor=1, unit="var"),
        Sensor("GridMs.TotW", Identifier.grid_power, factor=1, unit="W"),
        Sensor("GridMs.TotW.Pv", Identifier.pv_power, factor=1, unit="W"),
        Sensor(
            "GridMs.VA.phsA", Identifier.grid_apparent_power_l1, factor=1, unit="VA"
        ),
        Sensor(
            "GridMs.VAr.phsA", Identifier.grid_reactive_power_l1, factor=1, unit="var"
        ),
        Sensor("GridMs.W.phsA", Identifier.power_l1, factor=1, unit="W"),
        Sensor("InOut.GI1", None, factor=1, unit=None),  # codespell:ignore
        Sensor("Inverter.VArModCfg.PFCtlVolCfg.Stt", None, factor=1, unit=None),
        Sensor(
            "Isolation.FltA",
            Identifier.insulation_residual_current,
            factor=1000,
            unit="mA",
        ),
        Sensor(
            "Isolation.LeakRis", None, factor=1, unit="kOhm"
        ),  # TODO "pv_isolation_resistance"
        Sensor(
            "Metering.GridMs.TotWhIn.ChaSta", None, factor=1, unit=None
        ),  # same as Metering.GridMs.TotWhIn
        Sensor(
            "Metering.GridMs.TotWhIn",
            Identifier.metering_total_absorbed,
            factor=1000,
            unit="kWh",
        ),  # charging_station_meter_reading
        Sensor(
            "Metering.GridMs.TotWIn.ChaSta", None, factor=1, unit=None
        ),  # same as Metering.GridMs.TotWIn
        Sensor(
            "Metering.GridMs.TotWIn",
            Identifier.metering_power_absorbed,
            factor=1,
            unit="W",
        ),  #
        Sensor("Metering.TotFeedTms", None),
        Sensor("Metering.TotOpTms", None),
        Sensor("Metering.TotWhOut", Identifier.total_yield, factor=1000, unit="kWh"),
        Sensor(
            "Metering.TotWhOut.Pv", Identifier.pv_gen_meter, factor=1000, unit="kWh"
        ),
        Sensor("Operation.BckStt", None, factor=1, unit=None),
        Sensor("Operation.DrtStt", None, factor=1, unit=None),
        Sensor("Operation.EvtCntIstl", None, factor=1, unit=None),
        Sensor("Operation.EvtCntUsr", None, factor=1, unit=None),
        Sensor("Operation.Evt.Dsc", None, factor=1, unit=None),
        Sensor("Operation.Evt.Msg", None, factor=1, unit=None),
        Sensor("Operation.GriSwCnt", None, factor=1, unit=None),
        Sensor(
            "Operation.GriSwStt",
            Identifier.grid_relay_status,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor(
            "Operation.Health",
            Identifier.status,
            factor=1,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor("Operation.HealthStt.Alm", None, factor=1, unit=None),
        Sensor("Operation.HealthStt.Ok", None, factor=1, unit=None),
        Sensor("Operation.HealthStt.Wrn", None, factor=1, unit=None),
        Sensor(
            "Operation.OpStt",
            Identifier.operating_status_genereal,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor("Operation.PvGriConn", None, factor=1, unit=None),
        Sensor("Operation.RstrLokStt", None, factor=1, unit=None),
        Sensor("Operation.RunStt", None, factor=1, unit=None),
        Sensor("Operation.StandbyStt", None, factor=1, unit=None),
        Sensor("Operation.VArCtl.VArModAct", None, factor=1, unit=None),
        Sensor("Operation.WMaxLimSrc", None, factor=1, unit=None),
        Sensor(
            "PvGen.PvWh", None, factor=1, unit=None
        ),  # Meter count and PV gen. meter
        Sensor("PvGen.PvW", None, factor=1, unit=None),  #  PV generation power
        Sensor(
            "Setpoint.PlantControl.InOut.GO1",  # codespell:ignore
            None,
            factor=1,
            unit=None,
        ),
        Sensor(
            "Spdwr.ComSocA.Stt", None, factor=1, unit=None
        ),  # Speedwire connection status of SMACOM A
        Sensor(
            "SunSpecSig.SunSpecTx.1", None, factor=1, unit=None
        ),  # SunSpec life sign [1]
        Sensor("Upd.Stt", None, factor=1, unit=None),
        Sensor(
            "WebConn.Stt", None, factor=1, unit=None
        ),  #  Status of the Webconnect functionality
        Sensor("Wl.AcqStt", None, factor=1, unit=None),
        Sensor("Wl.AntMod", None, factor=1, unit=None),  #  WiFi antenna type
        Sensor("Wl.ConnStt", None, factor=1, unit=None),
        Sensor("Wl.SigPwr", None, factor=1, unit=None),
        Sensor("Wl.SoftAcsConnStt", None, factor=1, unit=None),
        Sensor("Bat.Amp.1", None, factor=1, unit=None),
        Sensor("Bat.ChaSttArr.1", None, factor=1, unit=None),
        Sensor("Bat.Diag.VolMax.1", None, factor=1, unit=None),
        Sensor("Bat.OpTms.1", None, factor=1, unit=None),  #### Tot. battery runtime
        Sensor("Bat.Vol.1", None, factor=1, unit=None),
        Sensor("BatChrg.BatChrg", None, factor=1, unit=None),  #### Battery charge
        Sensor("BatChrg.BatChrgArr.1", None, factor=1, unit=None),  ####
        Sensor(
            "BatChrg.CurBatChaArr.1", None, factor=1, unit=None
        ),  ### Present battery charge
        Sensor("BatDsch.BatDsch", None, factor=1, unit=None),  ###
        Sensor("BatDsch.BatDschArr.1", None, factor=1, unit=None),  ####
        Sensor("BatDsch.CurBatDschArr.1", None, factor=1, unit=None),
        Sensor("DcMs.TotDcEnCntWh.1", None, factor=1, unit=None),
        Sensor("DcMs.TotDcEnCntWh.2", None, factor=1, unit=None),
        Sensor("DcMs.TotDcEnCntWh.3", None, factor=1, unit=None),
        Sensor("EpsMs.Amp", None, factor=1, unit=None),  # Emergency power measurements
        Sensor("EpsMs.Vol", None, factor=1, unit=None),  # Emergency power measurements
        Sensor("EpsMs.Watt", None, factor=1, unit=None),  # Emergency power measurements
        Sensor("GridGuard.Cntry", None, factor=1, unit=None),
        Sensor("GridMs.GriTyp", None, factor=1, unit=None),
        Sensor("GridMs.TotPFEEI", None, factor=1, unit=None),
        Sensor("GridMs.TotPFExt", None, factor=1, unit=None),
        Sensor("GridMs.TotPFPrc", None, factor=1, unit=None),
        Sensor("InOut.GI1", None, factor=1, unit=None),  # codespell:ignore
        Sensor("InOut.GO1", None, factor=1, unit=None),  # codespell:ignore
        Sensor("Inverter.VArModCfg.PFCtlVolCfg.Stt", None, factor=1, unit=None),
        Sensor("Isolation.LeakRis", None, factor=1, unit=None),
        Sensor("Metering.GridMs.TotWhIn.Bat", None, factor=1, unit=None),
        Sensor("Metering.GridMs.TotWhOut.Bat", None, factor=1, unit=None),
        Sensor("Metering.TotFeedTms", None, factor=1, unit=None),
        Sensor("Metering.TotOpTms", None, factor=1, unit=None),
        Sensor("Metering.TotWhIn", None, factor=1, unit=None),
        Sensor("Operation.Bat.Health", None, factor=1, unit=None),
        Sensor("Operation.BckStt", None, factor=1, unit=None),
        Sensor("Operation.DrtStt", None, factor=1, unit=None),
        Sensor("Operation.Evt.Dsc", None, factor=1, unit=None),
        Sensor("Operation.Evt.Msg", None, factor=1, unit=None),
        Sensor("Operation.EvtCntIstl", None, factor=1, unit=None),
        Sensor("Operation.EvtCntUsr", None, factor=1, unit=None),
        Sensor("Operation.GriSwCnt", None, factor=1, unit=None),
        Sensor("Operation.HealthStt.Alm", None, factor=1, unit=None),
        Sensor("Operation.HealthStt.Ok", None, factor=1, unit=None),
        Sensor("Operation.HealthStt.Wrn", None, factor=1, unit=None),
        Sensor("Operation.PvGriConn", None, factor=1, unit=None),
        Sensor("Operation.RstrLokStt", None, factor=1, unit=None),
        Sensor("Operation.RunStt", None, factor=1, unit=None),
        Sensor("Operation.StandbyStt", None, factor=1, unit=None),
        Sensor("Operation.VArCtl.VArModAct", None, factor=1, unit=None),
        Sensor("Operation.VArCtl.VArModStt", None, factor=1, unit=None),
        Sensor("Operation.WMaxLimSrc", None, factor=1, unit=None),
        Sensor("Operation.WMinLimSrc", None, factor=1, unit=None),
        Sensor("Portal.EnnexOS.ConnStt", None, factor=1, unit=None),
        Sensor("PvGen.PvW", None, factor=1, unit=None),
        Sensor("PvGen.PvWh", None, factor=1, unit=None),
        Sensor("Spdwr.ComSocA.Stt", None, factor=1, unit=None),
        Sensor("SunSpecSig.SunSpecTx.1", None, factor=1, unit=None),
        Sensor("Upd.Stt", None, factor=1, unit=None),
        Sensor("WebConn.Stt", None, factor=1, unit=None),
        Sensor("Wl.AcqStt", None, factor=1, unit=None),
        Sensor("Wl.AntMod", None, factor=1, unit=None),
        Sensor("Wl.ConnStt", None, factor=1, unit=None),
        Sensor("Wl.SigPwr", None, factor=1, unit=None),
        Sensor("Wl.SoftAcsConnStt", None, factor=1, unit=None),
        Sensor("Setpoint.PlantControl.CmpBMS.OpMod.1", None, factor=1, unit=None),
        Sensor("Metering.GridMs.TotWhIn.Bat", None, factor=1, unit=None),
        Sensor("Metering.GridMs.TotWhOut.Bat", None, factor=1, unit=None),
    ],
    "EDMM-10": [
        Sensor(
            "Operation.Health",
            Identifier.status,
            factor=1,
            unit=None,
            mapper=SMATagList,
        ),
        Sensor("DevUpd.IsOn", None, factor=1, unit=None),
        Sensor("FTPPush.IsOn", None, factor=1, unit=None),
        Sensor("FTPPush.Login", None, factor=1, unit=None),
        Sensor("FTPPush.Port", None, factor=1, unit=None),
        Sensor("FTPPush.Pwd", None, factor=1, unit=None),
        Sensor("FTPPush.RemStoLcn", None, factor=1, unit=None),
        Sensor("FTPPush.Srv", None, factor=1, unit=None),
        Sensor("FTPPush.UpldCyc", None, factor=1, unit=None),
        Sensor("InOut.GI1", None, factor=1, unit=None),  # codespell:ignore
        Sensor("Nameplate.CmpMain.HwRev", None, factor=1, unit=None),
        Sensor("Nameplate.CmpMain.Rev", None, factor=1, unit=None),
        Sensor("Nameplate.CmpOS.SwRev", None, factor=1, unit=None),
        Sensor("Nameplate.Location", None, factor=1, unit=None),
        Sensor("Nameplate.MainModel", None, factor=1, unit=None),
        Sensor("Nameplate.Model", None, factor=1, unit=None),
        Sensor("Nameplate.ModelStr", None, factor=1, unit=None),
        Sensor("Nameplate.PkgRev", None, factor=1, unit=None),
        Sensor("Nameplate.SerNum", None, factor=1, unit=None),
        Sensor("Nameplate.Vendor", None, factor=1, unit=None),
        Sensor("Portal.EnnexOS.ConnStt", None, factor=1, unit=None),
        Sensor("Spdwr.ActlDnsSrvIp", None, factor=1, unit=None),
        Sensor("Spdwr.ActlGwIp", None, factor=1, unit=None),
        Sensor("Spdwr.ActlIp", None, factor=1, unit=None),
        Sensor("Spdwr.ActlSnetMsk", None, factor=1, unit=None),
        Sensor("Spdwr.AutoCfgIsOn", None, factor=1, unit=None),
        Sensor("Spdwr.IgmpQryTms", None, factor=1, unit=None),
        Sensor("Spdwr.IgmpQryTx", None, factor=1, unit=None),
        Sensor("SwCmp.CmpEnnexOS.Frwk.SwRev", None, factor=1, unit=None),
        Sensor("Sys.DevRstr", None, factor=1, unit=None),
        Sensor("Upd.AutoUpdIsOn", None, factor=1, unit=None),
        Sensor("WebConn.IsOn", None, factor=1, unit=None),
        Sensor("WebConn.Stt", None, factor=1, unit=None),
        Sensor("WebConn.SwRev", None, factor=1, unit=None),
    ],
}
