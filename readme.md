Very simple addon for rasperrymatic. It can play MP3-announcments on BOSE-Soundtouch (with fallback to a eventually running preset).

In raspberrymatic-skript do:  
var player="name_of_soundtouch"; ! same as in /etc/bose_mp3-settings.conf  
var payload="name_of_soundfile"; ! no ".mp3" suffix  
dom.GetObject("CUxD.CUX2801001:1.CMD_EXE").State("/usr/local/addons/bose_mp3/bin/script.sh" # " " # PLAYER # " " # PAYLOAD);  

CUx-Daemon required! ["system.Exec()" works as well, but is not a good idea -> google-search]  
In v0.0.1 you have to edit your settings in /etc/bose_mp3-settings.conf and upload your *.mp3 to /www/tts/ by hand (SSH to raspberrymatic)!

Important:  
Because support by BOSE has ended, prior action is mandatory to use presets. Without obligation I recommend https://github.com/JRpersonal/streborn
