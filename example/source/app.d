import std.stdio;
import colorize : fg, color, cwritef;

void main() {
	// writeln("this program is an example of a program that does nothing useful");
	write("This program is an ");
	cwritef("example".color(fg.red));
	write(" of a ");
	cwritef("program".color(fg.green));
	write(" that does nothing ");
	cwritef("useful".color(fg.blue));
	writeln();
}
