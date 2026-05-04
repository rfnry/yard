# Vertical Machining Center MX-500 - Service Manual

Document number: SVC-MX500-R3. Supersedes revision R2 dated 2025-09-08. Applies to MX-500 units with serial numbers MX500-1102 through MX500-1487. Read in conjunction with mechanical drawing package DWG-MX500 sheets 1 through 6 and electrical schematic ESCH-MX500 sheets 1 through 9.

## 1. Overview and specifications

The MX-500 is a three-axis vertical machining center designed for high-speed milling of aluminum, mild steel, and stainless components up to 600 mm by 400 mm by 350 mm in envelope. The unit ships with the spindle drive, hydraulic clamping system, coolant loop, and 24-position automatic tool changer pre-assembled on the main casting.

### 1.1 Mechanical specifications

- X-axis travel: 600 mm.
- Y-axis travel: 400 mm.
- Z-axis travel: 350 mm.
- Rapid traverse rate: 36 m/min on X and Y, 24 m/min on Z.
- Feed rate range: 1 to 10000 mm/min.
- Spindle speed range: 60 to 12000 RPM.
- Spindle taper: BT-40.
- Tool changer capacity: 24 tools, side-mount carousel.
- Maximum tool weight: 7 kg.
- Maximum tool length: 250 mm.
- Maximum tool diameter: 90 mm.
- Table size: 800 mm by 420 mm.
- Maximum table load: 350 kg evenly distributed.

### 1.2 Spindle specifications

- Drive: Yaskawa SGM7G-13 servo, 13 kW continuous, 18 kW peak.
- Cooling: closed-loop oil cooling via plate exchanger CL-401, target spindle housing temperature 24 degrees C plus or minus 2 degrees C.
- Drawbar: hydraulic, 22 bar plus or minus 1 bar at idle, 38 bar plus or minus 2 bar during tool clamp.
- Encoder: Heidenhain ECN-1325, absolute, 18-bit.
- Lubrication: oil-air mist via metering unit ML-301, 0.03 mL per minute per bearing.

### 1.3 Electrical specifications

- Mains supply: 400 VAC, 3-phase, 50 Hz, 80 A service.
- Control voltage: 24 VDC supplied by power supply unit PSU-101 (Phoenix Contact QUINT4-PS/1AC/24DC/20).
- CNC controller: Fanuc 31i-B5, mounted in cabinet CP-1 slot 1.
- HMI: Fanuc 15-inch iHMI panel, mounted on swing arm SA-12 at the front of the column.
- Safety relay: Pilz PNOZ s7 controlling E-stop, door interlock, and spindle-orientation monitor.
- Servo amplifiers: three Yaskawa SGD7S units (X, Y, Z) plus one SGD7S for the spindle.

### 1.4 Site requirements

- Foundation: reinforced concrete pad minimum 400 mm depth, 30 MPa rating.
- Compressed air: 6 bar clean dry air, 150 NL/min peak demand at port AP-1.
- Cooling water for plate exchanger CL-401: 18 LPM at 18 to 25 degrees C.
- Ambient temperature: 5 to 35 degrees C, non-condensing humidity below 75 percent.
- Floor levelness: 0.05 mm per meter measured under each leveling pad.

## 2. Safety system

The MX-500 safety architecture is rated PL d Cat 3 according to ISO 13849-1. All safety components are pre-wired to terminal block TB-SAFE in cabinet CP-1 and cross-monitored by safety relay PNOZ-1.

### 2.1 Door interlock

The front door is monitored by a coded magnetic switch SICK MM12, redundant channels OSSD1 and OSSD2 wired to PNOZ-1 inputs S11/S12. With the door open, spindle rotation and axis motion are inhibited; jog at 2 m/min is permitted only with the enabling switch SW-EN held closed.

### 2.2 Emergency stop circuit

Three E-stop pushbuttons are installed:

- ES-OP-1 on the operator pendant.
- ES-OP-2 on the rear maintenance access door.
- ES-OP-3 on the cabinet CP-1 front door.

All three buttons are wired in series to the PNOZ-1 dual-channel inputs. Pressing any E-stop drops the safety relay output contacts within 25 ms, removes the run permissive from all four servo amplifiers, and engages the spindle holding brake within 80 ms.

### 2.3 Lockout and tagout

Before performing any maintenance involving the spindle cartridge, the tool changer mechanism, or the coolant manifold, follow this lockout sequence:

1. Park all axes at the home position via HMI Manual screen.
2. Press E-stop ES-OP-1.
3. Open main disconnect QS-1 on cabinet CP-1 and apply padlock and tag.
4. Open compressed-air shutoff SO-AP-1 and bleed line via vent VV-AP-1.
5. Close coolant shutoff valve BV-CL-1 at the coolant inlet.
6. Verify zero pressure at gauge G-301 on coolant manifold M-301.
7. Confirm spindle drawbar fully clamped before opening the spindle housing.

### 2.4 Spindle orientation monitor

In automatic tool change mode, the spindle must be at the M19-orient position (zero degrees plus or minus 0.05 degrees) before the tool changer arm engages. Orientation is monitored by encoder feedback and confirmed by proximity sensor PS-301 on the spindle drive train. Misorientation generates fault code F-415.

## 3. Spindle and drawbar

### 3.1 Spindle cartridge

The spindle cartridge SP-101 is a sealed unit containing the BT-40 taper, the hydraulic drawbar, the angular-contact bearing pack, and the integral oil-air lubrication ports. Cartridge replacement is a workshop-level task; field service is limited to drawbar pressure adjustment, bearing relubrication via the metering unit, and seal kit replacement at the rear gland.

- Bearing pack: NSK 7014 angular-contact, four bearings in DBB arrangement.
- Belleville stack: 32 discs, providing tool-clamp force at zero hydraulic pressure.
- Drawbar travel: 12 mm at the gripper end.
- Drawbar gripper: collet-style for BT-40 retention knob HSK-PUL-40.

### 3.2 Drawbar pressure adjustment

The hydraulic drawbar is fed from the auxiliary power pack PP-201 via line OL-DR. Two pressure setpoints apply:

- Idle (tool retained): 22 bar plus or minus 1 bar measured at gauge G-DR-1.
- Tool clamp / unclamp transition: 38 bar plus or minus 2 bar measured during the M06 cycle, monitored by pressure transducer PT-DR-2 on PLC analog input AI8.

To adjust idle pressure, engage MAINTENANCE mode (level 3 password), unlock relief valve RV-DR-1 at PP-201, turn the adjusting screw clockwise to increase pressure, and lock the screw with the captive nut. Verify at G-DR-1 with the spindle parked. Do not adjust under load.

### 3.3 Tool clamp force verification

Tool clamp force shall be verified annually using force-meter kit TCM-BT40 (Schunk part TCM-BT40-15K, range 0 to 15 kN). Target clamp force at 38 bar drawbar pressure is 12.0 kN plus or minus 0.5 kN. Below 11.0 kN, replace the Belleville stack (part SPK-BV-32) and re-verify. Above 13.0 kN, reduce drawbar pressure to bring force into target.

## 4. Coolant system

### 4.1 Coolant tank and pump

The coolant tank T-501 has a 220 L working capacity. Two pumps draw from it:

- LP-201: low-pressure flood coolant, 60 LPM at 4 bar, Grundfos CRN5-3.
- HP-202: high-pressure through-spindle coolant (TSC), 30 LPM at 70 bar, Grundfos MTH4-50.

The TSC pump HP-202 is interlocked with the drawbar clamp signal and only runs when a tool is fully clamped. Loss of clamp signal during a TSC cycle generates fault code F-512 and halts the pump within 200 ms.

### 4.2 Coolant filtration

Coolant returns from the work envelope to a chip conveyor CV-401 that drops solids into the chip bin. The pre-filtered coolant passes through:

- Magnetic separator MAG-411 at the tank inlet (removes ferrous particles).
- Bag filter BF-411, 25 micron rating, in housing FH-411.
- TSC fine filter F-422, 5 micron absolute, downstream of HP-202.

Bag filter BF-411 differential pressure shall be checked weekly. Replace cartridge BF-411-CART (part COOL-BF411-25M) if differential pressure across DPI-411 exceeds 1.0 bar.

### 4.3 Coolant concentration

The MX-500 ships configured for a 7 percent emulsion of the OEM-recommended semi-synthetic coolant (Blaser B-Cool 9665 or equivalent). Concentration shall be checked weekly using a refractometer; target reading 7.0 plus or minus 0.5 percent. Below 5 percent, top up with fresh emulsion at twice the working concentration to recover; above 9 percent, dilute with deionized water.

## 5. Axis drives

### 5.1 X-axis

- Servomotor: Yaskawa SGM7G-13DA, 13 kW, 1500 RPM.
- Ball screw: Hiwin HBN-40, 16 mm lead, C3 grade, length 750 mm.
- Linear guide: Hiwin HG-35-CA on twin rails, four blocks per rail.
- Position feedback: Heidenhain LC-181 linear scale, 1 nm resolution.
- Lubrication: central system, line LL-X1, 0.5 mL per cycle, every 30 minutes.

### 5.2 Y-axis

- Servomotor: Yaskawa SGM7G-13DA, 13 kW.
- Ball screw: Hiwin HBN-40, 16 mm lead, length 500 mm.
- Linear guide: same as X-axis.
- Position feedback: Heidenhain LC-181 linear scale.
- Lubrication: line LL-Y1.

### 5.3 Z-axis

- Servomotor: Yaskawa SGM7G-9DA, 9 kW, with integrated holding brake.
- Counterbalance: nitrogen cylinder CB-Z1, pre-charge 80 bar, vented through accumulator A-Z1.
- Ball screw: Hiwin HBN-32, 16 mm lead, length 450 mm.
- Linear guide: Hiwin HG-35-CA, twin rails, four blocks per rail.
- Position feedback: Heidenhain LC-181 linear scale.
- Lubrication: line LL-Z1.

The Z-axis counterbalance pressure shall be checked monthly. Below 70 bar, recharge using nitrogen cart NCK-MX500. The pre-charge directly affects the apparent weight of the spindle head and therefore the servo following error during rapid moves.

## 6. Common faults and troubleshooting

### 6.1 Spindle slow to reach commanded speed

Symptom: spindle ramp-up takes longer than the recipe target; cycle time inflated; encoder error increases above 50 counts during ramp.

Diagnostic steps, in order:

1. Verify drawbar pressure at G-DR-1 reads 22 bar plus or minus 1 bar at idle. Below 21 bar indicates leak in line OL-DR or worn seal kit at the drawbar gland.
2. Check spindle cooling oil temperature at TS-401 (HMI Diagnostics screen). Target 24 degrees C plus or minus 2 degrees C. Above 28 degrees C indicates fouling at plate exchanger CL-401 or low coolant flow at FS-401.
3. Inspect spindle drive amplifier diagnostics for trip warnings. The Yaskawa SGD7S records the last 10 alarms with timestamps.
4. Verify spindle motor current against load monitor: target steady-state at 12000 RPM no-load is 8 to 10 amps; values above 14 amps indicate bearing drag or seized bearing.
5. Check lubrication metering unit ML-301: each bearing port should pulse once per 30 minutes. Missed pulses on the count register indicate an empty oil reservoir or a pinched air-mist line.

### 6.2 Spindle housing overtemperature

Symptom: TS-401 reading climbs above 28 degrees C during normal cutting; warning W-411 triggers at 30 degrees C; fault F-411 trips at 35 degrees C.

Diagnostic steps:

1. Verify cooling water flow to CL-401 is at least 15 LPM. Read at flow switch FS-401; the contact closes above 12 LPM and opens below 8 LPM.
2. Confirm bypass solenoid SOL-411 (PLC output Q3.7) energizes when commanded. Manually pulse from HMI Manual screen.
3. Inspect plate exchanger CL-401 for fouling. Differential pressure across DPI-401 above 1.5 bar indicates plate stack needs reverse-flush or chemical cleaning.
4. Sample the coolant oil for water content. Above 500 ppm reduces heat transfer measurably.
5. Verify ambient at the cell. CL-401 capacity falls when inlet water exceeds 25 degrees C.

Refer to drawing CL-401 sheet 3 of 8 for complete cooler loop service procedure.

### 6.3 Drawbar pressure drift

Symptom: G-DR-1 idle reading drifts below 21 bar over a single shift; tool retention warning W-512 may trigger.

Diagnostic steps:

1. Inspect line OL-DR fittings at the drawbar gland for visible weeping. A drop forming in 30 minutes equals approximately 0.5 bar per shift.
2. Check pump PP-201 reservoir level; below the low mark indicates an external leak or a bypass leak at relief RV-DR-1.
3. Replace seal kit SPK-DR-22 at the drawbar gland (workshop-level task).
4. Verify accumulator A-DR-1 nitrogen pre-charge at 18 bar via charging kit CHG-A-DR.

### 6.4 Tool changer arm misorientation

Symptom: M06 hangs in the tool change cycle; fault F-415 (spindle orientation tolerance exceeded) is logged.

Diagnostic steps, in order:

1. Confirm proximity sensor PS-301 on the spindle drive train signals correctly when the spindle is jogged to the M19 orient position. The HMI Diagnostics screen shows the input live state.
2. Verify the spindle encoder Heidenhain ECN-1325 has not lost its absolute reference. A loss requires re-homing per procedure HOME-SP-101.
3. Inspect the orient-position cam on the spindle drive train for damage or contamination.
4. Check the M19 commanded angle in the recipe; a corrupted recipe can request an angle outside the tool changer's accept window.

### 6.5 Coolant pressure low at TSC nozzle

Symptom: through-spindle coolant pressure measured at gauge G-CL-2 reads below 60 bar during a TSC-enabled cycle; warning W-512 may trigger.

Diagnostic steps:

1. Replace TSC fine filter cartridge F-422-CART (part COOL-F422-5M) if differential pressure at DPI-422 exceeds 1.5 bar.
2. Verify HP-202 motor current is within nameplate. A pump that is bypassing internally may run at low current with no useful output.
3. Inspect TSC line for kinks where it wraps around the spindle housing.
4. Confirm tool retention knob HSK-PUL-40 is the correct part for through-spindle coolant; non-TSC retention knobs block the coolant path and produce identical symptoms.

## 7. Fault code reference

Fault codes are grouped by subsystem. Full list maintained in document FCL-MX500-R2.

### 7.1 Safety faults F-001 to F-019

- F-001: emergency stop pressed.
- F-002: door interlock open during cycle.
- F-003: enabling switch SW-EN released during open-door jog.
- F-005: safety relay PNOZ-1 fault.
- F-007: spindle holding brake feedback mismatch.

### 7.2 Spindle faults F-400 to F-419

- F-401: spindle drive amplifier overcurrent.
- F-403: spindle encoder loss of signal.
- F-411: spindle housing overtemperature trip at 35 degrees C.
- F-412: spindle drawbar pressure low (G-DR-1 below 18 bar).
- F-413: spindle drawbar pressure high (G-DR-1 above 25 bar at idle).
- F-415: spindle orientation tolerance exceeded.
- F-416: spindle holding brake did not release.

### 7.3 Coolant faults F-500 to F-529

- F-501: coolant tank low level.
- F-503: bag filter BF-411 clogged.
- F-505: coolant concentration out of range.
- F-512: TSC pump HP-202 ran without drawbar clamp signal.
- F-514: TSC pressure low (G-CL-2 below 50 bar during commanded cycle).

### 7.4 Axis faults F-600 to F-649

- F-601: X-axis following error exceeded.
- F-602: Y-axis following error exceeded.
- F-603: Z-axis following error exceeded.
- F-611: Z-axis counterbalance pressure low.
- F-621: linear scale Heidenhain LC-181 communication loss (any axis).

### 7.5 Tool-changer faults F-700 to F-719

- F-701: tool changer arm not at home position.
- F-703: tool pocket sensor mismatch.
- F-705: tool clamp confirmation timeout.

## 8. Maintenance schedule

### 8.1 Daily checks

- Visual inspection of coolant tank T-501 sight glass; level must be within green band.
- Confirm coolant concentration at refractometer; target 7.0 plus or minus 0.5 percent.
- Check air pressure at AP-1 reads 6 bar plus or minus 0.5 bar.
- Verify chip conveyor CV-401 runs cleanly and discharges into the bin.
- Inspect spindle housing temperature TS-401 at HMI; target 24 degrees C plus or minus 2 degrees C during cutting.

### 8.2 Weekly checks

- Read bag filter BF-411 differential pressure DPI-411. Replace cartridge if above 1.0 bar.
- Verify Z-axis counterbalance pressure at gauge G-CB-Z1; target 80 bar minimum.
- Test E-stop circuit by pressing each of ES-OP-1, ES-OP-2, ES-OP-3 in turn and verifying machine response.
- Inspect tool retention knobs in the carousel for wear or contamination.
- Lubricate tool changer arm pivot at grease nipple LP-TCA, one shot of NLGI 2 grease.

### 8.3 Monthly checks

- Replace bag filter cartridge BF-411-CART regardless of DPI reading.
- Replace TSC fine filter cartridge F-422-CART regardless of DPI reading.
- Drain a 100 mL coolant sample from sample port SP-501 for laboratory analysis (pH, concentration, biocount).
- Verify drawbar idle pressure at G-DR-1 reads 22 bar plus or minus 1 bar.
- Inspect linear scale carrier seals on X, Y, Z for coolant ingress.

### 8.4 Quarterly checks

- Recharge Z-axis counterbalance nitrogen if pre-charge has dropped below 75 bar.
- Calibrate spindle drawbar pressure transducer PT-DR-2 against reference gauge.
- Inspect spindle bearings for noise and vibration; record vibration baseline at 6000 RPM no-load.
- Reverse-flush plate exchanger CL-401 if differential pressure exceeds 1.5 bar.
- Verify tool clamp force using force-meter kit TCM-BT40 (target 12.0 kN at 38 bar).

### 8.5 Annual maintenance

- Drain and replace coolant tank T-501 fill (220 L of 7 percent semi-synthetic emulsion).
- Replace breather BR-501 desiccant cartridge.
- Megger test servo motor windings for X, Y, Z, and spindle; minimum 1 megohm.
- Functional test of all three E-stop circuits.
- Replace seal kit SPK-DR-22 at the drawbar gland.
- Replace lubrication metering unit oil charge.
- Calibrate linear scales on X, Y, Z against laser interferometer.

## 9. Calibration procedures

### 9.1 CAL-DR-1 drawbar pressure calibration

1. Place machine in MAINTENANCE mode (level 3 password).
2. Park spindle.
3. Connect reference gauge RG-001 at test point TP-DR-1 in parallel with G-DR-1.
4. Adjust relief valve RV-DR-1 until the reference gauge reads 22.0 bar.
5. Lock the adjusting screw with the captive nut.
6. Cycle a tool change (M06) and verify peak pressure at PT-DR-2 reaches 38 bar plus or minus 2 bar during the unclamp transition.

### 9.2 CAL-CB-Z1 Z-axis counterbalance calibration

1. Park Z-axis at the home position.
2. Connect nitrogen cart NCK-MX500 at charging port CP-Z1.
3. Open isolation valve BV-CB-Z1.
4. Charge nitrogen until gauge G-CB-Z1 reads 80 bar plus or minus 1 bar.
5. Close BV-CB-Z1 and disconnect the cart.
6. Run Z-axis through full travel at rapid traverse and verify following error stays under 30 counts in either direction.

## 10. Parts catalog

### 10.1 Spindle and drawbar

- SP-101: spindle cartridge assembly, MX-500 BT-40, FANUC-built. Workshop-only.
- SPK-DR-22: drawbar seal kit, gland diameter 22 mm.
- SPK-BV-32: Belleville stack, 32 discs.
- TCM-BT40-15K: tool clamp force meter kit.
- HSK-PUL-40: tool retention knob, BT-40, through-spindle-coolant compatible.

### 10.2 Coolant

- COOL-BF411-25M: bag filter cartridge, 25 micron.
- COOL-F422-5M: TSC fine filter cartridge, 5 micron.
- COOL-MAG411: magnetic separator media.
- COOL-RFR: refractometer.

### 10.3 Electrical

- ELE-PSU101: 24 VDC power supply, Phoenix QUINT4-PS/1AC/24DC/20.
- ELE-CNC-FANUC: Fanuc 31i-B5 CNC controller.
- ELE-PNOZ1: Pilz PNOZ s7 safety relay.
- ELE-SGD7S-13: Yaskawa SGD7S amplifier, 13 kW frame.
- ELE-LC181: Heidenhain LC-181 linear scale.

### 10.4 Recommended on-site spares (kit SPK-MX500)

- 2 each: BF-411 cartridge.
- 2 each: F-422 cartridge.
- 1 set: SPK-DR-22 drawbar seal kit.
- 1 each: PSU-101.
- 1 each: HP-202 TSC pump rebuild kit.
- 4 each: HSK-PUL-40 retention knob.

## 11. Cross-references

- Coolant cooler loop CL-401: full bill of materials, connection list, and wiring schedule on drawing CL-401 sheet 3 of 8 (DWG-CL401-S3).
- Spindle cartridge mechanical drawing: DWG-MX500 sheet 1.
- Tool changer mechanism: DWG-MX500 sheet 4.
- Cabinet CP-1 wiring: ESCH-MX500 sheets 3 through 6.
- Safety circuit: ESCH-MX500 sheet 7.
- Foundation drawing: FDN-MX500-R1.
- Recipe library backup procedure: PROC-FANUC-BACKUP.

## 12. Document history

- R3 (current, 2026-04-02): added section 6.5 TSC pressure low diagnostic; updated F-512 description for the drawbar interlock change in firmware 31i-B5 v8.4.
- R2 (2025-09-08): added Z-axis counterbalance check to monthly schedule; updated F-611 description.
- R1 (2025-01-14): initial release for MX-500 production fleet.
