#!/bin/sh

# v0.0.1 (22.06.2026)

# in raspberrymatic do:
# var player="name_of_soundtouch"; ! same as in /etc/bose_mp3-settings.conf
# var payload="name_of_soundfile"; ! no ".mp3" suffix
# dom.GetObject("CUxD.CUX2801001:1.CMD_EXEC").State("/usr/local/addons/bose_mp3/bin/script.sh" # " " # player # " " # payload);
# -----------------------------------------------------------------------------------------------------------------------------


# arguments
PLAYER="$1"
PAYLOAD="$2"
if [ -z "$PLAYER" ] || [ -z "$PAYLOAD" ]; then
   exit 1
fi


# settings
ADDON="bose_mp3"
ADDON_PATH="/usr/local/addons/${ADDON}"
CONF_FILE="${ADDON_PATH}/etc/${ADDON}-settings.conf"                # this file must be edited by hand!

BOSE_IP=$(grep "^${PLAYER}=" "$CONF_FILE" | cut -d= -f2)
CCU_IP=$(grep "^CCU_IP=" "$CONF_FILE" | cut -d= -f2)
if [ -z "$BOSE_IP" ] || [ -z "$CCU_IP" ]; then
   exit 1
fi

MP3_VOL=$(grep "^ANNOUNCE_VOLUME=" "$CONF_FILE" | cut -d= -f2)
   [ -z "$MP3_VOL" ] && MP3_VOL=50

WAIT=$(grep "^WAIT=" "$CONF_FILE" | cut -d= -f2)
   [ -z "$WAIT" ] && WAIT=12

if [ -f "${ADDON_PATH}/www/tts/${PAYLOAD}.mp3" ]; then
   MP3_URL="http://${CCU_IP}/addons/bose_mp3/tts/${PAYLOAD}.mp3"
else
   MP3_URL="http://${CCU_IP}/addons/bose_mp3/tts/sorry.mp3"
fi


# store preset and volume
PRESET=$(curl -s "http://${BOSE_IP}:8090/now_playing" \
   | sed -n 's:.*<itemName>\([0-9][0-9]*\)</itemName>.*:\1:p')

OLDVOL=$(curl -s "http://${BOSE_IP}:8090/volume" \
   | sed -n 's:.*<actualvolume>\([0-9]*\)</actualvolume>.*:\1:p')
   [ -z "$OLDVOL" ] && OLDVOL=20


# restore volume on exit
restore_volume() {
    curl -s -X POST "http://${BOSE_IP}:8090/volume" \
         -H "Content-Type: text/xml" \
         -d "<volume>${OLDVOL}</volume>" >/dev/null
}
trap restore_volume EXIT


# play MP3 first and change volume
curl -s \
     -d "{\"url\":\"${MP3_URL}\"}" \
     "http://${BOSE_IP}:8888/api/play" >/dev/null

curl -s \
     -X POST "http://${BOSE_IP}:8090/volume" \
     -H "Content-Type: text/xml" \
     -d "<volume>${MP3_VOL}</volume>" >/dev/null


# wait for end of announcement and then  restore preset
[ "$PAYLOAD" = "bigben" ] && WAIT=78
  sleep "$WAIT"

if [ -n "$PRESET" ]; then
   curl -s \
        -X POST "http://${BOSE_IP}:8888/api/play/${PRESET}" >/dev/null
fi

exit 0

# ----------------------------------------------------------------------------------------------------------------------------------
# EOF
