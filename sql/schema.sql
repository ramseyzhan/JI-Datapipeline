CREATE TABLE anomaly (
  anomalyid INTEGER PRIMARY KEY AUTOINCREMENT,
  recorded DATETIME NOT NULL,
  global_active_power REAL,
  global_reactive_power REAL,
  voltage REAL,
  global_intensity REAL,
  sub_metering_1 REAL,
  sub_metering_2 REAL,
  sub_metering_3 REAL
);
