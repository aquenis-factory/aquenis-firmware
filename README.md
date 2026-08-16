# Aquenis Firmware Repository

Öffentlicher Distributionskanal für OTA-fähige Aquenis-Firmware.

## Kanäle

- `production`: freigegebene Firmware für produktive G1-Geräte
- `development`: Entwicklungs- und Pilotpakete

Die Android-App lädt `manifest.json`, anschließend die passende Datei unter
`channels/` und zuletzt die referenzierten Firmware-Metadaten und Payloads.

Der jeweilige Kanalindex verweist auf die aktuell angebotene Firmware. Bereits
veröffentlichte Pakete bleiben weiterhin in ihrem versionsbezogenen Verzeichnis
erhalten.

## Veröffentlichte Firmware

| Gerät | Hardwareprofil | Version | Build | Status |
|---|---|---|---|---|
| Aquenis Hub M5Basic G1 | `m5stack-basic` | [`2.4.11-finalized-hub`](production/main/Aquenis_Hub_M5Basic/v2.4.11-finalized-hub/) | `2026.08.15-01` | Veröffentlichte und abgenommene Ausgangsversion |
| Aquenis Hub M5Basic G1 | `m5stack-basic` | [`2.4.12-ota-test`](production/main/Aquenis_Hub_M5Basic/v2.4.12-ota-test/) | `2026.08.16-01` | Aktuell in `production`; erstes OTA-Update über die App erfolgreich bestätigt |

Aktueller Production-Stand:

- Gerätetyp: `hub`
- OTA-Target: `hub-m5`
- Hardwareprofil: `m5stack-basic`
- angebotene Version: `2.4.12-ota-test`
- OTA-Installation über die Aquenis App: erfolgreich verifiziert

## Repository-Inhalt

Quellcode und Build-Konfiguration bleiben in den jeweiligen privaten
Geräte-Repositories. Dieses Repository enthält ausschließlich veröffentlichte
Firmware-Pakete, Metadaten, Kanalindizes und Prüfinformationen.

Jedes Firmware-Paket enthält:

- `firmware.bin`
- `metadata.json` mit Version, Build, Zielgerät, Dateigröße und SHA-256-Prüfsumme
