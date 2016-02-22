function reloadGTK(){
python - <<END
import sys, gtk

if len(sys.argv) >= 2:
    usage()
events=gtk.gdk.Event(gtk.gdk.CLIENT_EVENT)
data=gtk.gdk.atom_intern("_GTK_READ_RCFILES", False)
events.data_format=8
events.send_event=True
events.message_type=data
events.send_clientmessage_toall()
    
END
}
