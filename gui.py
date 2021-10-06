import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class OutputTable(Gtk.Window):
    def __init__(self, n_rows, data):
        super().__init__(title="VLSM")
        
        table = Gtk.Table(n_rows = n_rows, n_columns = 9, homogeneous = True)
        self.add(table)

        """for point in data:
            label = Gtk.Label()"""

window = OutputTable(10, [])
window.connect("destroy", Gtk.main_quit)
#window.set_default_size(1500, 500)
window.show_all()
Gtk.main()
