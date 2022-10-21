#
# Makefile for registration client for switchdesk
#

NAME    = $(shell awk '/Name:/ { print $$2 }' switchdesk.spec)
VERSION = $(shell awk '/Version:/ { print $$2 }' switchdesk.spec)

BACKEND = backend
DOC     = doc
FILES   = $(BACKEND) $(NAME)-gui
GLADES  = $(NAME).glade
PIXMAPS = switchdesk.png
PYFILES = $(BACKEND).py $(NAME)-gui.py
SCRIPTS = $(NAME) $(NAME)-helper

OBJECTS = $(addsuffix .py, $(FILES))

SUBDIRS = po

prefix  = /usr
bindir  = $(prefix)/bin
sbindir = $(prefix)/sbin
datadir = $(prefix)/share
mandir  = $(datadir)/man

all:: $(OBJECTS) $(NAME).desktop.in
	$(MAKE) -C po update-po
	intltool-merge po $(NAME).desktop.in $(NAME).desktop -d -u -c po/.intltool-merge-cache

install:: all
	(cd po ; make install)

	@mkdir -p $(DESTDIR)$(datadir)/applications
	install -p -m 644 $(NAME).desktop $(DESTDIR)$(datadir)/applications/

	@mkdir -p $(DESTDIR)$(datadir)/$(NAME)
	@for f in $(PYFILES) ; do install -m 755 $$f $(DESTDIR)$(datadir)/$(NAME)/ ; done
	install -p -m 755 Xclients* $(DESTDIR)$(datadir)/$(NAME)/
	install -p -m 644 $(GLADES) $(DESTDIR)$(datadir)/$(NAME)/

	@mkdir -p $(DESTDIR)$(bindir)
	install -p -m 755 $(SCRIPTS) $(DESTDIR)$(bindir)

	@mkdir -p $(DESTDIR)$(datadir)/pixmaps
	@for i in $(PIXMAPS) ; do install -p -m 644 pixmaps/$$i $(DESTDIR)$(datadir)/pixmaps/ ; done

	@mkdir -p $(DESTDIR)$(mandir)/man1
	install -p -m 644 $(DOC)/$(NAME).1 $(DESTDIR)$(mandir)/man1

	@mkdir -p $(DESTDIR)$(mandir)/fr/man1
	install -p -m 644 $(DOC)/$(NAME).fr.1 $(DESTDIR)$(mandir)/fr/man1

clean::
	@rm -fv *~ .*~ *.desktop
