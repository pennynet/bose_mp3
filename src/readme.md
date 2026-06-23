v0.1  

Very simple addon for raspberrymatic.  

It can play MP3-announcments on BOSE-Soundtouch (with fallback after a certain time to a eventually running preset).  

In raspberrymatic do as a skript:  

   var action"announce":  
   var player="name_of_soundtouch"; ! same as in /etc/bose_mp3-settings.conf  
   var payload="name_of_soundfile"; ! no ".mp3" suffix  
   dom.GetObject("CUxD.CUX2801001:1.CMD_EXE").State("/usr/local/addons/bose_mp3/bin/" # action # ".sh " # player # " " # payload);  

CUx-Daemon required! 

["system.Exec()" works as well, but is not a good idea -> google-search]  

For settings and upload mp3 go to http://[CCU_IP]/addons/bose_mp3/index.html  

Important: 
Because support by BOSE has ended, prior action is mandatory to use presets! Without obligation I recommend https://github.com/JRpersonal/streborn
