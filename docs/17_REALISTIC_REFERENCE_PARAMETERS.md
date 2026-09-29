# The reference plant: parameters and their sources

> **Parent:** [Documentation map](00_DOCUMENTATION_MAP.md)  
> **Code:** `caes/presets.py` (`REALISTIC_REFERENCE`), `realistic_reference_config.json`  
> **Full source dossier:** [research/REALISTIC_PARAMETERS_SOURCES.md](research/REALISTIC_PARAMETERS_SOURCES.md) (163 links, 155 verified reachable)

The desktop application opens with this configuration. "Reset defaults" and
the command line without `--config` use it too. It describes a **large
LTAHP-CAES plant, tens of MW**, built from commercially available machinery.
Most values are the typical published value for that class. Five are design
choices of this project, marked `[choice]` and justified against the
published range they sit in: equal stage counts, the two machine
efficiencies, the air/water exchanger class and the 80 °C user supply.

`PlantConfig()` without arguments keeps its original field defaults. Those are
the fixed numerical baseline of the test suite, not a claim about a real
plant.

## 1. The plant

```text
site         North-German salt-cavern region, 10 °C annual mean, 80 % RH
storage      salt cavern at 100 bar (single design pressure)
compression  integrally geared compressor, 8 stages, intercooled after every stage
expansion    integrally geared radial expander, 8 stages (two 4-stage gearboxes)
cavern       salt cavern, no net heat exchange, injection up to 50 °C
aftercooler  only if the last intercooler cannot hold that limit (not in this plant)
store        two tanks, coolant not yet chosen, screened from -40 to 150 °C
heat user    district heating, supply 80 °C, return 40 °C
```

## 2. Parameters

Tags: `[datasheet]` vendor document, `[paper]` peer-reviewed, `[project]`
operator or project document, `[estimate]` engineering estimate with the
stated basis, `[choice]` a design decision of this project.

| input | value | published range | basis | tag |
|---|---:|---|---|---|
| `storage_pressure_bar` | 100 | 40-152 | The LTA-CAES design window: 100-152 bar in [Budt, Wolf and Span 2012](https://2012.international.conference.modelica.org/proceedings/html/pdf/ecp12076791_BudtWolfSpan.pdf); 40-100 bar for KompEx (Hadam and Budt 2023). Operating caverns run 43-76 bar (Huntorf, McIntosh). 100 bar sits at the meeting point of the two LTA-CAES designs. Higher pressure lowers every figure of merit here (section 3) | `[paper]` |
| `maximum_injection_temperature_c` | 50 | 40-50 | Air is injected into the salt cavern at up to 50 °C at Huntorf (Kaiser 2020, in the dossier); the last intercooler is given more water when the air would leave it warmer, and an aftercooler works only if that is not enough. The cavern itself exchanges no net heat ([document 02](02_PHYSICS_AND_MODEL_BOUNDARY.md#the-cavern)). In the reference plant the last intercooler leaves the air at 45.7 °C, so the limit does not bind | `[project]` |
| `compressor_stages` | 8 | 5-10 | "an eight stage compressor and a four stage expander, both integrally geared" (Budt, Wolf and Span 2012); IGC vendors offer up to 8-10 stages with intercooling after each ([MAN RG](https://www.man-es.com/docs/default-source/document-sync/rg-integrally-geared-compressors-eng.pdf)). At 100 bar this is a stage ratio of about 1.8, inside the 1.7-2.2 IGC band | `[paper]` |
| `expander_stages` | 8 | 3-8 | Equal to the compressor by choice. An integrally geared expander carries 1-4 stages per gearbox ([Atlas Copco](https://www.atlascopco.com/content/dam/atlas-copco/compressor-technique/gas-and-process/documents/new-folder/AC%20Turboexpander%20Brochure.pdf.coredownload.pdf)), so eight stages mean two gearboxes. LTA-CAES used four | `[choice]` |
| `compressor_efficiency` | 0.86 | 0.85-0.89 | Per-stage **isentropic**. Inside the band converted from the IGC polytropic "high eighties" ([Witkowski and Majkut 2012](https://journals.pan.pl/Content/84623/PDF/06_paper.pdf)), one point above its conservative end: a margin for a large machine running across its map | `[choice]` |
| `expander_efficiency` | 0.85 | 0.80-0.92 | Isentropic, total-to-static. The KompEx turbomachine value, 85 % (Hadam and Budt 2023), below the 0.88-0.90 of design studies ([Sciacovelli et al. 2017](https://pure-oai.bham.ac.uk/ws/portalfiles/portal/42823087/Manuscript_Clear_v4.pdf); Pottie et al. 2024) | `[choice]` |
| `intercooler_pressure_drop` | 0.015 | 0.005-0.025 | 1.5 % per exchanger, the base value of the Huntorf-calibrated low-temperature A-CAES model of [Luo et al. 2016](https://wrap.warwick.ac.uk/76075/1/WRAP_1-s2.0-S0306261915013185-main.pdf) | `[paper]` |
| `interheater_pressure_drop` | 0.015 | 0.005-0.025 | Same source; every paper that publishes both applies one value to charge and discharge exchangers | `[paper]` |
| `heat_exchanger_ntu` | 3.4 | 2.8-3.4 | The top of six A-CAES design points in [Barbour et al. 2025](https://pure-oai.bham.ac.uk/ws/portalfiles/portal/279134473/IET_Renewable_Power_Gen_-_2025_-_Barbour_-_Exergy_analysis_of_isochoric_and_isobaric_adiabatic_compressed_air_energy.pdf) (NTU 2.83-3.41). No source supports a larger class | `[choice]` |
| `heat_user_exchanger_ntu` | 5.0 | 3.7-8.9 | Conventional substation, LMTD about 10 K ([Thorsen and Iversen 2012](https://assets.danfoss.com/documents/latest/90874/AC098986469348en-010201.pdf)) | `[paper]` |
| `extraction_exchanger_ntu` | 8 per zone | 3-13 | By analogy with closed feedwater heaters, terminal difference 2.8-4.4 K ([EPRI TR-107422-V2](https://restservice.epri.com/publicdownload/TR-107422-V2/0/Product)). The least constrained input: no staged-bleed exchanger of this kind exists in a built CAES plant | `[estimate]` |
| `cold_return_cooler_ntu` | 0.8 | 0.4-1.1 | Dry cooler at a typical 5-9 K approach to ambient ([IEA SHC Task 38, C5](https://task38.iea-shc.org/Data/Sites/1/publications/IEA-Task38-Report_C5_Heat%20rejection.pdf)). The model treats the atmosphere as an infinite stream, `eps = 1 - exp(-NTU)`: about 55 % effectiveness | `[paper]` |
| `coolant_minimum_temperature_c` | -40 | | The coolant is not yet chosen (water-glycol, brine, a low-temperature heat-transfer fluid), so the limit is set wide enough to screen the physics rather than a fluid; the model uses the heat capacity of water throughout. In the reference case the coldest return is +5 °C and no antifreeze is needed. Colder sites, colder stored air or more expansion stages drive the tail returns below 0 °C, and the chosen fluid must then cover them: about -25 °C needs 40 % glycol | `[design choice]` |
| `coolant_maximum_temperature_c` | 150 | | A common ceiling for glycol mixtures and unpressurized loops. The plant reaches 86 °C, so the limit does not bind | `[estimate]` |
| `thermal_storage_tank_ua_w_per_k` | 1.0e-3 per kg of air | 3e-4 to 3e-3 | About 1.5 kW/K for a 10 000 m³ insulated hot-water store ([IEA-ES fact sheet](https://iea-es.org/wp-content/uploads/public/FactSheet_Thermal_Sensible_Water_2022-10-19.pdf)), divided by the 1.56e6 kg of air it serves | `[estimate]` |
| `storage_duration_hours` | 4 | 2-12 | The **standing time** of each tank between charge and discharge, not the discharge duration; one value applies to both tanks | `[estimate]` |
| `heat_user_supply_temperature_c` | 80 | 65-90 | Close to the measured Danish average supply of 78 °C; inside the 3rd-generation range (Sweden 86 °C, Germany 88 °C) | `[choice]` |
| `heat_user_return_temperature_c` | 40 | 35-55 | Danish guidance: return "should never exceed 40 °C" | `[project]` |
| `ambient_temperature_c` | 10 | 8.7-10.1 | Deutscher Wetterdienst, Bremen, 1991-2020 annual mean 9.8 °C ([DWD CDC](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/multi_annual/mean_91-20/Temperatur_1991-2020.txt)); Elsfleth, next to Huntorf, 9.9 °C | `[datasheet]` |
| `ambient_relative_humidity` | 0.80 | 0.78-0.82 | DWD Klimatafel Bremen, mean of daily means ([DWD](https://www.dwd.de/DWD/klima/beratung/ak/ak_102240_kt.pdf)); a 1961-1990 normal | `[datasheet]` |
| `optimization_objective` | combined delivery | | The plant sells heat. The charge split is still chosen by exergy ([document 14](14_HEAT_USER_REDUCTION_AND_CHARGE_SPLIT.md)) | |

### What the literature does not give

- **A total pressure-drop target for LTA-CAES.** Wolf and Budt 2014 and the
  Modelica paper of Budt, Wolf and Span 2012 contain no numeric pressure loss.
  Luo et al. 2016 is the best-supported source for a low-temperature A-CAES.
  At 1.5 % per exchanger, eight intercoolers compound to 11.4 % of the
  compressor discharge pressure; the model includes that compounding.
- **An air/water stage exchanger better than NTU 3.4** in any A-CAES design.
- **A measured per-stage isentropic efficiency** of an air-service IGC at
  60-100 bar: the value is converted from polytropic figures.
- **Any operating staged-extraction exchanger** in CAES service.

## 3. What the reference plant does

Solved with the current code (`python -m caes.cli`, no arguments):

| quantity | value |
|---|---:|
| compression work | 539.7 kJ/kg-air |
| expansion work | 320.9 kJ/kg-air |
| heat delivered at 80/40 °C | 235.2 kJ/kg-air |
| ambient heat drawn in | 0 |
| electrical round-trip efficiency | **59.5 %** |
| useful-exergy efficiency | 66.0 % |
| useful-energy delivery ratio `J` | 1.030 |
| net heat-pump COP (Carnot at 80/40 °C and 10 °C ambient: 6.7) | 1.08 |
| coolant inventory | 2.55 kg / kg air |
| cold / hot store | 33.3 °C / 82.1 °C |
| stored air | 45.7 °C (as the last intercooler leaves it), 0.80 g/kg |
| exhaust | -7.6 °C |

**Against the literature.** The electrical efficiency lies inside the 52-60 %
published for LTA-CAES concepts (Wolf and Budt 2014; 55.5 % for KompEx).

**Where the compression heat goes.** All of it reaches the store through the
intercoolers: the cavern exchanges no net heat and the aftercooler is not
needed, so the air is stored at the 45.7 °C the last intercooler leaves it at.

**Sensitivity.**

| variant | RTE | J | eta_ex |
|---|---:|---:|---:|
| reference | 0.595 | 1.030 | 0.660 |
| with the air aftercooled to the 10 °C ambient (the former model) | 0.561 | 1.041 | 0.632 |
| winter day, -20 °C ambient, 100/40 °C user (last intercooler held at the 50 °C limit) | 0.558 | 0.982 | 0.669 |
| same winter day, aftercooled to -20 °C (the former model) | 0.506 | 0.947 | 0.621 |

**Why the aftercooler stays off.** Cooling the reference air to ambient
before the cavern would throw away 44 kJ/kg, but the dry air would let the
turbines expand to -27 °C and the plant take 31 kJ/kg back from the
atmosphere while selling more heat: `J` would be 1.1 points higher, round-trip
efficiency 3.4 points lower. The design keeps the aftercooler for when it is
needed - the injection limit - not as a way to raise `J`. On the winter day
the last intercooler holds the air at the 50 °C limit with extra water, and
`J` stays below one: at -20 °C the atmosphere is the coldest stream in the
plant, so there is no ambient heat to draw, and the undried exhaust cannot go
much below its own frost point, about -22 °C.

**What drier air is worth.** An upper bound, computed with the former
aftercooler at the 50 °C limit: perfectly dry air (ambient RH 0.1 %) lets the
turbines expand to -49 °C and draw 103 kJ/kg from the atmosphere, `J` = 1.20
at RTE 0.47. Reaching even part of it needs the air dried at storage pressure
against a sink colder than the ambient, and air dried before the cavern is
partly re-wetted by the brine sump. A discharge-side dryer, cooled by the
plant's own cold exhaust, is the candidate; it is not modelled yet.

**Other concepts on these parameters.** The same site and machines do not
close as AD-CAES: at 10 °C ambient and 100 bar, ambient reheat cannot keep
the expander outlets above the anti-icing floor. Use
`--config heat_and_power_example_config.json --mode diabatic` (15 °C,
85.8 bar) to see AD-CAES. The electricity-only dispatch of the same hardware
still runs through the older coupled cold-loop solver.

## 4. Where the model and real machines differ

- **Constant storage pressure.** A real cavern swings between its minimum and
  maximum pressure during a cycle, and the turbine inlet is often throttled
  to a constant value, a loss the model does not represent.
- **Equal stage ratios.** Real LTA-CAES compressors raise the ratio in the last
  stages (Budt, Wolf and Span 2012, figure 12).
- **Cavern thermal behaviour.** The cavern is taken as exchanging no net
  heat, so the air leaves at the temperature it entered. Within a cycle the
  air still swings by 15-20 K around the wall temperature (Huntorf: 28-45 °C)
  and the rock returns 1-4 kJ/kg net (document 02); neither is represented.
- **Expander outlet floor.** The model holds every turbine outlet at 10 °C, or
  at the frost point plus 10 K. Vendors accept 0 °C as a hard limit.
- **The AD-CAES ambient exchanger** (`ambient_heat_exchanger_ntu`) was not
  part of this research and keeps its original value, 5.
