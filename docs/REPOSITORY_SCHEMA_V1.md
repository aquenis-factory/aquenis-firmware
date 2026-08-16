# Aquenis Firmware Repository Schema V1

## Auflösung durch die App

1. `manifest.json`
2. `channels/production.json` oder `channels/development.json`
3. die in `firmwares[].path` referenzierte `metadata.json`
4. die im Metadatensatz unter `files.firmware` genannte Payload

## Kanäle

- `production`: freigegebene Firmware aus `main` beziehungsweise einem finalisierten Release
- `development`: Pakete aus `develop`, `feature/*`, `hotfix/*` und noch nicht finalisierten `release/*`

Die physischen Entwicklungs-Lanes bleiben im Pfad sichtbar. Der logische
App-Kanal bleibt trotzdem immer `production` oder `development`.

## Beispiel-Metadaten

```json
{
  "schemaVersion": 1,
  "product": "Aquenis Hub M5Basic",
  "deviceType": "hub",
  "otaTarget": "hub-m5",
  "hardwareProfile": "m5stack-basic",
  "firmwareVersion": "2.4.12-example",
  "build": "2026.08.16-01",
  "channel": "production",
  "otaCapable": true,
  "artifactsAvailable": true,
  "firmwareSizeBytes": 123456,
  "files": {
    "firmware": "firmware.bin"
  },
  "sha256": {
    "firmware": "<sha256>"
  }
}
```

`deviceType` dient zur Auswahl in der App. `otaTarget` ist der konkrete,
vom Gerät geprüfte Wert des HTTP-Headers `X-Firmware-Target`.
