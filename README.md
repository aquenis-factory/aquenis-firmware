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
| Aquenis Hub M5Basic G1 | `m5stack-basic` | [`2.4.12-ota-test`](production/main/Aquenis_Hub_M5Basic/v2.4.12-ota-test/) | `2026.08.16-01` | Erstes OTA-Update über die App erfolgreich bestätigt |
| Aquenis Hub M5Basic G1 | `m5stack-basic` | [`2.4.13-tank-ota-metadata`](production/main/Aquenis_Hub_M5Basic/v2.4.13-tank-ota-metadata/) | `2026.08.16-02` | Führt Tank-OTA-Metadaten ein; bei mehreren Tanks durch `2.4.14` ersetzt |
| Aquenis Hub M5Basic G1 | `m5stack-basic` | [`2.4.14-tank-registry-capacity-fix`](production/main/Aquenis_Hub_M5Basic/v2.4.14-tank-registry-capacity-fix/) | `2026.08.16-03` | Aktuell in `production`; behebt Controllerlisten-Überlauf bei mehreren Tanks |
| Aquenis Tank ESP32-C3 G1 | `esp32-c3-mini` | [`0.5.20-ota-bootstrap`](production/main/Aquenis_Tank_ESP32C3/v0.5.20-ota-bootstrap/) | `2026.08.16-01` | Aktuell in `production`; OTA-fähige Tank-Bootstrap-Version |

## Aktueller Production-Stand

| Gerätetyp | OTA-Target | Hardwareprofil | Angebotene Version |
|---|---|---|---|
| `hub` | `hub-m5` | `m5stack-basic` | `2.4.14-tank-registry-capacity-fix` |
| `tank` | `tank-esp32c3` | `esp32-c3-mini` | `0.5.20-ota-bootstrap` |

Der Hub wurde bereits erfolgreich über die Aquenis App von `2.4.11` auf
`2.4.12` aktualisiert. Für Tank-OTA und zuverlässige Registrierung in einer
Mehrcontroller-Installation muss der Hub mindestens `2.4.14` verwenden. Ein
Tank benötigt einmalig `0.5.20-ota-bootstrap` per USB; alle nachfolgenden
Tank-Versionen können anschließend über die App installiert werden.

## Repository-Inhalt

Quellcode und Build-Konfiguration bleiben in den jeweiligen privaten
Geräte-Repositories. Dieses Repository enthält ausschließlich veröffentlichte
Firmware-Pakete, Metadaten, Kanalindizes und Prüfinformationen.

Jedes Firmware-Paket enthält:

- `firmware.bin`
- `metadata.json` mit Version, Build, Zielgerät, Dateigröße und SHA-256-Prüfsumme
