# Aquenis Firmware Repository

Öffentlicher Distributionskanal für OTA-fähige Aquenis-Firmware.

## Kanäle

- `production`: freigegebene Firmware für produktive G1-Geräte
- `development`: Entwicklungs- und Pilotpakete

Die Android-App lädt `manifest.json`, anschließend die passende Datei unter
`channels/` und zuletzt die referenzierten Firmware-Metadaten und Payloads.

Quellcode und Build-Konfiguration bleiben in den jeweiligen privaten
Geräte-Repositories. Dieses Repository enthält ausschließlich veröffentlichte
Firmware-Pakete und deren Prüfinformationen.

Aktuell sind noch keine Firmware-Payloads veröffentlicht.
