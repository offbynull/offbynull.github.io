```{title}
3D Printing
```

```{toc}
```

# H2S Environment

H2SPrinter must be ...

 * placed on a flat and stable surface.

 * operated within temperatures between 15-30C (60-85F).

   If the temperature is ...

    * < 15C, there may be issues with adhesion to plate and / or weaken layer bonding
    * \> 30C, there filament may soften before reaching hotend, increasing risk of extruder or nozzle clogs.

   The H2S comes with an "active exhaust fan" to blow out hot air (and fumes), but in warmer climates that may not be enough. The operating space recommended is 80cm width x 102cm depth x 105cm height, which covers the space required in the back for the exhaust and the AMS 2 Pro to sit on top. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/224`

   ```{note}
   The active exhaust fan is different from the top vent. The exhaust is in the back, and apparently there are filters involved with it.
   ```

# H2S Auto-calibration

H2S's auto-calibration process attempts to adjust machine parameters. The main aspects that are calibrated are ...

 * bed leveling.
 * motor noise cancellation.
 * vibration compensation.

```{note}
It sounds like if you have additional modules, auto-calibration performs more work (e.g., vision encoder).
```

Trigger auto-calibration manually by navigating to **[Wrench Icon]** → **Settings** → **Calibration**. Perform auto-calibrate whenever ...

 * there's a decrease in print quality.
 * after printer maintenance.
 * after firmware updates (recommended but not required). `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/224`

# H2S Filament Loading

Filament can be loaded through either the AMS 2 Pro or the external spool holder. The external spool holder is used when ...

 * an AMS 2 Pro isn't attached to the printer.
 * the filament spool is oversized for the AMS 2 Pro.
 * the filament spool is for a material the AMS 2 Pro doesn't support (but the printer does).
 * the filament spool is from an unsupported third-party. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/225`

```{note}
The source doesn't cite this, but I know for a fact that TPU is not supported by the AMS 2 Pro and must fed via the external spool holder (unless it's specifically branded as TPU for AMS, which Bambu Lab sells). 
```

To load filament using the AMS 2 Pro, ...

1. open the two tabs on the front edge and lift the cover.
1. stick the filament spool into one of the four slots, ensuring that it sits on the slot's roller and rotates freely.
1. push the slot's inlet release tab toward the spool and feed filament into that inlet - inlet will automatically grip and pull in filament.
1. close the cover and lock it in by closing the two tabs on the front edge.
1. select filament properties: 
   * For filament from Bambu Lab filament, filament color and  material should be automatically detected (using RFID).
   * For filament not from Bambu Lab, navigate to **[Spool Icon]** → **[Pencil Icon]** (for the slot spool was added to) and select filament brand, material, and color.

`{bm-disable-all}`

![AMS 2 Pro top diagram](ams2.drawio.svg)

`{bm-enable-all}`

To load filament using the external spool holder, ...

1. place filament on external spool holder, where filament tip faces up.
1. push filament through PTFE tube until you feel resistance (should reach into printer's extruder).
1. load filament into extruder:
   1. navigate to **[Spool Icon]** and ensure extruder icon is green (confirms filament reaches extruder).
   1. tap the external spool, then select filament brand, material, and color, then tap **Confirm**.
   1. tap **Load** (pulls filament into extruder).
1. inspect as loading process performs a sample extrusion:
   * Tap **Filament Extruded, Continue** if extrusion is thin, even, and steady line free from gaps and sputtering.
   * Tap **Not Extruded Yet, Retry** and gently push filament further into PTFE tube (to help extruder grip it) if extrusion doesn't happen, happens in blobs, or extrusion curls instead of dropping freely.

![External spool diagram](external%20spool.drawio.svg)

`{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/225`

# H2S User Interface

Along left-side of the UI are 5 options, each represented by an icon:

1. **[Home]**: Primary functions and readings (e.g., triggering prints, sensor readings, WiFi status, and statistics).
2. **[Controls]**: Control panel for hardware settings (e.g., fan speed, nozzle and heatbed temperature, light, speed, and motion).
3. **[Filaments]**: Control panel for filament management (e.g., AMS 2 Pro functionality and manually selecting filament material and color).
4. **[Settings]**: Control panel for printer calibration as well as system and identity settings (e.g., account information, WiFi, firmware, and USB).
5. **[Health Monitoring System]**: Printer diagnostics. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

## Print Calibration

To calibrate the printer, navigate to **[Settings]** → **Calibration** → **Print Calibration**, select the desired calibrations and hit **Start**. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

## Print

To print, navigate to **[Home]** → **Print Files** and select the drive and file to load. Two drives should be present:

 * **Internal**: Files preloaded onto the printer's internal memory.
 * **USB**: Files on USB drive plugged into the printer.

One a file is chosen, select the appropriate **Plate** and **Nozzle** (H2S comes with "Texture PEI" plate and "0.4mm Standard" nozzle - these should be selected as defaults). Then, hit **Next** select the filament to print with. Then, hit **Print** to begin printing. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

## Print Speed

To configure the printing speed, navigate to **[Controls]** → **Speed** and select either **Silent**, **Standard** (default), **Sport**, or **Ludicrous**. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

```{note}
An introductory YouTube video I watched mentioned that the faster the speed is, the lower quality the print will be. Some people are willing to accept lower quality prints in exchange for speed.
```

## Printhead and Heatbed Movement

To perform movements of the printhead (XZ axis) and heatbed (Y axis), navigate to **[Controls]** → **Motion** and tap the adjustment buttons as necessary. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

```{note}
This seems to only be for testing purposes and moving things to get at parts? I had to use this feature to get at a thin piece of plastic that popped off and fell on the bottom of the printer. I moved the heatbed up so I could fit my hand in and reach it.
```

## Extruder Movement

To perform adhoc extrusion and retraction of filament, navigate to **[Controls]** → **Nozzle & Extruder** and use the up/down buttons under **Extruder**. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

```{note}
This seems to be for testing purposes. But also, does this have to be done when swapping between AMS 2 Pro and manual spool feeding?
```

## Nozzle Type

When nozzle has been swapped, navigate to **[Controls]** → **Nozzle & Extruder** and select the nozzle's type under **Nozzle**. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

## Nozzle Temperature

To set the nozzle's temperature, navigate to **[Controls]** → **Nozzle & Extruder** and select the nozzle's temperature under **Nozzle**. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

```{note}
This seems to only be for testing purposes and doesn't apply to any prints? AFAIK initiating a new print should unset this as the print needs specific temperatures based on the print and the filament used.
```

## Heatbed Temperature

To set the heatbed's temperature, navigate to **[Controls]** → **Heatbed** and select the temperature. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

```{note}
This seems to only be for testing purposes and doesn't apply to any prints? AFAIK initiating a new print should unset this as the print needs specific temperatures based on the print and the filament used.
```

## Chamber Temperature

To set the chamber's temperature, navigate to **[Controls]** → **Chamber** and select the temperature. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

```{note}
This seems to only be for testing purposes and doesn't apply to any prints? AFAIK initiating a new print should unset this as the print needs specific temperatures based on the print and the filament used.
```

## Chamber Light

To turn the chamber's light on/off, navigate to **[Controls]** and toggle the **Light** switch. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

## Heating and Cooling

To configure the printer's internal climate, navigate to **[Controls]** → **Air Condition** and select either **Cooling** or **Heating**. Individual parts that control the climate (e.g., fans, heaters, and exhausts) are listed and can be individually controlled. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

When the mode is set to ...

 * cooling, the chamber heat circulation fan remains off and the filter switch flap is positioned down. Cooling mode should be used for filaments that have low heat resistance (e.g. PLA and TPU).
 * heating, the chamber heat circulation fan automatically turns on, the auxiliary part cooling fan remains off, and the filter switch flap is positioned up. Heating mode should be used for filaments with high heat resistance (e.g., ABS, ASA, PC, and PA). `{ref} https://wiki.bambulab.com/en/h2/manual/cooling-fan-system`

## Filament Type

To select which filaments are in the AMS 2 Pro and / or external spool holder, navigate to **[Filament]** and select the desired spool to input the spool's type, color, and manufacturer. Bambu Lab filaments come with RFID that allows the AMS 2 Pro to automatically identify material and color. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

## Filament Auto Refill

When a filament runs out, the printer and attached AMS 2 Pro unit automatically swap to a second spool to continue printing, provided that second spool has the same brand, color, and material of the original spool being printed with. To enable auto refill, navigate to **[Settings]** → **AMS Options** and select **AMS Auto-Refill**. . Then, navigate to **[Filament]**, select the wrench icon, and select **Auto Refill** to view refill relationships. `{ref} https://wiki.bambulab.com/en/ams-2-pro/manual/setup-and-printting#ams-auto-refill`.

```{note}
On the H2D, there are 2 extruders (left and right) and apparently each of the H2D's AMS 2 Pro units is assigned to one of these heads (there may be multiple AMS 2 Pros per printer). The second spool must be in an AMS 2 Pro unit assigned to the same extruder for auto refill to use it.
```

## Filament Drying

To dry filament, ensure the spool is loaded into the AMS 2 Pro and navigate to **[Filament]** and find the water droplet icon. Below the icon should be a humidity sensor reading. Select the water droplet icon and either ...

 * manually enter a heat and duration
 * select the type of filament (loads in optimal heat and duration presets for the filament selected)
 
..., then select **Start**. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/226`

```{note}
What happens when the spools within the AMS 2 Pro are different filament materials? It seems there might be some guard rails preventing you from doing this with certain mixes of materials.

> When drying high-temperature filament, you need to take out the low-temperature filament. For example, when drying ABS, PLA filament cannot be placed in the AMS.

`{ref} https://wiki.bambulab.com/en/ams-2-pro/ams-2-pro-for-drying-in-x1-p1-series`
```

# H2S Checklist

 * is on flat and stable surface?
 * is room temperature of 15-30C (60-85F)?
 * requires auto-calibration? `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/224`
 * is filament dry? `{ref} ADD CITATION`
 * is filament tangled? `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/225`

# Terminology

* `{bm} AMS/\b(AMS 2 Pros|AMS 2 Pro|AMSes|AMS)\b/` - Automatic Material System, an extension to Bambu Lab printers that manages multiple filament spools.

  The original AMS targets Bambu Lab P2 series printers and supports ...
  
  * feeding filament to the printer from the desired spool (4 spools per unit).
  * chaining multiple AMS units together (16 spools max).
  * keeping filament dry.
  * identifying the color and type of filament (only for official Bambu Lab filaments, using RFID). `{ref} https://us.store.bambulab.com/products/ams-multicolor-printing`
  
  The AMS 2 Pro targets multiple Bambu Lab printer series (e.g., P2, H2, etc..) and additionally supports chaining even more units together (4 spools per unit, 24 spools max). `{ref} https://us.store.bambulab.com/products/ams-2-pro`

  `{bm-error} Did you mean AMS 2 Pro?/(AMS\s?Pro\s?2|AMS\s?2|AMS\s?Pro)/i`

* `{bm} heat resistance` - FILL ME IN.

* `{bm} chamber heat circulation fan` - FILL ME IN.

* `{bm} filter switch flap` - FILL ME IN.

* `{bm} part cooling fan` - FILL ME IN.

* `{bm} auxiliary part cooling fan` - FILL ME IN.

* `{bm} PLA/\b(PLA)\b/` - FILL ME IN (filament).

* `{bm} TPU/\b(TPU)\b/` - FILL ME IN (filament).

* `{bm} ABS/\b(ABS)\b/` - FILL ME IN (filament).

* `{bm} ASA/\b(ASA)\b/` - FILL ME IN (filament).

* `{bm} PC/\b(PC)\b/` - FILL ME IN (filament).

* `{bm} PA/\b(PA)\b/` - FILL ME IN (filament).

* `{bm} toolhead` - An assembly consisting of a PTFE connector, an extruder, and a hotend with nozzle housed in an enclosure. Filament enters the nozzle through the PTFE connector located at the top, where the extruder motor grabs it and pushes it into the nozzle located at the bottom. The bottom bottom right-side of the toolhead has a camera attached, while the hotend poking out of the enclosure is sandwiched between cooling ducts that directs air to rapidly cool filament as its printed.

![Toolhead front diagram](toolhead.drawio.svg)


The toolhead moves left-right on the X-Axis linear rail. The X-Axis linear rail itself moves forward and backward on the Y-Axis. These rails are how the toolhead positions itself for printing. `{ref} https://bambulab.com/en/support/academy/10/course/1031276070794240000/chapter/227`

```{note}
It sounds like the camera and the cooling ducts (and the railing) are not a part of the toolhead itself? These are attachments.
```

```{note}
The H2D's toolhead is different from the H2S's toolhead? It has two PTFE connectors and two nozzles?
```

* `{bm} extruder` -

FILL ME IN
FILL ME IN
FILL ME IN
FILL ME IN
FILL ME IN
FILL ME IN
FILL ME IN

`{bm-error} Did you mean Bambu Lab (not plural)?/(Bambu Labs)/`

`{bm-ignore} !!([\w\-]+?)!!/i`

`{bm-error} Missing topic reference/(_TOPIC)/i`