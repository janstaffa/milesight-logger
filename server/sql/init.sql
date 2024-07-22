CREATE TABLE IF NOT EXISTS "data" (
	"ID" INTEGER PRIMARY KEY,
	"device_eui" INT,
	"timestamp" TIMESTAMPTZ,
	"parameter" TEXT,
	"value" REAL
);