# Drawing - Cooler Loop CL-401 (Sheet 3 of 8)

Drawing number: DWG-CL401-S3. Part of drawing package DWG-HP1200 supporting hydraulic press HP-1200. This sheet documents the closed-loop oil cooling circuit between manifold M-301 and reservoir T-501. Read in conjunction with HP-1200 operations manual section 3.5 (cooling loop reference) and section 6.4 (oil overheating diagnostics).

## 1. Sheet description and revision history

This sheet shows the plate heat exchanger CL-401 and its associated piping, instrumentation, and control wiring. The cooler is mounted on bracket BR-CL401 on the rear apron of the HP-1200 skid, between the power pack and the reservoir T-501. Coolant flow is bottom-up on the oil side, top-down on the water side, providing counter-flow heat exchange.

### 1.1 Revision history

- Rev D (current, 2026-01-18): added secondary temperature sensor TS-402 and bypass loop interlock with valve BV-405; updated wiring schedule for PLC output Q3.7.
- Rev C (2025-04-22): replaced original cooler with higher-capacity 220 kW unit; updated BOM.
- Rev B (2024-08-09): added pressure relief valve PRV-401 on water side.
- Rev A (2024-01-30): initial release.

### 1.2 Sheet scope

This sheet covers:

- Cooler unit CL-401 and its mounting hardware.
- Circulation pump P-301 and motor M-301-MOT.
- Oil-side filter F-411 upstream of cooler.
- Water-side solenoid SOL-411 and check valve CV-411.
- Temperature instruments TS-401 and TS-402.
- Pressure instruments PG-401 and PG-402.
- All piping between manifold M-301 return port R1 and reservoir T-501 return header.
- Cable schedule for PLC interface to cabinet CP-1.

## 2. Bill of materials

### 2.1 Major equipment

- **CL-401**: plate heat exchanger, Alfa Laval M6-MFG, 220 kW thermal rating, 60 plates, EPDM gaskets, 316L stainless plates. Supplier part AL-M6MFG-60. Tag CL-401.
- **P-301**: circulation pump, KSB Etabloc 50-160, 60 LPM at 4 bar, close-coupled to motor M-301-MOT. Supplier part KSB-EB50-160. Tag P-301.
- **M-301-MOT**: motor for P-301, Siemens 1LE1 4 kW, 1450 RPM, 400 VAC 3-phase, IE3. Supplier part SIE-1LE1503-1AB. Tag M-301-MOT. Note: distinct from manifold M-301 in HP-1200 power pack.
- **F-411**: return-line filter, Hydac RFM 270, 10 micron absolute, beta-200 rated, with clogging indicator CI-411. Supplier part HYD-RFM270-10M. Tag F-411.
- **F-412W**: water-side strainer, Spirax Sarco Y-strainer 50 mesh, DN50. Supplier part SS-Y-DN50. Tag F-412W.

### 2.2 Valves and fittings

- **SOL-411**: bypass solenoid valve, Burkert type 6213 EV, DN25, 24 VDC, normally closed. Supplier part BUR-6213-DN25. Tag SOL-411.
- **CV-411**: check valve, water side, Crane swing check, DN50. Supplier part CR-CK-DN50. Tag CV-411.
- **BV-401**: manual ball valve, oil-side isolation upstream of F-411, DN50, two-piece bronze. Supplier part KIT-BV-DN50. Tag BV-401.
- **BV-402**: manual ball valve, oil-side isolation downstream of CL-401 outlet B1, DN50. Tag BV-402.
- **BV-403**: manual ball valve, water inlet to CL-401 port C1, DN40. Tag BV-403.
- **BV-404**: manual ball valve, water outlet from CL-401 port D1, DN40. Tag BV-404.
- **BV-405**: bypass loop manual valve around CL-401 oil side, DN50, normally closed. Tag BV-405.
- **PRV-401**: pressure relief valve, water side, set to 8 bar, DN20 vent to drain. Supplier part KSB-PRV-8B. Tag PRV-401.
- **DV-401**: drain valve at low point of oil-side return line, DN15. Tag DV-401.
- **VV-401**: vent valve at high point of cooler oil-side outlet, DN10 with hex plug. Tag VV-401.

### 2.3 Instrumentation

- **TS-401**: temperature sensor, RTD PT100, three-wire, mounted on CL-401 outlet pipe 200 mm downstream of port B1. Supplier part EH-TR10-PT100. Tag TS-401.
- **TS-402**: temperature sensor, RTD PT100, three-wire, mounted on CL-401 oil inlet pipe 150 mm upstream of port A1. Supplier part EH-TR10-PT100. Tag TS-402. Added in Rev D.
- **PG-401**: pressure gauge, oil side inlet, 0 to 16 bar, glycerine-filled, DN63 face. Supplier part WIK-213-53-16B. Tag PG-401.
- **PG-402**: pressure gauge, oil side outlet, 0 to 16 bar, glycerine-filled. Supplier part WIK-213-53-16B. Tag PG-402.
- **DPI-401**: differential pressure indicator across CL-401, 0 to 2.5 bar. Supplier part WIK-DPGS40. Tag DPI-401.
- **CI-411**: clogging indicator on F-411, electrical contact rated at 24 VDC 0.5 A. Tag CI-411.
- **FS-401**: water-side flow switch, paddle type, normally open contact closes at flow above 20 LPM. Supplier part GEM-FF-401. Tag FS-401.

### 2.4 Mounting and structural

- **BR-CL401**: cooler mounting bracket, mild steel weldment, hot-dip galvanized.
- **BR-P301**: pump baseplate for P-301 and M-301-MOT, common skid mounted to BR-CL401.
- **VIB-1, VIB-2, VIB-3, VIB-4**: vibration isolators between BR-P301 and main skid, 30 Shore A neoprene.

## 3. Component connection list

The following list documents all process and signal connections relevant to graph extraction. Connection vocabulary uses: feeds, connected, controls, mounted, wired.

### 3.1 Oil-side connections

- Manifold M-301 return port R1 **feeds** filter F-411 inlet via line OL-1 (DN50 pipe).
- Filter F-411 outlet **feeds** cooler CL-401 oil inlet at port A1 via line OL-2 (DN50 pipe).
- Cooler CL-401 oil outlet at port B1 **feeds** reservoir T-501 return header via line OL-3 (DN50 pipe).
- Manual valve BV-401 is **mounted** on line OL-1 between M-301 and F-411.
- Manual valve BV-402 is **mounted** on line OL-3 between CL-401 port B1 and reservoir T-501.
- Manual valve BV-405 is **mounted** on bypass line OL-BP that connects line OL-2 to line OL-3, allowing isolation of CL-401 for maintenance.
- Drain valve DV-401 is **mounted** at the low point of line OL-3.
- Vent valve VV-401 is **mounted** at the high point of CL-401 oil-side dome between port A1 and B1.

### 3.2 Water-side connections

- Facility chilled water supply **feeds** strainer F-412W inlet via line WL-1 (DN40 pipe).
- Strainer F-412W outlet **feeds** solenoid SOL-411 inlet via line WL-2.
- Solenoid SOL-411 outlet **feeds** cooler CL-401 water inlet at port C1 via line WL-3.
- Cooler CL-401 water outlet at port D1 **feeds** check valve CV-411 inlet via line WL-4.
- Check valve CV-411 outlet **connected** to facility return header via line WL-5.
- Manual valves BV-403 and BV-404 are **mounted** on lines WL-3 and WL-4 respectively for isolation.
- Pressure relief valve PRV-401 is **mounted** on water-side outlet line WL-4, vents to floor drain FD-1.
- Flow switch FS-401 is **mounted** on line WL-4 downstream of CV-411.

### 3.3 Pump and motor connections

- Pump P-301 suction **connected** to reservoir T-501 auxiliary port AUX-1 via line OL-AUX (DN50 pipe). The pump runs continuously to circulate cooler-loop oil during machine operation.
- Pump P-301 discharge **connected** to manifold M-301 cooler port CP-1, providing the motive flow for the cooler loop.
- Motor M-301-MOT is **mounted** on baseplate BR-P301 and **connected** to pump P-301 via flexible coupling FC-301.
- Motor M-301-MOT power supply is **wired** from cabinet CP-1 contactor KM-301 via cable PWR-M301 (4-core 4 mm2, length 12 m).

### 3.4 Instrumentation mounting

- Temperature sensor TS-401 is **mounted** on line OL-3, 200 mm downstream of CL-401 port B1, in thermowell TW-401.
- Temperature sensor TS-402 is **mounted** on line OL-2, 150 mm upstream of CL-401 port A1, in thermowell TW-402.
- Pressure gauge PG-401 is **mounted** on line OL-2 just before CL-401 port A1.
- Pressure gauge PG-402 is **mounted** on line OL-3 just after CL-401 port B1.
- Differential pressure indicator DPI-401 is **mounted** across CL-401 oil-side ports A1 and B1 via impulse lines IL-1 and IL-2.
- Clogging indicator CI-411 is **mounted** on filter F-411 head and gives a contact at delta-P above 1.2 bar.

## 4. Cable and wiring schedule

All cables run in cable tray CT-3 from cabinet CP-1 along the rear apron of the skid to the cooler bracket BR-CL401.

### 4.1 Power cables

- **PWR-M301**: motor M-301-MOT mains supply, 4-core 4 mm2 SY screened, 12 m length, runs from cabinet CP-1 contactor KM-301 terminals T1, T2, T3, PE.
- **PWR-SOL411**: solenoid SOL-411 24 VDC supply, 2-core 1 mm2, 10 m length, runs from cabinet CP-1 PLC output module DO-3 terminal Q3.7.

### 4.2 Signal cables

- **SIG-TS401**: TS-401 RTD signal, 3-core screened 0.5 mm2, 11 m length, **wired** from sensor to cabinet CP-1 PLC analog input AI6 at terminal block TB-AI terminals 1, 2, 3.
- **SIG-TS402**: TS-402 RTD signal, 3-core screened 0.5 mm2, 11 m length, **wired** to PLC analog input AI7 at TB-AI terminals 4, 5, 6.
- **SIG-FS401**: FS-401 flow switch contact, 2-core 0.75 mm2, 12 m length, **wired** to PLC digital input I3.2 at terminal block TB-DI terminal 18.
- **SIG-CI411**: CI-411 clogging indicator contact, 2-core 0.75 mm2, 12 m length, **wired** to PLC digital input I3.4 at TB-DI terminal 20.
- **SIG-DPI401**: DPI-401 alarm contact, 2-core 0.75 mm2, 11 m length, **wired** to PLC digital input I3.3 at TB-DI terminal 19.

### 4.3 PLC output mapping

- PLC output Q3.7 **controls** solenoid SOL-411 via cable PWR-SOL411 through interposing relay K-SOL411 on terminal X12-7 of cabinet CP-1.
- PLC output Q3.6 **controls** contactor KM-301 (motor M-301-MOT) via interposing relay K-M301 on terminal X12-6.
- Both interposing relays are 24 VDC coils with LED status indicators.

### 4.4 Earthing and bonding

- Cooler frame BR-CL401 is bonded to skid earth bus EB-1 via 6 mm2 green-yellow conductor.
- Pump baseplate BR-P301 is bonded to EB-1 via 6 mm2 conductor.
- All cable screens are terminated at the cabinet CP-1 EMC gland plate.

## 5. Pneumatic and hydraulic line schedule

### 5.1 Oil-side lines

- **OL-1**: DN50 seamless steel pipe, manifold M-301 port R1 to filter F-411 inlet, length 1.8 m.
- **OL-2**: DN50 seamless steel pipe, F-411 outlet to CL-401 port A1, length 1.2 m.
- **OL-3**: DN50 seamless steel pipe, CL-401 port B1 to reservoir T-501 return header, length 2.4 m.
- **OL-AUX**: DN50 seamless steel pipe, T-501 port AUX-1 to pump P-301 suction, length 1.6 m.
- **OL-BP**: DN50 bypass line, OL-2 tee to OL-3 tee, length 0.9 m, normally isolated by BV-405.
- **IL-1, IL-2**: DN6 stainless impulse lines for DPI-401, length 0.4 m each.

### 5.2 Water-side lines

- **WL-1**: DN40 copper pipe, facility supply to strainer F-412W, length 2.0 m.
- **WL-2**: DN40 copper pipe, F-412W to SOL-411, length 0.5 m.
- **WL-3**: DN40 copper pipe, SOL-411 to CL-401 port C1, length 0.6 m.
- **WL-4**: DN40 copper pipe, CL-401 port D1 to CV-411, length 0.5 m.
- **WL-5**: DN40 copper pipe, CV-411 to facility return header, length 1.8 m.

### 5.3 Pneumatic

No pneumatic lines on this sheet. Reference air supply at AP-1 is documented on sheet 8.

## 6. Off-page connectors

- Coolant supply continues on **sheet 4** (drawing CL-402, port A2 of CL-401) for the secondary cooling loop serving the gearbox heat exchanger.
- Manifold M-301 detailed plumbing on **sheet 2** (drawing HSCH-HP1200-S2).
- Reservoir T-501 internal detail on **sheet 5** (drawing TNK-T501-S5).
- PLC I/O panel layout for cabinet CP-1 on **sheet 7** (drawing PNL-CP1-S7).
- Cable tray routing on **sheet 8** (drawing CT-RTG-S8).
- Facility chilled water tie-in point on **sheet 1** (utility plan UTL-S1).

## 7. Cross-references to HP-1200 manual

- Cooler loop role and overall hydraulic architecture: HP-1200 manual section 3.5.
- Diagnostic procedure for oil overheating fault E-031: HP-1200 manual section 6.4.
- Cooler-related fault codes E-050 through E-053: HP-1200 manual section 7.3.
- Filter F-411 service and cartridge part HYD-F411-10M: HP-1200 manual section 8.3 (monthly checks) and section 10.1 (parts catalog).
- Quarterly cooler inspection procedure: HP-1200 manual section 8.4.
- Cooler bypass solenoid SOL-411 wiring at PLC output Q3.7: HP-1200 manual section 4.2 (PLC I/O assignment).
- Lockout sequence prior to opening BV-401, BV-402, or removing CL-401 plates: HP-1200 manual section 2.3.

## 8. Maintenance access notes

- The cooler CL-401 plate stack can be accessed by removing the four front fasteners FAST-CL-1 through FAST-CL-4 and sliding the front follower forward on guide rods GR-1 and GR-2.
- A minimum clearance of 900 mm in front of the cooler is required to fully extract the plate pack.
- During plate-pack service the bypass valve BV-405 must be opened and BV-401 plus BV-402 must be closed. The pump P-301 must be locked out at cabinet CP-1.
- The water side must be drained via PRV-401 vent or the bottom drain plug DP-401 prior to opening any flange.
- After re-assembly, vent the oil side at VV-401 and the water side at the highest point of WL-4 before resuming normal operation.

## 9. Notes and warnings

### 9.1 Design parameters

- Maximum allowable working pressure, oil shell side: 16 bar.
- Maximum allowable working pressure, water tube side: 25 bar.
- Maximum temperature, oil side: 80 degrees C continuous.
- Maximum temperature, water side: 60 degrees C continuous.
- Minimum cooling water flow at full press production: 25 LPM.
- Nominal heat removal at 220 bar press production with 35 degrees C oil and 18 degrees C water: 180 to 200 kW.

### 9.2 Operational warnings

- Differential pressure across F-411 reading above 1.2 bar at DPI-401 indicates filter cartridge HYD-F411-10M needs replacement.
- Differential pressure across CL-401 reading above 1.5 bar at DPI-401 indicates plate stack fouling and requires reverse-flush or chemical cleaning.
- Loss of cooling water flow detected at FS-401 will trigger fault E-050 and cause the press to halt at the next top of stroke.
- Solenoid SOL-411 must remain energized whenever pump P-201 is running. Loss of feedback at PLC input I4.5 generates fault E-053.
- Never open BV-405 while BV-401 and BV-402 are open; this short-circuits the cooler and bypasses heat rejection.

### 9.3 Material compatibility

The cooler gaskets are EPDM and are not compatible with phosphate-ester fluids. The HP-1200 standard fill is mineral oil ISO VG 46 only. If the press is converted to fire-resistant fluid, the gaskets must be upgraded to FKM (part AL-M6MFG-60-FKM) and the documentation flagged accordingly.
