BEGIN;

CREATE TABLE IF NOT EXISTS civic_event (
  civic_event_id TEXT PRIMARY KEY,
  event_name TEXT NOT NULL,
  location TEXT NOT NULL,
  organizer TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attendance (
  attendance_id TEXT PRIMARY KEY,
  civic_event_id TEXT NOT NULL,
  attendee_type TEXT NOT NULL,
  checked_in INTEGER NOT NULL,
  contribution REAL NOT NULL,
  attend_date TEXT NOT NULL,
  FOREIGN KEY (civic_event_id) REFERENCES civic_event(civic_event_id)
);

COMMIT;
