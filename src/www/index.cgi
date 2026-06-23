#!/bin/tclsh
package require ncgi

set uploadDir "/usr/local/addons/bose_mp3/www/mp3"
set cfgFile "/usr/local/addons/bose_mp3/etc/bose_mp3-settings.conf"

array set cfg {}

if {[file exists $cfgFile]} {
    set fh [open $cfgFile r]
    while {[gets $fh line] >= 0} {
        if {[regexp {^([^=]+)=(.*)$} $line -> key value]} {
            set cfg($key) $value
        }
    }
    close $fh
}

puts "Content-Type: text/html"
puts ""

puts "<html><head><meta charset=\"utf-8\"><title>Bose MP3 administration</title></head><body>"

puts "<h2>upload MP3</h2>"
puts {<form action="upload.cgi" method="post" enctype="multipart/form-data">
<input type="file" name="mp3file" accept=".mp3">
<input type="submit" value="Upload">
</form>}

puts "<hr><h3>existing files</h3>"

foreach f [lsort [glob -nocomplain -directory $uploadDir *.mp3]] {
    set name [file tail $f]
    set size [file size $f]
    puts "<div>$name ($size Bytes) <a href=\"tts/$name\">Download</a> <a href=\"delete.cgi?file=$name\" onclick=\"return confirm('Datei wirklich löschen?');\">Löschen</a></div>"
}

puts "<hr><h3>Speakers</h3>"
puts "<form action=\"save_settings.cgi\" method=\"post\">"
puts "<table border=\"1\" cellpadding=\"4\">"
puts "<tr><th>Name</th><th>IP-Address</th></tr>"

set idx 0
foreach key [lsort [array names cfg]] {
    if {$key eq "ANNOUNCE_VOLUME" || $key eq "WAIT"} { continue }
    incr idx
    puts "<tr><td><input type=\"text\" name=\"speaker_name_$idx\" value=\"$key\"></td><td><input type=\"text\" name=\"speaker_ip_$idx\" value=\"$cfg($key)\"></td></tr>"
}

for {set i [expr {$idx+1}]} {$i <= $idx+5} {incr i} {
    puts "<tr><td><input type=\"text\" name=\"speaker_name_$i\"></td><td><input type=\"text\" name=\"speaker_ip_$i\"></td></tr>"
}

set vol 50
if {[info exists cfg(ANNOUNCE_VOLUME)]} { set vol $cfg(ANNOUNCE_VOLUME) }

set wait 12
if {[info exists cfg(WAIT)]} { set wait $cfg(WAIT) }

puts "</table><br>"
puts "ANNOUNCE_VOLUME: <input type=\"number\" min=\"0\" max=\"100\" name=\"ANNOUNCE_VOLUME\" value=\"$vol\"><br><br>"
puts "FALLBACK_TIME: <input type=\"number\" min=\"0\" max=\"300\" name=\"WAIT\" value=\"$wait\"><br><br>"
puts "<input type=\"submit\" value=\"save\">"
puts "</form>"
puts "</body></html>"
