TOPTARGETS := all clean

MAKES := $(wildcard */Makefile)
SUBDIRS := $(MAKES:%Makefile=%.)

$(TOPTARGETS): $(SUBDIRS)

$(SUBDIRS):
		@echo ""
		@echo MAKE $@
		@$(MAKE)  --no-print-directory -C $@ $(MAKECMDGOALS) || true

.PHONY: $(TOPTARGETS) $(SUBDIRS)