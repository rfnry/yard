# Fault Code Quick Reference Card

Document number: QR-FC-2026-04. Revision: B. Owner: Plant Maintenance, Building 3. This card is intended for first-line technicians and shift leads. It lists the common fault codes raised by the line PLCs and HMIs across the south production floor, together with quick-action steps, pass/fail criteria for the recovery, and the on-call contact path when the issue cannot be cleared in the time budget below.

This card does not replace the OEM service manuals. When a code persists after the listed actions, escalate per the rules at the end of this document.

## How to use this card

1. Read the fault code from the HMI banner or from the alarm column of the line dashboard.
2. Locate the code in the section below that matches its prefix.
3. Follow the listed steps in order. Do not skip steps.
4. Apply the pass criteria. If the line returns to a normal run state and no related warning is active for ten minutes, treat the recovery as successful and log it.
5. If the recovery fails, escalate using the table at the bottom of this card. Do not attempt undocumented workarounds.

The expected time budget for a first-line recovery is fifteen minutes per fault. If you exceed that, escalate even if the code looks familiar.

## Code prefixes at a glance

- **E-0xx** electrical and control faults, including drives, contactors, safety relays.
- **H-1xx** hydraulic and lubrication faults.
- **P-2xx** pneumatic faults including air pressure, valves, regulators.
- **T-3xx** thermal faults including coolers, heaters, ambient excursions.
- **S-4xx** sensor and instrumentation faults.
- **Q-5xx** quality and process-window faults raised by the in-line gauges.
- **W-9xx** warnings only. These do not stop the line by themselves but they precede most stops if ignored.

## E-0xx Electrical and control

### E-001 main contactor did not pull in

1. Check that the local disconnect on the cabinet is in the on position.
2. Verify that the e-stop mushroom on the operator panel is released and twisted clear.
3. Press the control-power reset on the cabinet door and wait five seconds.
4. Re-arm from the HMI.

Pass: contactor audibly closes and the HMI reports control power healthy. Fail: contactor chatters or the HMI keeps the same code.

### E-004 servo drive overcurrent

1. Stop the line and remove the run permissive.
2. Cycle control power to the drive bay using the marked breaker. Wait ten seconds before re-energizing.
3. Inspect the driven axis for binding, debris, or a tool that has dropped into the path.
4. Re-arm. Run the axis at jog speed for one full stroke before resuming auto.

Pass: the drive completes the jog stroke without an overcurrent peak above seventy percent of rated. Fail: the code returns within two strokes.

### E-007 safety relay open

1. Walk the perimeter. Check every gate, light curtain, and rope pull. Reset any that you find tripped.
2. Verify nobody is inside the cell. Make eye contact with the operator before calling clear.
3. Press the safety reset button on the main panel, then the line reset.

Pass: safety chain healthy on the HMI and no rope-pull or gate icon highlighted. Fail: the chain still shows open after a complete walk.

### E-012 encoder fault on main axis

1. Stop the line. Open the encoder cover at the back of the gearbox.
2. Verify the cable strain relief is intact and the connector is fully seated.
3. Wipe the encoder window with a lint-free cloth. Do not use solvent.
4. Reseat the connector and re-arm.

Pass: position trace on the HMI is smooth and matches the commanded path within tolerance. Fail: position jumps or the code returns within one stroke.

### E-021 VFD overtemperature

1. Stop the line. Leave control power on so the drive fans keep running.
2. Inspect the cabinet filters. Replace if they are visibly loaded.
3. Confirm the cabinet door is closed and the gasket is intact.
4. Wait until the drive reports its heatsink under sixty degrees Celsius before clearing.

Pass: heatsink trends down for five consecutive minutes after the door is closed. Fail: heatsink stays above the trip point with the door shut and clean filters.

### E-033 communication loss to remote IO

1. Check the indicator LEDs on the affected remote IO block. A solid green link plus blinking activity means the cable is healthy.
2. If the link LED is off, reseat the patch cable at both ends.
3. If the activity LED is off, power-cycle the remote IO block from its local breaker.

Pass: HMI reports the IO block online and no inputs are stuck. Fail: the block stays offline or any input is stuck high after the cycle.

## H-1xx Hydraulic and lubrication

### H-101 low oil level in the main reservoir

1. Stop the line.
2. Read the sight glass directly. Do not trust only the float switch.
3. If the level is genuinely low, top up with the grade specified on the reservoir placard. Do not mix grades.
4. Check the floor and the return line for an external leak before resuming.

Pass: sight glass between the marks and no fresh oil on the floor. Fail: level keeps falling or there is visible oil under the unit.

### H-104 hydraulic oil overtemperature

1. Stop the line and leave the pump running on bypass if the unit supports it.
2. Verify the cooler fan or fan bank is running. Listen for a fan that is spinning slowly or is silent.
3. Check the cooler inlet screen for blockage. Clear with low-pressure air only.
4. Wait for the oil to drop below sixty degrees Celsius before resuming.

Pass: oil temperature trends down at half a degree per minute or better with the line idle. Fail: temperature rises or stays flat under no load.

### H-110 filter delta pressure high

1. The filter is loaded but not yet bypassing. The line can finish the current run if it is short.
2. At the next stop, change the affected element. Use the part number printed on the filter housing.
3. Bleed the filter housing per the maintenance card before resuming.

Pass: delta pressure drops below the warning threshold after the swap. Fail: delta pressure stays high with a fresh element, which indicates a downstream restriction.

### H-118 lube pump did not prime

1. Verify the lube reservoir is above the low mark.
2. Open the bleed screw on the pump housing until clean grease appears, then close.
3. Run a manual lube cycle from the HMI.

Pass: every distributor block in the train cycles within the expected window. Fail: a block does not move or the pump faults again on the same code.

## P-2xx Pneumatic

### P-201 supply pressure low

1. Read the pressure gauge at the line entry header. Compare to the placard target.
2. Walk the line and listen for a clearly audible leak. Tag the location, do not attempt a repair while the system is pressurized.
3. Drain any visible water from the filter bowl at the line entry.
4. If the supply is genuinely low, contact compressed-air services per the escalation table.

Pass: header pressure stable within the green band for at least five minutes. Fail: pressure droops under load or a leak is severe enough to be heard from a meter away.

### P-208 valve did not confirm position

1. Cycle the valve manually from the HMI service screen, two complete strokes.
2. Verify both position-sense reed switches show their state cleanly during the stroke.
3. If a sensor is intermittent, mark the valve for the next planned shift.

Pass: both directions confirm in under the configured timeout for two consecutive cycles. Fail: a position is missed or a sensor flickers.

### P-215 air dryer dewpoint alarm

1. Confirm the dryer is in a run state and not in regen.
2. Check the dryer dewpoint reading on its local panel.
3. If the reading is above the alarm threshold, contact compressed-air services. The line may continue at the discretion of the shift lead, but quality data must be flagged.

Pass: dewpoint trending down toward the normal band. Fail: dewpoint flat or rising.

## T-3xx Thermal

### T-301 cooler loop low flow

1. Verify the loop pump is running. Listen at the pump and read the local flow indicator.
2. Check the strainer at the loop inlet. Clean if loaded.
3. Confirm the bypass valve is in the operating position, not the maintenance position.

Pass: flow returns to the green band within two minutes of clearing the strainer. Fail: flow stays below the band or the pump cavitates.

### T-308 zone heater did not reach setpoint

1. Allow the zone its full warm-up time before declaring a fault. Many zones need fifteen minutes from cold.
2. Verify the heater contactor pulls in and the element draws current.
3. Inspect the thermocouple lead for damage.

Pass: zone within plus or minus two degrees of setpoint, holding for five minutes. Fail: zone drifts or the heater output is at one hundred percent without progress.

### T-315 ambient temperature out of range

1. This code reflects the cabinet or cell ambient, not the process.
2. Verify the cell exhaust fan is running.
3. If the plant is in a heat event, follow the hot-weather operations advisory issued by the plant.

Pass: ambient back inside the configured band. Fail: ambient continues to rise during normal operation.

## S-4xx Sensor and instrumentation

### S-401 vision sensor low contrast

1. Wipe the lens with a clean lens wipe.
2. Verify the part-presence light is on and aimed correctly.
3. Run a teach cycle on a known good part if the recipe allows it. If the recipe locks teaching, escalate.

Pass: contrast score above the recipe minimum on five consecutive parts. Fail: score floats around the threshold or fails on known good parts.

### S-407 thermocouple open

1. Inspect the lead from the connector head to the panel. A visibly broken lead is the most common cause.
2. Reseat the lead at both ends.
3. If the lead is damaged, replace as a unit. Do not splice.

Pass: live reading appears on the HMI and tracks the expected value during warm-up. Fail: reading remains at the open-circuit indication.

### S-412 load cell drift

1. Trigger a tare from the HMI with the platform empty.
2. Verify nothing is touching the load path.
3. Place the calibration check weight, confirm the reading within tolerance.

Pass: zero stable for five minutes and check weight reads within plus or minus half a percent. Fail: zero drifts or check weight is out of tolerance.

## Q-5xx Quality and process

### Q-501 dimension out of window

1. Stop pulling parts to finished goods. Quarantine the last ten parts.
2. Check the upstream tooling for visible wear or contamination.
3. Run a test cycle and re-measure off-line.

Pass: three consecutive parts inside the window after the corrective action. Fail: parts continue to drift or the dimension oscillates.

### Q-509 cycle time excessive

1. Confirm the recipe matches the part being run.
2. Look for a single station that is dwelling longer than its peers on the line balance display.
3. If a single station is the cause, focus there. Otherwise it is likely a utilities issue, see P-2xx and T-3xx.

Pass: cycle time within the green band for ten consecutive cycles. Fail: cycle time inflated or unstable.

## W-9xx Warnings to watch

These do not stop the line on their own but they precede stops. Treat any warning that has been active for an entire shift as a maintenance request.

- **W-901** filter delta pressure approaching limit. Plan the swap.
- **W-907** door interlock cycled more than expected this shift. Coach the operator if appropriate.
- **W-915** UPS on battery. Investigate before the next planned downtime.
- **W-923** network jitter elevated. Notify controls before the next shift.

## Escalation rules

Use the path below when the recovery time budget of fifteen minutes is exceeded, when the code repeats more than three times in a shift, or when any safety-related fault is involved. Always escalate immediately for any code that involves smoke, leaks of unknown fluid, or visible damage to a guard.

- **First-line maintenance**, ext. 4012, day shift only.
- **On-call maintenance**, pager 4099, after hours and weekends. Expect a callback within fifteen minutes.
- **Controls engineering**, ext. 4030, for any E-0xx that does not clear after one full power cycle.
- **Compressed-air services**, ext. 4055, for P-2xx that cannot be cleared at the line.
- **Plant safety**, ext. 4001, for any safety-relay event that recurs after a clean reset, or any incident with personnel involvement. Safety calls take precedence over production.
- **Shift lead**, radio channel 2, must be informed of any escalation before it leaves the floor.

When you call, have the following ready: the exact fault code, the line and station, the time of first occurrence, the count of recurrences, the steps you have already tried, and the current state of the line.

## Logging

Every fault that triggers an escalation must be entered in the maintenance log before the end of shift. Use the standard template referenced in document QR-LOG-2025-11. Include the fault code, action taken, who you escalated to, and the final state of the line at handover.

Closing reminder: this card is a starting point. If you are unsure, stop and call. A stopped line is recoverable. An undocumented workaround is not.
