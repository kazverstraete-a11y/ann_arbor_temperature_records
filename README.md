# Ann Arbor Temperature Records (2005–2015)

This project analyzes daily temperature records in Ann Arbor, Michigan, using historical weather station data.

The goal is to compare **daily minimum and maximum temperatures from 2015** against the **historical range (2005–2014)** and to highlight days where 2015 set new record highs or lows.

---

## Key Steps

- Clean and preprocess raw NOAA weather data
- Convert temperatures from tenths of degrees Celsius to °C
- Correct for leap-year effects to ensure proper day-of-year alignment
- Aggregate daily minimum and maximum temperatures across all stations
- Identify record-breaking days in 2015 relative to the 2005–2014 baseline
- Visualize:
  - Historical daily temperature bands
  - Record-breaking days in 2015
  - Clear annotations and contextual summaries

---

## Visualization

The final figure shows:
- A shaded band representing historical daily temperature ranges (2005–2014)
- Lines for historical daily minimum and maximum temperatures
- Highlighted points for 2015 record highs and lows
- A summary of how many record-breaking days occurred in each direction

The emphasis is on **clarity, correct temporal alignment, and honest representation of variability** rather than simple averages.

---

## Requirements

```bash
pip install -r requirements.txt

