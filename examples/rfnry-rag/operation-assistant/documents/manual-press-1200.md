# Hydraulic Press HP-1200 - Operations Manual

Document number: OPS-HP1200-R7. Supersedes revision R6 dated 2024-03-12. Applies to all HP-1200 units with serial numbers HP1200-0214 through HP1200-0488. Read in conjunction with drawing package DWG-HP1200 sheets 1 through 8 and electrical schematic ESCH-HP1200 sheets 1 through 12.

## 1. Overview and specifications

The HP-1200 is a four-column down-acting hydraulic forming press rated for 1200 metric tons of nominal force. The machine is designed for cold forming, deep drawing, blanking, and coining of mild and stainless steel sheet up to 12 mm thickness. The unit ships pre-assembled on a single skid with the power pack mounted on the rear apron.

### 1.1 Mechanical specifications

- Nominal force: 1200 metric tons at 220 bar system pressure.
- Maximum continuous duty cycle: 12 strokes per minute.
- Stroke length: 800 mm, programmable in 1 mm increments.
- Daylight opening: 1400 mm with bolster removed.
- Bed area: 2500 mm by 1600 mm.
- Slide weight: 14800 kg.
- Approach speed: 320 mm per second.
- Pressing speed: 22 mm per second at full tonnage.
- Return speed: 380 mm per second.
- Total machine weight: 78 metric tons.

### 1.2 Hydraulic specifications

- Operating pressure range: 180 to 220 bar.
- Maximum allowable pressure: 240 bar (relief valve RV-110 set point).
- Reservoir capacity: 2400 liters of ISO VG 46 mineral oil.
- Recommended fluid: Shell Tellus S2 MX 46 or equivalent meeting DIN 51524 part 2 HLP.
- Filtration target: ISO 4406 cleanliness class 18/16/13 or better.
- Operating temperature window: 38 to 55 degrees C.

### 1.3 Electrical specifications

- Mains supply: 400 VAC, 3-phase, 50 Hz, 250 A service.
- Control voltage: 24 VDC supplied by power supply unit PSU-101 (Phoenix Contact QUINT4-PS/1AC/24DC/40).
- PLC: Siemens S7-1500 CPU 1516F-3 PN/DP at slot 2 of rack RK-01.
- HMI: Siemens TP1500 Comfort, 15 inch widescreen, mounted on swing arm SA-12.
- Safety relay: Pilz PNOZ s7 controlling E-stop and light curtain inputs.

### 1.4 Site requirements

- Foundation: reinforced concrete pad minimum 800 mm depth, 35 MPa rating.
- Compressed air: 6 bar clean dry air, 200 NL/min peak demand at port AP-1.
- Cooling water (optional plate exchanger CL-401): 30 LPM at 18 to 25 degrees C.
- Ambient temperature: 5 to 40 degrees C, non-condensing humidity.

## 2. Safety system

The HP-1200 safety architecture is rated PL e Cat 4 according to ISO 13849-1. All safety components are pre-wired to terminal block TB-SAFE in cabinet CP-1 and cross-monitored by safety relay PNOZ-1.

### 2.1 Light curtains

Two SICK deTec4 Core light curtains guard the front aperture:

- LC-FRONT-A: left half, resolution 14 mm, protective height 1200 mm, range 6 m.
- LC-FRONT-B: right half, resolution 14 mm, protective height 1200 mm, range 6 m.

Each curtain output (OSSD1, OSSD2) is wired to safety relay PNOZ-1 inputs S11/S12 and S21/S22 respectively. Muting sensors MS-101 and MS-102 are mounted at the rear of the bed for material feed-through and feed signals to the muting controller MC-201.

### 2.2 Emergency stop circuit

Three E-stop pushbuttons are installed:

- ES-OP-1 on the operator HMI pendant.
- ES-OP-2 on the rear maintenance platform.
- ES-OP-3 on the cabinet CP-1 front door.

All three buttons are wired in series to the PNOZ-1 dual-channel inputs. When any E-stop is depressed, the safety relay drops its output contacts within 25 ms, which in turn de-energizes the main solenoid valve V-101 and closes the pump P-201 contactor KM-201. Total response time from button press to pressure drop at the slide is 80 ms or less.

### 2.3 Lockout and tagout

Before performing any maintenance involving the platen, the cylinder C-501, or the manifold M-301, follow the lockout sequence:

1. Lower the platen to the bed using the manual jog mode.
2. Press E-stop ES-OP-1.
3. Open main disconnect QS-1 on cabinet CP-1 and apply padlock and tag.
4. Bleed accumulator A-203 by opening manual bleed valve BV-203 until gauge G-203 reads zero.
5. Close manual ball valves BV-201 (pump discharge) and BV-204 (return).
6. Insert mechanical safety blocks SB-1 and SB-2 between platen and bolster.
7. Verify zero pressure at gauge G-301 on manifold M-301.

### 2.4 Two-hand control

In manual mode the operator must press both palm buttons PB-LH and PB-RH within 500 ms of each other to initiate a stroke. The buttons are wired to PNOZ-1 inputs and monitored by the PLC for synchronous operation. Any timing fault generates fault code E-021.

## 3. Hydraulic system

### 3.1 Power pack

The hydraulic power pack is mounted on the rear apron of the press skid. Primary components:

- Pump P-201: Bosch Rexroth A4VSO 250 DRG, axial piston, pressure-compensated, 250 cc/rev displacement, driven by motor M-201 (Siemens 1LE1, 132 kW, 1480 RPM).
- Pump P-202: Bosch Rexroth A10VSO 71, auxiliary pilot and pre-fill pump, 71 cc/rev.
- Reservoir T-501: 2400 L stainless steel tank with sight glass SG-501 and breather BR-501.
- Cooler CL-401: plate heat exchanger, 220 kW rating, water-cooled (see drawing CL-401 sheet 3 of 8).
- Filter F-411: return-line filter, 10 micron absolute, beta-200 rated, with clogging indicator CI-411.
- Filter F-412: pressure-line filter, 5 micron, mounted downstream of P-201.

### 3.2 Manifold M-301

Manifold M-301 is a custom cast iron block bolted to the cylinder yoke. It contains the following cartridge valves:

- V-101: main directional control, NG25, pilot-operated, Rexroth WEH25 with solenoids Y1A and Y1B at 24 VDC.
- PV-105: proportional pressure valve, NG10, Rexroth DBETR-10, 0 to 10 V command from PLC analog output AQ4.
- RV-110: pressure relief valve, NG16, set to 240 bar, lead-sealed.
- POCV-130: pilot-operated check valve, NG25, Rexroth SV30PB1 holding the slide against gravity.
- CBV-220: counterbalance valve, NG16, Rexroth FD16KA, set 30 bar above static load pressure.
- LV-140: load-sensing shuttle, NG6, feeds pressure signal to PV-105.

Test points TP-1 through TP-6 are M16x2 minimess connectors located on the front face of M-301 for diagnostic gauge attachment.

### 3.3 Accumulator station

- A-203: bladder accumulator, 50 L, nitrogen pre-charged to 90 bar, rated 350 bar.
- A-204: bladder accumulator, 20 L, nitrogen pre-charged to 60 bar, dedicated to pilot pressure.
- BV-203: manual bleed valve for A-203.
- SV-203: safety valve, set to 250 bar, vents to T-501.

Pre-charge nitrogen pressure must be checked monthly with the dedicated charging kit (part number CHG-A203-K).

### 3.4 Cylinder C-501

The main pressing cylinder C-501 is a single-acting plunger cylinder with the following characteristics:

- Bore: 800 mm.
- Stroke: 850 mm (mechanical), 800 mm (programmed).
- Maximum pressure: 240 bar.
- Piston seal: Hallite 605 (part HLT-605-800).
- Rod wiper: Merkel PT2 (part MKL-PT2-800).
- Position feedback: magnetostrictive linear transducer LT-501 (Balluff BTL7), 1000 mm stroke, 0.01 mm resolution.

Two return cylinders C-502 and C-503 (bore 200 mm, stroke 850 mm) lift the slide on the up-stroke. They are fed from the auxiliary pump P-202 through directional valve V-102.

### 3.5 Cooling loop reference

The cooler CL-401 forms the closed-loop heat rejection path for the hydraulic system. Return oil from manifold M-301 passes through filter F-411, then through the shell side of CL-401, then back to reservoir T-501. The water side of CL-401 is supplied from facility chilled water via solenoid valve SOL-411. Full component layout, BOM, and connection list are documented in drawing CL-401 sheet 3 of 8 (document DWG-CL401-S3).

## 4. Electrical system

### 4.1 Cabinet CP-1

Main control cabinet CP-1 is a Rittal VX25 enclosure, 1800 mm tall by 1200 mm wide by 600 mm deep, mounted on the rear of the skid. Internal layout:

- Top section: main disconnect QS-1, line filter LF-1, surge protection SPD-1.
- Upper middle: motor starters KM-201 and KM-202 (Siemens SIRIUS 3RT).
- Lower middle: PLC rack RK-01, safety relay PNOZ-1, IO modules.
- Bottom: 24 VDC supplies PSU-101 and PSU-102, terminal blocks TB-1 through TB-12.

### 4.2 PLC I/O assignment

Selected I/O points (full list in document IOL-HP1200-R3):

- I0.0: main start pushbutton PB-START.
- I0.1: cycle stop pushbutton PB-STOP.
- I0.2: two-hand left palm PB-LH.
- I0.3: two-hand right palm PB-RH.
- I1.0: light curtain LC-FRONT-A OSSD feedback.
- I1.1: light curtain LC-FRONT-B OSSD feedback.
- I2.0: top-of-stroke proximity sensor PS-101.
- I2.1: bottom-of-stroke proximity sensor PS-102.
- I3.4: filter F-411 clogging switch CI-411.
- I3.5: oil level low switch LS-501 on T-501.
- I3.6: oil temperature high switch TS-501 on T-501.
- Q0.0: pump P-201 contactor KM-201 coil.
- Q0.1: pump P-202 contactor KM-202 coil.
- Q1.0: V-101 solenoid Y1A (downstroke).
- Q1.1: V-101 solenoid Y1B (upstroke).
- Q3.7: cooler bypass solenoid SOL-411 (see drawing CL-401).
- AI4: pressure transducer PT-301 on manifold M-301, 4-20 mA, 0 to 250 bar.
- AI5: position transducer LT-501 on cylinder C-501.
- AI6: oil temperature RTD TT-501 on reservoir T-501.
- AQ4: proportional valve PV-105 command, 0 to 10 V.

### 4.3 Motor protection

- KM-201 (P-201 main motor): Siemens 3RV2 motor protection circuit breaker, set to 245 A, with auxiliary contact wired to PLC input I4.0.
- KM-202 (P-202 auxiliary motor): Siemens 3RV2, set to 32 A, auxiliary on I4.1.
- Thermistor relay TR-201 monitors motor M-201 PTC sensors and trips KM-201 on overheat. TR-201 fault is wired to I4.2.

### 4.4 Sensors

- PT-301: pressure transducer, Hydac HDA 4445, 0 to 250 bar, 4-20 mA, mounted at manifold M-301 test point TP-1.
- PT-203: pressure transducer, accumulator A-203, 0 to 350 bar.
- LT-501: linear transducer, cylinder C-501, magnetostrictive.
- TT-501: temperature transducer, reservoir T-501, RTD PT100.
- TS-401: temperature sensor, cooler CL-401 outlet, RTD PT100 (see drawing CL-401).
- PS-101 and PS-102: inductive proximity sensors, Sick IME12, NPN NO.

## 5. Operator interface

### 5.1 HMI screens

The TP1500 HMI provides the following screen hierarchy:

- HOME: machine status, current mode, last fault, cycle counter.
- PRODUCTION: recipe selector, part counter, OEE display.
- MANUAL: jog controls, valve diagnostics, sensor live values.
- RECIPE: load, save, edit recipes (password-protected at level 2).
- DIAGNOSTICS: I/O status, fault history, trend graphs.
- MAINTENANCE: service hour counters, lubrication reminders.
- PARAMETERS: pressure setpoints, position setpoints, timer values (level 3 password).

### 5.2 Operating modes

- OFF: system de-energized, only HMI live.
- MANUAL: jog only, two-hand control required, single strokes.
- SETUP: low-pressure (50 bar) jog for die installation, requires key switch KS-SETUP at position 1.
- AUTO: full production, recipe-driven, requires both light curtains clear.
- CALIBRATION: service mode, level 3 password, allows direct valve commands.

### 5.3 Recipes

Recipes are stored on the HMI internal SD card and cover the following parameters per part program:

- Approach speed setpoint (mm/s).
- Pressing pressure setpoint (bar) commanded to PV-105.
- Dwell time at bottom dead center (ms).
- Decompression ramp time (ms).
- Return speed setpoint (mm/s).
- Top of stroke position (mm from reference).
- Slow-down position (mm above bottom dead center).

Recipes 001 through 050 are reserved for production. Recipes 901 through 999 are reserved for service and test cycles.

## 6. Common faults and troubleshooting

### 6.1 Slow downstroke

Symptom: slide takes longer than commanded to reach bottom dead center; cycle time exceeds recipe target.

Diagnostic steps:

1. Check accumulator A-203 nitrogen pre-charge against target 90 bar using charging kit CHG-A203-K. Recharge if reading is below 80 bar.
2. Inspect proportional valve PV-105 spool feedback at HMI Diagnostics screen. Spool position should track command within 2 percent.
3. Verify pump P-201 case-drain flow at test point TP-CD does not exceed 4 LPM. Excessive case drain indicates internal pump wear.
4. Confirm filter F-412 differential pressure at gauge DPG-412 is below 2 bar. Replace cartridge if above.
5. Check oil viscosity by sampling reservoir T-501 and sending to lab; ISO VG 46 should read 41 to 50 cSt at 40 degrees C.

### 6.2 Pressure relief chatter

Symptom: audible buzz or hammering at full system pressure, oscillating PT-301 reading.

Diagnostic steps:

1. Replace return-line filter F-411 (cartridge part HYD-F411-10M). Contaminated oil is the leading cause.
2. Inspect relief valve RV-110 poppet seat for scoring or particle damage. Replace cartridge if seat is not mirror-smooth.
3. Bleed pilot line at PV-105 test port TP-2 to remove trapped air.
4. Verify accumulator A-204 pilot pre-charge is at 60 bar.
5. If chatter persists, replace RV-110 cartridge (Rexroth DBDS6K1X/240).

### 6.3 Platen drift during dwell

Symptom: platen position LT-501 reading drifts downward more than 0.5 mm during programmed dwell time.

Most likely causes, in order:

- Internal leak past piston seal in cylinder C-501. Replace seal kit HLT-605-800 (requires platen removal).
- Counterbalance valve CBV-220 sticking open due to contamination. Flush manifold and replace cartridge.
- Pilot-operated check valve POCV-130 leaking back. Inspect for contamination, replace if seat is damaged.
- Proportional valve PV-105 zero offset drift. Run calibration procedure CAL-PV105.

### 6.4 Hydraulic oil overheating

Symptom: TT-501 reading climbs above 55 degrees C during normal production, alarm A-031 triggers at 58 degrees C, fault E-031 trips at 62 degrees C.

Diagnostic steps:

1. Verify cooling water flow to CL-401 is at least 25 LPM. Check facility supply pressure at PT-CW.
2. Confirm bypass solenoid SOL-411 is energizing correctly (Q3.7 on PLC). Manually open SOL-411 from HMI Manual screen.
3. Inspect CL-401 plate fouling. Differential pressure across cooler exceeding 1.5 bar indicates fouling.
4. Check ambient temperature in the press hall; CL-401 capacity is rated at 25 degrees C inlet water.
5. Sample reservoir T-501 oil for water content. Above 500 ppm reduces cooler effectiveness.

Refer to drawing CL-401 sheet 3 of 8 for complete cooler loop service procedure.

### 6.5 Sensor faults

#### 6.5.1 LT-501 position transducer fault

Fault E-042 indicates the magnetostrictive transducer LT-501 has lost signal. Check cable BLT-501 from cylinder head to PLC analog input AI5. Replace transducer if cable is verified good.

#### 6.5.2 PT-301 pressure transducer fault

Fault E-043 indicates pressure transducer PT-301 has gone out of range or open circuit. Check 4-20 mA loop with reference meter at TB-3 terminals 12 and 13. Typical replacement: Hydac HDA 4445.

#### 6.5.3 Light curtain fault

Fault E-002 (light curtain blocked) or E-003 (light curtain internal fault) on either LC-FRONT-A or LC-FRONT-B. For E-002, clear obstruction from the front aperture. For E-003, check alignment using the SICK alignment laser kit and reset via HMI Diagnostics screen.

### 6.6 PLC and communication faults

- E-080: PROFINET communication loss to remote IO. Check switch SW-1 and cable PNC-01.
- E-081: HMI communication loss. Power-cycle HMI; check Ethernet cable to switch SW-1.
- E-082: drive ServoPack DRV-201 communication loss. Check shielded cable to drive.

## 7. Fault code reference

Fault codes are grouped by subsystem. Full list maintained in document FCL-HP1200-R5.

### 7.1 Safety faults E-001 to E-019

- E-001: emergency stop pressed.
- E-002: light curtain interrupted during cycle.
- E-003: light curtain internal fault.
- E-004: muting timeout exceeded.
- E-005: safety relay PNOZ-1 fault.
- E-006: two-hand control timing violation.
- E-007: gate switch GS-1 open during cycle.
- E-008: mechanical safety block SB-1 or SB-2 not stowed.

### 7.2 Hydraulic faults E-020 to E-049

- E-020: low oil level in T-501 (LS-501 active).
- E-021: high oil level in T-501.
- E-022: oil temperature warning at 58 degrees C.
- E-023: oil temperature trip at 62 degrees C.
- E-024: filter F-411 clogged (CI-411 active).
- E-025: filter F-412 clogged.
- E-030: pump P-201 motor overload.
- E-031: pump P-202 motor overload.
- E-032: low pilot pressure at A-204.
- E-040: pressure transducer PT-301 fault.
- E-041: pressure transducer PT-203 fault.
- E-042: position transducer LT-501 fault.
- E-043: temperature transducer TT-501 fault.

### 7.3 Cooling faults E-050 to E-059

- E-050: low cooling water flow to CL-401.
- E-051: high differential pressure across CL-401.
- E-052: TS-401 outlet temperature high.
- E-053: SOL-411 solenoid feedback mismatch.

### 7.4 Process faults E-060 to E-079

- E-060: stroke time exceeded.
- E-061: pressing pressure not reached.
- E-062: top of stroke not reached.
- E-063: bottom of stroke overshoot.
- E-064: dwell drift exceeded.

### 7.5 Communication faults E-080 to E-099

- E-080: PROFINET remote IO loss.
- E-081: HMI loss.
- E-082: drive DRV-201 loss.
- E-090: SD card write failure.

## 8. Maintenance schedule

### 8.1 Daily checks

- Visual inspection of reservoir T-501 sight glass SG-501. Oil level must be within green band.
- Check oil temperature TT-501 reading at HMI; should be 38 to 55 degrees C during production.
- Verify no oil leaks at manifold M-301, cylinder C-501, and cooler CL-401 connections.
- Wipe down light curtain LC-FRONT-A and LC-FRONT-B sensor windows.
- Lubricate slide gibs and ways with ISO VG 220 way oil at points LP-1 through LP-8.
- Confirm air pressure at AP-1 reads 6 bar plus or minus 0.5 bar.

### 8.2 Weekly checks

- Lubricate pinion bearings B-701 and B-702 with one shot of NLGI 2 lithium complex grease (Mobilux EP 2 or equivalent).
- Inspect filter F-411 differential pressure indicator CI-411 reading at HMI Diagnostics.
- Test E-stop circuit by pressing each of ES-OP-1, ES-OP-2, ES-OP-3 in turn and verifying machine response.
- Check accumulator A-203 pre-charge with charging kit CHG-A203-K (target 90 bar).
- Inspect platen mounting bolts BLT-CYL-501-1 through BLT-CYL-501-12 for proper torque (450 Nm).

### 8.3 Monthly checks

- Drain a 250 mL oil sample from reservoir T-501 sample port SP-501 for ISO 4406 cleanliness analysis.
- Replace return filter cartridge F-411-CART (part HYD-F411-10M) if differential pressure exceeds 1.2 bar.
- Replace pressure filter cartridge F-412-CART (part HYD-F412-5M) if differential pressure exceeds 2 bar.
- Inspect light curtain alignment using SICK laser tool.
- Verify safety relay PNOZ-1 functional via test routine in HMI Maintenance screen.
- Clean cabinet CP-1 air filter AF-CP1.

### 8.4 Quarterly checks

- Recharge accumulator A-203 nitrogen if pre-charge has dropped below 85 bar.
- Inspect cooler CL-401 plate stack for fouling. Reverse-flush if differential pressure exceeds 1.5 bar.
- Calibrate pressure transducer PT-301 against reference gauge at TP-1.
- Calibrate position transducer LT-501 against mechanical scale at slide reference points.
- Inspect motor M-201 bearings for noise and vibration; record vibration baseline.

### 8.5 Annual maintenance

- Drain and replace reservoir T-501 oil charge (2400 L of ISO VG 46).
- Replace breather BR-501 desiccant cartridge.
- Replace all minor seal kits at manifold M-301 cartridge interfaces.
- Inspect cylinder C-501 piston seal HLT-605-800 and rod wiper MKL-PT2-800; replace as wear indicates.
- Megger test motor M-201 windings; minimum 1 megohm.
- Functional test of all 8 emergency stop circuits.
- Calibrate proportional valve PV-105 according to procedure CAL-PV105.
- Inspect counterbalance valve CBV-220 cartridge for spool wear.

## 9. Calibration procedures

### 9.1 CAL-PT301 pressure transducer calibration

1. Place machine in CALIBRATION mode (level 3 password).
2. Disconnect PT-301 from manifold M-301 test point TP-1.
3. Connect reference gauge RG-001 (DH-Budenberg, 0 to 250 bar, NIST traceable).
4. Apply pressure in 50 bar steps from 0 to 240 bar via manual pump.
5. Record HMI reading versus reference at each step.
6. Adjust offset and span at HMI Parameters screen if any reading deviates more than 1 percent.

### 9.2 CAL-LT501 position transducer calibration

1. Place machine in CALIBRATION mode.
2. Lower platen to mechanical hard stop and record LT-501 raw reading; this is REF-BOTTOM.
3. Raise platen to top mechanical stop and record raw reading; this is REF-TOP.
4. Enter both values at HMI Parameters screen, position calibration tab.
5. Verify intermediate position by jogging to 400 mm and measuring with calibrated steel rule.

### 9.3 CAL-PV105 proportional valve calibration

1. Place machine in CALIBRATION mode.
2. Use HMI direct command screen to step PV-105 from 0 to 100 percent in 10 percent increments.
3. Record PT-301 pressure at each command step.
4. Adjust valve null offset and span via HMI parameters until 0 percent command produces less than 5 bar and 100 percent command produces 220 bar plus or minus 2 bar.

## 10. Parts catalog

### 10.1 Hydraulic parts

- HYD-P201: pump P-201, Bosch Rexroth A4VSO 250 DRG.
- HYD-P202: pump P-202, Bosch Rexroth A10VSO 71.
- HYD-V101: directional valve V-101, Rexroth WEH25.
- HYD-PV105: proportional valve PV-105, Rexroth DBETR-10.
- HYD-RV110: relief valve RV-110, Rexroth DBDS6K1X/240.
- HYD-CBV220: counterbalance valve CBV-220, Rexroth FD16KA.
- HYD-POCV130: check valve POCV-130, Rexroth SV30PB1.
- HYD-F411-10M: filter cartridge F-411, 10 micron.
- HYD-F412-5M: filter cartridge F-412, 5 micron.
- HYD-A203: accumulator A-203, 50 L bladder.
- HYD-A204: accumulator A-204, 20 L bladder.
- HLT-605-800: piston seal kit for cylinder C-501.
- MKL-PT2-800: rod wiper kit for cylinder C-501.

### 10.2 Electrical parts

- ELE-PSU101: 24 VDC power supply, Phoenix QUINT4-PS/1AC/24DC/40.
- ELE-PLC-CPU: Siemens S7-1500 CPU 1516F-3 PN/DP.
- ELE-HMI: Siemens TP1500 Comfort.
- ELE-PNOZ1: Pilz PNOZ s7 safety relay.
- ELE-LC-A: SICK deTec4 Core, 1200 mm protective height.
- ELE-PT301: Hydac HDA 4445 pressure transducer.
- ELE-LT501: Balluff BTL7 magnetostrictive transducer, 1000 mm.
- ELE-TT501: Endress+Hauser TR10 RTD PT100.

### 10.3 Spare parts kit SPK-HP1200

Recommended on-site spares for 12 months operation:

- 2 each: F-411 cartridge.
- 2 each: F-412 cartridge.
- 1 each: PV-105 proportional valve.
- 1 each: RV-110 cartridge.
- 1 set: HLT-605-800 piston seal.
- 1 set: MKL-PT2-800 rod wiper.
- 1 each: PT-301 pressure transducer.
- 1 each: SOL-411 cooler bypass solenoid.
- 1 each: LC-FRONT-A or LC-FRONT-B light curtain.
- 1 each: PSU-101 24 VDC supply.

## 11. Cross-references

- Cooler loop CL-401: complete bill of materials, connection list, and wiring schedule on drawing CL-401 sheet 3 of 8 (DWG-CL401-S3).
- Electrical schematic for cabinet CP-1: ESCH-HP1200 sheets 4 through 7.
- Hydraulic schematic: HSCH-HP1200 sheet 1 (overall) and sheet 2 (manifold M-301 detail).
- Foundation drawing: FDN-HP1200-R2.
- Spare parts catalog: SPK-HP1200-R4.
- Recipe library backup procedure: PROC-HMI-BACKUP-R1.

## 12. Document history

- R7 (current): added cooler CL-401 fouling diagnostic to section 6.4, added fault code E-053.
- R6 (2024-03-12): updated PT-301 part number, added section 9.3 PV-105 calibration.
- R5 (2023-09-04): expanded section 2 safety system, added two-hand control description.
- R4 (2023-02-15): initial release for HP-1200 production fleet.
