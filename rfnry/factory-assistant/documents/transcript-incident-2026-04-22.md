# Meeting Transcript - MX-500 Line 3 Incident Review (2026-04-22)

Document number: TR-INC-2026-04-22. Author: Plant Maintenance, Building 3. Status: closed, root cause confirmed, action items tracked under work-order WO-26-1184. Distribution: shift leads, controls engineering, OEM service contact.

This transcript captures the incident review meeting held the day after a recurring fault on MX-500 unit serial MX500-1331 produced four unscheduled stops on second shift. The unit is on the south production floor, line 3, station 4. Timestamps are approximate; the meeting was recorded on the cell-area microphone and transcribed by the plant transcription service. Names are anonymized to role labels per company policy.

## Attendees

- **SHIFT-LEAD-2** (second-shift lead, line 3)
- **TECH-A** (first-line technician, line 3)
- **TECH-B** (first-line technician, swing shift)
- **CONTROLS-ENG** (controls engineering, on-call rotation)
- **MAINT-LEAD** (maintenance lead, Building 3)
- **OEM-CSE** (OEM customer service engineer, dialed in)

## Transcript

### 09:00 — opening

**MAINT-LEAD:** OK we're recording. This is the incident review for MX500-1331 last night, second shift. Four stops between 18:00 and 23:30. Let's go through the timeline first then root cause.

**SHIFT-LEAD-2:** Sure. First stop was at 18:14. F-411 popped on the HMI banner. Spindle housing overtemperature. TECH-A was at the cell.

**TECH-A:** Yeah I was over there for tooling on station 5 actually, station 4 went down right next to me. The HMI said F-411, I went through the card. The card says check coolant water flow at FS-401, check the bypass solenoid, check plate fouling.

**MAINT-LEAD:** And what did you find?

**TECH-A:** Flow looked fine. The local indicator at FS-401 was reading like 16 LPM, well above the threshold. SOL-411 was energized, I could hear it. So I went to the plate. DPI-401 was reading half a bar, no fouling. So I cleared it and we ran again.

**MAINT-LEAD:** OK and how long until the second stop.

**SHIFT-LEAD-2:** Forty minutes. 18:54. Same code.

**TECH-A:** Same thing. I went through the card again, same readings. We cleared it again, ran for about twenty minutes, F-411 again.

**MAINT-LEAD:** When did you escalate?

**TECH-A:** Third stop. I called SHIFT-LEAD-2 and we paged on-call.

### 09:08 — what controls found

**CONTROLS-ENG:** I came in at like 21:15. By that point they'd cleared it three times. I pulled the trace from the controller. Spindle housing temp was tracking 26, 27 degrees C steady. So the temperature wasn't actually high. The fault was firing without the temperature being high.

**TECH-B:** That's what I told you on the phone right? The number on the HMI looked normal.

**CONTROLS-ENG:** Right. So I started looking at the input chain. TS-401, TS-402, AI6, AI7. AI6 was reading 27 degrees, AI7 was reading 26 degrees, no issue. But the fault logic was reading from a different input.

**MAINT-LEAD:** Different input?

**CONTROLS-ENG:** Yeah. The firmware on this unit was upgraded in March. 31i-B5 v8.4. The upgrade moved the F-411 fault source from AI6 to a derived signal that combines AI6 with the FS-401 flow switch state. So the fault can fire on either temperature OR loss of flow.

**OEM-CSE:** That's correct, that's part of the v8.4 change. F-411 used to be temperature-only. Now it's a combined safety condition. The release notes called it out.

**SHIFT-LEAD-2:** The release notes are not on the wall card.

**OEM-CSE:** Right. We didn't push a card update.

**MAINT-LEAD:** OK so we have a fault code that means two things now and our card only tells the technician about one of them. Got it. Keep going.

### 09:15 — narrowing down

**CONTROLS-ENG:** So if temperature wasn't high, the other branch is FS-401. I went to look at FS-401. The contact was reading closed. So the PLC was seeing flow. But the trace showed FS-401 was bouncing — it was opening for like 80 to 120 milliseconds at random intervals, then closing again. That's faster than the technician would notice on the local indicator. But the PLC was latching it.

**TECH-A:** I never saw it open. The light on the cabinet was solid green every time I looked.

**CONTROLS-ENG:** Right, the panel light has a debounce. But the fault logic reads the raw input. So the bounce was firing the fault.

**OEM-CSE:** What's the fault dwell?

**CONTROLS-ENG:** 100 milliseconds. So a single 120-millisecond open is enough.

### 09:21 — actual root cause

**CONTROLS-ENG:** I went to the cooler and watched FS-401. The flow was steady on the local indicator. So the question is why the contact was bouncing if the flow was OK.

**MAINT-LEAD:** Bad sensor.

**CONTROLS-ENG:** That was my first guess. I swapped the FS-401 with a spare. Same behavior. So it's not the sensor.

**TECH-B:** Wiring?

**CONTROLS-ENG:** I checked the wiring. SIG-FS401 from FS-401 to TB-DI terminal 18. Cable looked fine, terminations clean. Continuity good. But here's the thing — the cable runs in tray CT-3 right next to PWR-M301, the motor cable for the cooler pump.

**MAINT-LEAD:** And?

**CONTROLS-ENG:** PWR-M301 was repulled in February when they replaced the M-301-MOT motor. The new pull put PWR-M301 directly against SIG-FS401 for about three meters. The drawing calls for separation, but whoever pulled it didn't follow the drawing.

**SHIFT-LEAD-2:** So the motor cable was inducing on the signal cable.

**CONTROLS-ENG:** Yes. The bouncing was VFD switching noise coupling into the FS-401 contact circuit. It only showed up on this unit because the cable separation was wrong.

**OEM-CSE:** That tracks. The flow switch contact circuit is dry, it's susceptible to coupled noise if the separation isn't maintained.

### 09:30 — corrective action

**MAINT-LEAD:** OK. So the fix is repull PWR-M301 to follow the drawing.

**CONTROLS-ENG:** Right. Or add ferrite beads on PWR-M301 at both ends if the repull isn't practical.

**MAINT-LEAD:** Repull is the right fix. Schedule that for next planned downtime. WO-26-1184. TECH-B can you own that.

**TECH-B:** Yeah, I'll write it up.

**MAINT-LEAD:** OK. And let's talk about the documentation problem.

### 09:33 — documentation gap

**SHIFT-LEAD-2:** The card says check flow, check solenoid, check fouling. It doesn't say "the fault might be firing because the contact is bouncing even though flow is fine." The technician went through every step on the card and got nothing.

**TECH-A:** I cleared it three times because I thought it was a transient.

**MAINT-LEAD:** Right. We need to update the card. Add a step: "if all three checks pass and the fault keeps recurring, escalate to controls — the fault may be triggered by FS-401 bouncing rather than actual flow loss."

**CONTROLS-ENG:** And we should call out the v8.4 firmware change. F-411 is now a combined fault. That's not on the card anywhere.

**MAINT-LEAD:** Yeah. OK so two card updates: combined fault description and the bouncing-contact escalation. CONTROLS-ENG can you write the language and send it to me. I'll route it through the maintenance documentation review.

**CONTROLS-ENG:** I can have it by Friday.

### 09:38 — fault code disambiguation

**OEM-CSE:** While we're on documentation. There's another disambiguation issue I want to raise. F-413.

**MAINT-LEAD:** F-413 is drawbar pressure high.

**OEM-CSE:** That's the older firmware. In v8.4 F-413 was reassigned to the cooler bypass solenoid feedback mismatch. The drawbar pressure high fault moved to F-414.

**SHIFT-LEAD-2:** That's bad.

**OEM-CSE:** I know. The fault code list document FCL-MX500-R2 hasn't been updated for v8.4. We're working on it. R3 will reflect the changes.

**MAINT-LEAD:** When?

**OEM-CSE:** End of May. I can send a preview if it would help.

**MAINT-LEAD:** Yes please. Send me a preview, I'll cross-reference against our cards and get any updates queued.

### 09:42 — cooler service status

**MAINT-LEAD:** While we have you OEM-CSE. The cooler on this unit, CL-401, was reverse-flushed in March. Quarterly cleaning. We saw 0.5 bar at DPI-401 last night, so the plate stack is fine. But the gaskets are EPDM and we're due for the annual replacement next month. Are we still on AL-M3FG-30 gaskets or did the part number change?

**OEM-CSE:** AL-M3FG-30 is current. But I want to flag — we've had two reports this quarter of EPDM gaskets failing early on units running coolant concentration above 8 percent. If your coolant is running hot in concentration, consider FKM. Part number AL-M3FG-30-FKM. It's a drop-in.

**MAINT-LEAD:** Our concentration target is 7 plus or minus 0.5. We log it weekly. We've been within band for at least a year.

**OEM-CSE:** Then EPDM is fine for you. Just wanted to flag it.

### 09:48 — action items recap

**MAINT-LEAD:** OK let's recap. Action items.

1. TECH-B — repull PWR-M301 to follow drawing CL-401 sheet 3 separation requirements. Next planned downtime. Work order WO-26-1184.
2. CONTROLS-ENG — write update for the F-411 quick-reference card. Add the v8.4 combined-fault description and the bouncing-contact escalation step. Deliver to MAINT-LEAD by Friday 2026-04-25.
3. OEM-CSE — send preview of FCL-MX500-R3 to MAINT-LEAD by Friday 2026-04-25.
4. MAINT-LEAD — route card update through maintenance documentation review and post on all line 3 cell walls within two weeks of receiving CONTROLS-ENG's draft.
5. SHIFT-LEAD-2 — log the four stops in the maintenance log against unit MX500-1331 and reference WO-26-1184 and TR-INC-2026-04-22.

**MAINT-LEAD:** Anything else.

**TECH-A:** Yeah. The card is going to be longer now. Can we keep it on one page?

**MAINT-LEAD:** We'll try. CONTROLS-ENG, lean on the language.

**CONTROLS-ENG:** Will do.

**MAINT-LEAD:** OK we're done. Thanks everyone.

### 09:51 — meeting end

## Action item summary

- **WO-26-1184**: repull PWR-M301 cable on MX500-1331 to maintain separation from SIG-FS401 per drawing DWG-CL401-S3-MX500. Owner TECH-B. Due next planned downtime.
- **DOC-26-091**: update the F-411 quick-reference card to reflect v8.4 firmware combined-fault behavior and add the bouncing-contact escalation step. Owner CONTROLS-ENG. Draft due 2026-04-25.
- **DOC-26-092**: cross-reference FCL-MX500-R3 preview against existing cards once OEM-CSE delivers. Owner MAINT-LEAD. Due two weeks from preview receipt.

## Notes

- The transcript-mentioned drawing DWG-CL401-S3-MX500 specifies cable separation between PWR-M301 and SIG-FS401 in section 4 of that sheet. The drawing has not been violated by design — only by the February repull. The drawing remains authoritative.
- The transcript-mentioned firmware v8.4 of the Fanuc 31i-B5 controller changed the source of fault F-411 from a temperature-only condition to a combined temperature-or-flow condition. The MX-500 service manual section 7.3 and the in-house quick-reference card both predate this change. Until both are updated, technicians should treat any recurring F-411 with normal cooling temperature as a candidate for the bouncing-contact root cause and escalate per action item DOC-26-091.
- The disambiguation of fault code F-413 between drawbar pressure high (older firmware) and cooler bypass solenoid feedback mismatch (v8.4) is an open documentation issue. The MX-500 service manual section 6.2 contains the older description and is not yet updated.
