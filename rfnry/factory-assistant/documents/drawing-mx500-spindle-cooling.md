# Drawing - MX-500 Spindle Cooling Loop CL-401 (Sheet 3 of 6)

Drawing number: DWG-CL401-S3-MX500. Part of drawing package DWG-MX500 supporting the MX-500 vertical machining center. This sheet documents the closed-loop oil cooling circuit between the spindle cartridge SP-101 and the plate heat exchanger CL-401. Read in conjunction with MX-500 service manual section 4 (coolant system) and section 6.2 (spindle housing overtemperature).

## 1. Sheet description and revision history

This sheet shows the plate heat exchanger CL-401 dedicated to spindle housing oil cooling and its associated piping, instrumentation, and control wiring. The cooler is mounted on bracket BR-CL401 on the rear column of the MX-500, between the column and the rear cabinet wall.

### 1.1 Revision history

- Rev D (current, 2026-03-15): added secondary temperature sensor TS-402 on the cooler oil inlet; updated wiring schedule for PLC analog input AI7.
- Rev C (2025-08-10): replaced the original brazed-plate cooler with a gasketed plate heat exchanger of equivalent rating to allow plate-pack service.
- Rev B (2025-04-22): added pressure relief valve PRV-401 on the water side at customer request.
- Rev A (2024-11-30): initial release.

### 1.2 Sheet scope

This sheet covers:

- Cooler unit CL-401 and its mounting hardware.
- Circulation pump P-301 and motor M-301-MOT (distinct from coolant pumps LP-201 and HP-202 in the work envelope).
- Oil-side filter F-411 upstream of the cooler.
- Water-side solenoid SOL-411 and check valve CV-411.
- Temperature instruments TS-401 and TS-402.
- Pressure instruments PG-401 and PG-402.
- All piping between the spindle housing return port SR-1 and the spindle housing supply port SS-1.
- Cable schedule for PLC interface to cabinet CP-1.

## 2. Bill of materials

### 2.1 Major equipment

- **CL-401**: plate heat exchanger, Alfa Laval M3-FG, 25 kW thermal rating, 30 plates, EPDM gaskets, 316L stainless plates. Supplier part AL-M3FG-30. Tag CL-401.
- **P-301**: circulation pump, KSB Etabloc 32-125, 18 LPM at 3 bar, close-coupled to motor M-301-MOT. Supplier part KSB-EB32-125. Tag P-301.
- **M-301-MOT**: motor for P-301, Siemens 1LE1 0.75 kW, 1450 RPM, 400 VAC 3-phase, IE3. Supplier part SIE-1LE1503-0KB. Tag M-301-MOT.
- **F-411**: oil-side return filter, Hydac RFM 165, 10 micron absolute, beta-200 rated, with clogging indicator CI-411. Supplier part HYD-RFM165-10M. Tag F-411.
- **F-412W**: water-side strainer, Spirax Sarco Y-strainer 50 mesh, DN25. Supplier part SS-Y-DN25. Tag F-412W.

### 2.2 Valves and fittings

- **SOL-411**: bypass solenoid valve, Burkert type 6213 EV, DN20, 24 VDC, normally closed. Supplier part BUR-6213-DN20. Tag SOL-411.
- **CV-411**: check valve, water side, Crane swing check, DN25. Supplier part CR-CK-DN25. Tag CV-411.
- **BV-401**: manual ball valve, oil-side isolation upstream of F-411, DN25. Tag BV-401.
- **BV-402**: manual ball valve, oil-side isolation downstream of CL-401 outlet B1, DN25. Tag BV-402.
- **BV-403**: manual ball valve, water inlet to CL-401 port C1, DN20. Tag BV-403.
- **BV-404**: manual ball valve, water outlet from CL-401 port D1, DN20. Tag BV-404.
- **BV-405**: bypass loop manual valve around CL-401 oil side, DN25, normally closed. Tag BV-405.
- **PRV-401**: pressure relief valve, water side, set to 8 bar, DN15 vent to drain. Supplier part KSB-PRV-8B. Tag PRV-401.
- **DV-401**: drain valve at low point of oil-side return line, DN15. Tag DV-401.
- **VV-401**: vent valve at high point of cooler oil-side outlet, DN10 with hex plug. Tag VV-401.

### 2.3 Instrumentation

- **TS-401**: temperature sensor, RTD PT100, three-wire, mounted on CL-401 oil outlet pipe 200 mm downstream of port B1, in thermowell TW-401. Supplier part EH-TR10-PT100. Tag TS-401.
- **TS-402**: temperature sensor, RTD PT100, three-wire, mounted on CL-401 oil inlet pipe 150 mm upstream of port A1, in thermowell TW-402. Supplier part EH-TR10-PT100. Tag TS-402. Added in Rev D.
- **PG-401**: pressure gauge, oil side inlet, 0 to 10 bar, glycerine-filled, DN50 face. Supplier part WIK-213-53-10B. Tag PG-401.
- **PG-402**: pressure gauge, oil side outlet, 0 to 10 bar, glycerine-filled. Supplier part WIK-213-53-10B. Tag PG-402.
- **DPI-401**: differential pressure indicator across CL-401, 0 to 2.5 bar. Supplier part WIK-DPGS40. Tag DPI-401.
- **CI-411**: clogging indicator on F-411, electrical contact rated at 24 VDC 0.5 A. Tag CI-411.
- **FS-401**: water-side flow switch, paddle type, normally open contact closes at flow above 12 LPM. Supplier part GEM-FF-401. Tag FS-401.

## 3. Component connection list

The following list documents all process and signal connections relevant to graph extraction. Connection vocabulary uses: feeds, connected, controls, mounted, wired.

### 3.1 Oil-side connections

- Spindle housing return port SR-1 **feeds** filter F-411 inlet via line OL-1 (DN25 pipe).
- Filter F-411 outlet **feeds** cooler CL-401 oil inlet at port A1 via line OL-2 (DN25 pipe).
- Cooler CL-401 oil outlet at port B1 **feeds** spindle housing supply port SS-1 via line OL-3 (DN25 pipe).
- Manual valve BV-401 is **mounted** on line OL-1 between SR-1 and F-411.
- Manual valve BV-402 is **mounted** on line OL-3 between CL-401 port B1 and the spindle housing.
- Manual valve BV-405 is **mounted** on bypass line OL-BP that connects line OL-2 to line OL-3, allowing isolation of CL-401 for maintenance.
- Drain valve DV-401 is **mounted** at the low point of line OL-3.
- Vent valve VV-401 is **mounted** at the high point of CL-401 oil-side dome between port A1 and B1.

### 3.2 Water-side connections

- Facility chilled water supply **feeds** strainer F-412W inlet via line WL-1 (DN20 pipe).
- Strainer F-412W outlet **feeds** solenoid SOL-411 inlet via line WL-2.
- Solenoid SOL-411 outlet **feeds** cooler CL-401 water inlet at port C1 via line WL-3.
- Cooler CL-401 water outlet at port D1 **feeds** check valve CV-411 inlet via line WL-4.
- Check valve CV-411 outlet **connected** to facility return header via line WL-5.
- Manual valves BV-403 and BV-404 are **mounted** on lines WL-3 and WL-4 respectively for isolation.
- Pressure relief valve PRV-401 is **mounted** on water-side outlet line WL-4, vents to floor drain FD-1.
- Flow switch FS-401 is **mounted** on line WL-4 downstream of CV-411.

### 3.3 Pump and motor connections

- Pump P-301 suction **connected** to oil reservoir RES-301 (mounted on bracket BR-RES-301 below the cooler) via line OL-AUX (DN25 pipe). The pump runs continuously to circulate spindle cooling oil during machine operation.
- Pump P-301 discharge **connected** to spindle housing supply manifold via line OL-3 through cooler CL-401, providing the motive flow for the cooler loop.
- Motor M-301-MOT is **mounted** on baseplate BR-P301 and **connected** to pump P-301 via flexible coupling FC-301.
- Motor M-301-MOT power supply is **wired** from cabinet CP-1 contactor KM-301 via cable PWR-M301 (4-core 1.5 mm2, length 8 m).

### 3.4 Instrumentation mounting

- Temperature sensor TS-401 is **mounted** on line OL-3, 200 mm downstream of CL-401 port B1, in thermowell TW-401.
- Temperature sensor TS-402 is **mounted** on line OL-2, 150 mm upstream of CL-401 port A1, in thermowell TW-402.
- Pressure gauge PG-401 is **mounted** on line OL-2 just before CL-401 port A1.
- Pressure gauge PG-402 is **mounted** on line OL-3 just after CL-401 port B1.
- Differential pressure indicator DPI-401 is **mounted** across CL-401 oil-side ports A1 and B1 via impulse lines IL-1 and IL-2.
- Clogging indicator CI-411 is **mounted** on filter F-411 head and gives a contact at delta-P above 1.0 bar.

## 4. Cable and wiring schedule

All cables run in cable tray CT-3 from cabinet CP-1 along the rear column of the MX-500 to the cooler bracket BR-CL401.

### 4.1 Power cables

- **PWR-M301**: motor M-301-MOT mains supply, 4-core 1.5 mm2 SY screened, 8 m length, runs from cabinet CP-1 contactor KM-301 terminals T1, T2, T3, PE.
- **PWR-SOL411**: solenoid SOL-411 24 VDC supply, 2-core 1 mm2, 7 m length, runs from cabinet CP-1 PLC output module DO-3 terminal Q3.7.

### 4.2 Signal cables

- **SIG-TS401**: TS-401 RTD signal, 3-core screened 0.5 mm2, 8 m length, **wired** from sensor to cabinet CP-1 PLC analog input AI6 at terminal block TB-AI terminals 1, 2, 3.
- **SIG-TS402**: TS-402 RTD signal, 3-core screened 0.5 mm2, 8 m length, **wired** to PLC analog input AI7 at TB-AI terminals 4, 5, 6.
- **SIG-FS401**: FS-401 flow switch contact, 2-core 0.75 mm2, 8 m length, **wired** to PLC digital input I3.2 at terminal block TB-DI terminal 18.
- **SIG-CI411**: CI-411 clogging indicator contact, 2-core 0.75 mm2, 8 m length, **wired** to PLC digital input I3.4 at TB-DI terminal 20.
- **SIG-DPI401**: DPI-401 alarm contact, 2-core 0.75 mm2, 8 m length, **wired** to PLC digital input I3.3 at TB-DI terminal 19.

### 4.3 PLC output mapping

- PLC output Q3.7 **controls** solenoid SOL-411 via cable PWR-SOL411 through interposing relay K-SOL411 on terminal X12-7 of cabinet CP-1.
- PLC output Q3.6 **controls** contactor KM-301 (motor M-301-MOT) via interposing relay K-M301 on terminal X12-6.
- Both interposing relays are 24 VDC coils with LED status indicators.

### 4.4 Earthing and bonding

- Cooler frame BR-CL401 is bonded to MX-500 earth bus EB-1 via 4 mm2 green-yellow conductor.
- Pump baseplate BR-P301 is bonded to EB-1 via 4 mm2 conductor.
- All cable screens are terminated at the cabinet CP-1 EMC gland plate.

## 5. Hydraulic line schedule

### 5.1 Oil-side lines

- **OL-1**: DN25 seamless steel pipe, spindle housing return SR-1 to filter F-411 inlet, length 1.2 m.
- **OL-2**: DN25 seamless steel pipe, F-411 outlet to CL-401 port A1, length 0.8 m.
- **OL-3**: DN25 seamless steel pipe, CL-401 port B1 to spindle housing supply SS-1, length 1.6 m.
- **OL-AUX**: DN25 seamless steel pipe, oil reservoir RES-301 port AUX-1 to pump P-301 suction, length 0.5 m.
- **OL-BP**: DN25 bypass line, OL-2 tee to OL-3 tee, length 0.6 m, normally isolated by BV-405.
- **IL-1, IL-2**: DN6 stainless impulse lines for DPI-401, length 0.3 m each.

### 5.2 Water-side lines

- **WL-1**: DN20 copper pipe, facility supply to strainer F-412W, length 1.4 m.
- **WL-2**: DN20 copper pipe, F-412W to SOL-411, length 0.4 m.
- **WL-3**: DN20 copper pipe, SOL-411 to CL-401 port C1, length 0.5 m.
- **WL-4**: DN20 copper pipe, CL-401 port D1 to CV-411, length 0.4 m.
- **WL-5**: DN20 copper pipe, CV-411 to facility return header, length 1.2 m.

## 6. Off-page connectors

- Spindle housing internal oil galleries on **sheet 1** (drawing DWG-MX500-S1).
- Coolant tank T-501 detail on **sheet 5** (drawing TNK-T501-S5).
- PLC I/O panel layout for cabinet CP-1 on **sheet 4** (drawing PNL-CP1-S4).
- Cable tray routing on **sheet 6** (drawing CT-RTG-S6).
- Facility chilled water tie-in on the building utility plan UTL-S1.

## 7. Cross-references to MX-500 service manual

- Coolant cooler loop role and overall system architecture: MX-500 service manual section 4.
- Diagnostic procedure for spindle housing overtemperature fault F-411: MX-500 service manual section 6.2.
- Coolant-related fault codes F-501 through F-514: MX-500 service manual section 7.3.
- Filter F-411 service and cartridge part HYD-RFM165-10M: MX-500 service manual section 8.2 (weekly checks).
- Quarterly cooler inspection procedure: MX-500 service manual section 8.4.
- Cooler bypass solenoid SOL-411 wiring at PLC output Q3.7: MX-500 service manual section 5 (axis drives) cross-references the same I/O block.
- Lockout sequence prior to opening BV-401, BV-402, or removing CL-401 plates: MX-500 service manual section 2.3.

## 8. Maintenance access notes

- The cooler CL-401 plate stack can be accessed by removing the four front fasteners FAST-CL-1 through FAST-CL-4 and sliding the front follower forward on guide rods GR-1 and GR-2.
- A minimum clearance of 600 mm in front of the cooler is required to fully extract the plate pack.
- During plate-pack service the bypass valve BV-405 must be opened and BV-401 plus BV-402 must be closed. The pump P-301 must be locked out at cabinet CP-1.
- The water side must be drained via PRV-401 vent or the bottom drain plug DP-401 prior to opening any flange.
- After re-assembly, vent the oil side at VV-401 and the water side at the highest point of WL-4 before resuming normal operation.

## 9. Notes and warnings

### 9.1 Design parameters

- Maximum allowable working pressure, oil shell side: 10 bar.
- Maximum allowable working pressure, water tube side: 25 bar.
- Maximum temperature, oil side: 60 degrees C continuous.
- Maximum temperature, water side: 50 degrees C continuous.
- Minimum cooling water flow at full spindle production: 15 LPM.
- Nominal heat removal at 12000 RPM continuous cutting with 24 degrees C oil and 18 degrees C water: 18 to 22 kW.

### 9.2 Operational warnings

- Differential pressure across F-411 reading above 1.0 bar at DPI-401 indicates filter cartridge HYD-RFM165-10M needs replacement.
- Differential pressure across CL-401 reading above 1.5 bar at DPI-401 indicates plate stack fouling and requires reverse-flush or chemical cleaning.
- Loss of cooling water flow detected at FS-401 below 8 LPM will trigger fault F-411 and halt the spindle within 200 ms.
- Solenoid SOL-411 must remain energized whenever pump P-301 is running. Loss of feedback at PLC input I4.5 generates fault F-413 (this fault is independent of the spindle drawbar pressure-high fault that shares the same numeric code in older firmware revisions; see the meeting transcript dated 2026-04-22 for the disambiguation effort).
- Never open BV-405 while BV-401 and BV-402 are open; this short-circuits the cooler and bypasses heat rejection.

### 9.3 Material compatibility

The cooler gaskets are EPDM and are not compatible with phosphate-ester fluids. The MX-500 standard fill is mineral oil ISO VG 32 only. If the cooler is converted to fire-resistant fluid, the gaskets must be upgraded to FKM (part AL-M3FG-30-FKM) and the documentation flagged accordingly.
