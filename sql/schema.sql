PRAGMA foreign_keys = ON;

CREATE TABLE anomaly (
  dateuse VARCHAR(20) PRIMARY KEY,
  consumption int,
  created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);
