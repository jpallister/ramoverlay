# Makefile.in generated by automake 1.14.1 from Makefile.am.
# src/qsort/Makefile.  Generated from Makefile.in by configure.

# Copyright (C) 1994-2013 Free Software Foundation, Inc.

# This Makefile.in is free software; the Free Software Foundation
# gives unlimited permission to copy and/or distribute it,
# with or without modifications, as long as this notice is preserved.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, to the extent permitted by law; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.



#   Makefile.am for building a BEEBS benchmark
#
#   Copyright (C) 2014 Embecosm Limited and University of Bristol
#
#   This file is part of the Bristol/Embecosm Energy Efficiency Benchmark
#   Suite.
#
#   Contributor: James Pallister <james.pallister@bristol.ac.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#   Common makefile.am fragments for building a BEEBS benchmark
#
#   Copyright (C) 2013 Embecosm Limited and University of Bristol
#
#   This file is part of the Bristol/Embecosm Energy Efficiency Benchmark
#   Suite.
#
#   Contributor: James Pallister <james.pallister@bristol.ac.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

VPATH = ../../../../beebs/src/qsort
am__is_gnu_make = test -n '$(MAKEFILE_LIST)' && test -n '$(MAKELEVEL)'
am__make_running_with_option = \
  case $${target_option-} in \
      ?) ;; \
      *) echo "am__make_running_with_option: internal error: invalid" \
              "target option '$${target_option-}' specified" >&2; \
         exit 1;; \
  esac; \
  has_opt=no; \
  sane_makeflags=$$MAKEFLAGS; \
  if $(am__is_gnu_make); then \
    sane_makeflags=$$MFLAGS; \
  else \
    case $$MAKEFLAGS in \
      *\\[\ \	]*) \
        bs=\\; \
        sane_makeflags=`printf '%s\n' "$$MAKEFLAGS" \
          | sed "s/$$bs$$bs[$$bs $$bs	]*//g"`;; \
    esac; \
  fi; \
  skip_next=no; \
  strip_trailopt () \
  { \
    flg=`printf '%s\n' "$$flg" | sed "s/$$1.*$$//"`; \
  }; \
  for flg in $$sane_makeflags; do \
    test $$skip_next = yes && { skip_next=no; continue; }; \
    case $$flg in \
      *=*|--*) continue;; \
        -*I) strip_trailopt 'I'; skip_next=yes;; \
      -*I?*) strip_trailopt 'I';; \
        -*O) strip_trailopt 'O'; skip_next=yes;; \
      -*O?*) strip_trailopt 'O';; \
        -*l) strip_trailopt 'l'; skip_next=yes;; \
      -*l?*) strip_trailopt 'l';; \
      -[dEDm]) skip_next=yes;; \
      -[JT]) skip_next=yes;; \
    esac; \
    case $$flg in \
      *$$target_option*) has_opt=yes; break;; \
    esac; \
  done; \
  test $$has_opt = yes
am__make_dryrun = (target_option=n; $(am__make_running_with_option))
am__make_keepgoing = (target_option=k; $(am__make_running_with_option))
pkgdatadir = $(datadir)/beebs
pkgincludedir = $(includedir)/beebs
pkglibdir = $(libdir)/beebs
pkglibexecdir = $(libexecdir)/beebs
am__cd = CDPATH="$${ZSH_VERSION+.}$(PATH_SEPARATOR)" && cd
install_sh_DATA = $(install_sh) -c -m 644
install_sh_PROGRAM = $(install_sh) -c
install_sh_SCRIPT = $(install_sh) -c
INSTALL_HEADER = $(INSTALL_DATA)
transform = $(program_transform_name)
NORMAL_INSTALL = :
PRE_INSTALL = :
POST_INSTALL = :
NORMAL_UNINSTALL = :
PRE_UNINSTALL = :
POST_UNINSTALL = :
build_triplet = x86_64-unknown-linux-gnu
host_triplet = arm-none-eabi
target_triplet = arm-none-eabi
bin_PROGRAMS = qsort$(EXEEXT)
DIST_COMMON = $(top_srcdir)/src/common.mk.am $(srcdir)/Makefile.in \
	$(srcdir)/Makefile.am $(top_srcdir)/build-aux/depcomp
#am__append_1 = -T $(top_srcdir)/src/platformcode/stm32f05_flash.ld
#am__append_2 = $(top_srcdir)/src/platformcode/startup.c
am__append_3 = -T $(top_srcdir)/src/platformcode/stm32vl_flash.ld
am__append_4 = $(top_srcdir)/src/platformcode/startup.c
#am__append_5 = -T $(top_srcdir)/src/platformcode/sam4lxplained.ld
#am__append_6 = $(top_srcdir)/src/platformcode/startup.c
#am__append_7 = -T $(top_srcdir)/src/platformcode/pic32mx.ld
#am__append_8 = $(top_srcdir)/src/platformcode/pic32mx_startup.s
#am__append_9 = $(top_srcdir)/src/platformcode/msp430.s
#am__append_10 = $(top_srcdir)/src/platformcode/msp430.s
subdir = src/qsort
ACLOCAL_M4 = $(top_srcdir)/aclocal.m4
am__aclocal_m4_deps = $(top_srcdir)/m4/libtool.m4 \
	$(top_srcdir)/m4/ltoptions.m4 $(top_srcdir)/m4/ltsugar.m4 \
	$(top_srcdir)/m4/ltversion.m4 $(top_srcdir)/m4/lt~obsolete.m4 \
	$(top_srcdir)/configure.ac
am__configure_deps = $(am__aclocal_m4_deps) $(CONFIGURE_DEPENDENCIES) \
	$(ACLOCAL_M4)
mkinstalldirs = $(install_sh) -d
CONFIG_CLEAN_FILES =
CONFIG_CLEAN_VPATH_FILES =
am__installdirs = "$(DESTDIR)$(bindir)"
PROGRAMS = $(bin_PROGRAMS)
am__qsort_SOURCES_DIST = qsort.c \
	$(top_srcdir)/src/platformcode/platformcode.c \
	$(top_srcdir)/src/platformcode/startup.c \
	$(top_srcdir)/src/platformcode/pic32mx_startup.s \
	$(top_srcdir)/src/platformcode/msp430.s
#am__objects_1 = startup.$(OBJEXT)
am__objects_2 = startup.$(OBJEXT)
#am__objects_3 = startup.$(OBJEXT)
#am__objects_4 = pic32mx_startup.$(OBJEXT)
#am__objects_5 = msp430.$(OBJEXT)
#am__objects_6 = msp430.$(OBJEXT)
am__objects_7 = platformcode.$(OBJEXT) $(am__objects_1) \
	$(am__objects_2) $(am__objects_3) $(am__objects_4) \
	$(am__objects_5) $(am__objects_6)
am_qsort_OBJECTS = qsort.$(OBJEXT) $(am__objects_7)
qsort_OBJECTS = $(am_qsort_OBJECTS)
qsort_LDADD = $(LDADD)
AM_V_lt = $(am__v_lt_$(V))
am__v_lt_ = $(am__v_lt_$(AM_DEFAULT_VERBOSITY))
am__v_lt_0 = --silent
am__v_lt_1 = 
AM_V_P = $(am__v_P_$(V))
am__v_P_ = $(am__v_P_$(AM_DEFAULT_VERBOSITY))
am__v_P_0 = false
am__v_P_1 = :
AM_V_GEN = $(am__v_GEN_$(V))
am__v_GEN_ = $(am__v_GEN_$(AM_DEFAULT_VERBOSITY))
am__v_GEN_0 = @echo "  GEN     " $@;
am__v_GEN_1 = 
AM_V_at = $(am__v_at_$(V))
am__v_at_ = $(am__v_at_$(AM_DEFAULT_VERBOSITY))
am__v_at_0 = @
am__v_at_1 = 
DEFAULT_INCLUDES = -I. -I$(srcdir)
depcomp = $(SHELL) $(top_srcdir)/build-aux/depcomp
am__depfiles_maybe = depfiles
am__mv = mv -f
COMPILE = $(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) \
	$(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS)
LTCOMPILE = $(LIBTOOL) $(AM_V_lt) --tag=CC $(AM_LIBTOOLFLAGS) \
	$(LIBTOOLFLAGS) --mode=compile $(CC) $(DEFS) \
	$(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) \
	$(AM_CFLAGS) $(CFLAGS)
AM_V_CC = $(am__v_CC_$(V))
am__v_CC_ = $(am__v_CC_$(AM_DEFAULT_VERBOSITY))
am__v_CC_0 = @echo "  CC      " $@;
am__v_CC_1 = 
CCLD = $(CC)
LINK = $(LIBTOOL) $(AM_V_lt) --tag=CC $(AM_LIBTOOLFLAGS) \
	$(LIBTOOLFLAGS) --mode=link $(CCLD) $(AM_CFLAGS) $(CFLAGS) \
	$(AM_LDFLAGS) $(LDFLAGS) -o $@
AM_V_CCLD = $(am__v_CCLD_$(V))
am__v_CCLD_ = $(am__v_CCLD_$(AM_DEFAULT_VERBOSITY))
am__v_CCLD_0 = @echo "  CCLD    " $@;
am__v_CCLD_1 = 
CCASCOMPILE = $(CCAS) $(AM_CCASFLAGS) $(CCASFLAGS)
LTCCASCOMPILE = $(LIBTOOL) $(AM_V_lt) $(AM_LIBTOOLFLAGS) \
	$(LIBTOOLFLAGS) --mode=compile $(CCAS) $(AM_CCASFLAGS) \
	$(CCASFLAGS)
AM_V_CCAS = $(am__v_CCAS_$(V))
am__v_CCAS_ = $(am__v_CCAS_$(AM_DEFAULT_VERBOSITY))
am__v_CCAS_0 = @echo "  CCAS    " $@;
am__v_CCAS_1 = 
SOURCES = $(qsort_SOURCES)
DIST_SOURCES = $(am__qsort_SOURCES_DIST)
am__can_run_installinfo = \
  case $$AM_UPDATE_INFO_DIR in \
    n|no|NO) false;; \
    *) (install-info --version) >/dev/null 2>&1;; \
  esac
am__tagged_files = $(HEADERS) $(SOURCES) $(TAGS_FILES) $(LISP)
# Read a list of newline-separated strings from the standard input,
# and print each of them once, without duplicates.  Input order is
# *not* preserved.
am__uniquify_input = $(AWK) '\
  BEGIN { nonempty = 0; } \
  { items[$$0] = 1; nonempty = 1; } \
  END { if (nonempty) { for (i in items) print i; }; } \
'
# Make sure the list of sources is unique.  This is necessary because,
# e.g., the same source file might be shared among _SOURCES variables
# for different programs/libraries.
am__define_uniq_tagged_files = \
  list='$(am__tagged_files)'; \
  unique=`for i in $$list; do \
    if test -f "$$i"; then echo $$i; else echo $(srcdir)/$$i; fi; \
  done | $(am__uniquify_input)`
ETAGS = etags
CTAGS = ctags
DISTFILES = $(DIST_COMMON) $(DIST_SOURCES) $(TEXINFOS) $(EXTRA_DIST)
ACLOCAL = ${SHELL} /home/ae/Desktop/ramoverlay/beebs/build-aux/missing aclocal-1.14
AMTAR = $${TAR-tar}
AM_CFLAGS = -mthumb -mcpu=cortex-m3 -DCORTEX_M3 -I $(top_srcdir)/src/platformcode -g \
	$(am__append_1) $(am__append_3) $(am__append_5) \
	$(am__append_7)
AM_DEFAULT_VERBOSITY = 0
AM_LDFLAGS = -lc -lnosys
AR = arm-none-eabi-ar
AUTOCONF = ${SHELL} /home/ae/Desktop/ramoverlay/beebs/build-aux/missing autoconf
AUTOHEADER = ${SHELL} /home/ae/Desktop/ramoverlay/beebs/build-aux/missing autoheader
AUTOMAKE = ${SHELL} /home/ae/Desktop/ramoverlay/beebs/build-aux/missing automake-1.14
AWK = mawk
BENCHMARKS_SUBDIRS = src/2dfir src/adpcm src/blowfish src/bs src/bsort100 src/bubblesort src/cnt src/compress src/cover src/crc src/crc32 src/ctl-string src/ctl-stack src/ctl-vector src/cubic src/dhrystone src/dijkstra src/dtoa src/duff src/edn src/expint src/fac src/fasta src/fdct src/fft src/fibcall src/fir src/float_matmult src/frac src/gdb-advance src/gdb-all-types src/gdb-anon src/gdb-arrayidx src/gdb-async src/gdb-bitfields src/gdb-constvars src/gdb-store src/huffbench src/insertsort src/int_matmult src/janne_complex src/jfdctint src/lcdnum src/levenshtein src/lms src/ludcmp src/mergesort src/miniz src/minver src/nbody src/ndes src/nettle-arcfour src/nettle-cast128 src/nettle-des src/nettle-md5 src/newlib-exp src/newlib-log src/newlib-mod src/newlib-sqrt src/ns src/nsichneu src/prime src/qsort src/qurt src/recursion src/rijndael src/select src/sglib-arraybinsearch src/sglib-arraysort src/sglib-arraysort1 src/sglib-dllist src/sglib-hashtable src/sglib-listinsertsort src/sglib-listinsertsort1 src/sglib-listsort src/sglib-queue src/sglib-rbtree src/sha src/slre src/stringsearch1 src/strstr src/sqrt src/st src/statemate src/tarai src/ud src/wikisort src/whetstone 
CC = arm-none-eabi-gcc -std=gnu99
CCAS = arm-none-eabi-gcc -std=gnu99
CCASDEPMODE = depmode=gcc3
CCASFLAGS =  -mthumb -mcpu=cortex-m3 -DCORTEX_M0
CCDEPMODE = depmode=gcc3
CFLAGS = 
CPP = arm-none-eabi-gcc -E
CPPFLAGS = 
CROSS_COMPILER_CHECK = yes
CYGPATH_W = echo
DEFS = -DPACKAGE_NAME=\"beebs\" -DPACKAGE_TARNAME=\"beebs\" -DPACKAGE_VERSION=\"1.0\" -DPACKAGE_STRING=\"beebs\ 1.0\" -DPACKAGE_BUGREPORT=\"james.pallister@embecosm.com\" -DPACKAGE_URL=\"\" -DPACKAGE=\"beebs\" -DVERSION=\"1.0\" -DSTDC_HEADERS=1 -DHAVE_SYS_TYPES_H=1 -DHAVE_SYS_STAT_H=1 -DHAVE_STDLIB_H=1 -DHAVE_STRING_H=1 -DHAVE_STRINGS_H=1 -DHAVE_INTTYPES_H=1 -DHAVE_STDINT_H=1 -DHAVE_UNISTD_H=1 -DLT_OBJDIR=\".libs/\"
DEPDIR = .deps
DLLTOOL = false
DSYMUTIL = 
DUMPBIN = 
ECHO_C = 
ECHO_N = -n
ECHO_T = 
EGREP = /bin/grep -E
EXEEXT = 
FGREP = /bin/grep -F
GREP = /bin/grep
INSTALL = /usr/bin/install -c
INSTALL_DATA = ${INSTALL} -m 644
INSTALL_PROGRAM = ${INSTALL}
INSTALL_SCRIPT = ${INSTALL}
INSTALL_STRIP_PROGRAM = $(install_sh) -c -s
LD = /usr/lib/arm-none-eabi/bin/ld
LDFLAGS =  -lc -lnosys
LIBOBJS = 
LIBS = 
LIBTOOL = $(SHELL) $(top_builddir)/libtool
LIPO = 
LN_S = ln -s
LTLIBOBJS = 
MAINT = #
MAKEINFO = ${SHELL} /home/ae/Desktop/ramoverlay/beebs/build-aux/missing makeinfo
MANIFEST_TOOL = :
MKDIR_P = /bin/mkdir -p
NM = /usr/bin/arm-none-eabi-nm -B
NMEDIT = 
OBJDUMP = arm-none-eabi-objdump
OBJEXT = o
OTOOL = 
OTOOL64 = 
PACKAGE = beebs
PACKAGE_BUGREPORT = james.pallister@embecosm.com
PACKAGE_NAME = beebs
PACKAGE_STRING = beebs 1.0
PACKAGE_TARNAME = beebs
PACKAGE_URL = 
PACKAGE_VERSION = 1.0
PATH_SEPARATOR = :
RANLIB = arm-none-eabi-ranlib
SED = /bin/sed
SET_MAKE = 
SHELL = /bin/bash
SIMULATORPATH = 
STRIP = arm-none-eabi-strip
VERSION = 1.0
abs_builddir = /home/ae/Desktop/ramoverlay/beebs_build/stm32vldiscovery/src/qsort
abs_srcdir = /home/ae/Desktop/ramoverlay/beebs_build/stm32vldiscovery/../../beebs/src/qsort
abs_top_builddir = /home/ae/Desktop/ramoverlay/beebs_build/stm32vldiscovery
abs_top_srcdir = /home/ae/Desktop/ramoverlay/beebs_build/stm32vldiscovery/../../beebs
ac_ct_AR = 
ac_ct_CC = 
ac_ct_DUMPBIN = 
am__include = include
am__leading_dot = .
am__quote = 
am__tar = $${TAR-tar} chof - "$$tardir"
am__untar = $${TAR-tar} xf -
bindir = ${exec_prefix}/bin
build = x86_64-unknown-linux-gnu
build_alias = 
build_cpu = x86_64
build_os = linux-gnu
build_vendor = unknown
builddir = .
datadir = ${datarootdir}
datarootdir = ${prefix}/share
docdir = ${datarootdir}/doc/${PACKAGE_TARNAME}
dvidir = ${docdir}
exec_prefix = ${prefix}
host = arm-none-eabi
host_alias = arm-none-eabi
host_cpu = arm
host_os = eabi
host_vendor = none
htmldir = ${docdir}
includedir = ${prefix}/include
infodir = ${datarootdir}/info
install_sh = ${SHELL} /home/ae/Desktop/ramoverlay/beebs/build-aux/install-sh
libdir = ${exec_prefix}/lib
libexecdir = ${exec_prefix}/libexec
localedir = ${datarootdir}/locale
localstatedir = ${prefix}/var
mandir = ${datarootdir}/man
mkdir_p = $(MKDIR_P)
oldincludedir = /usr/include
pdfdir = ${docdir}
prefix = /usr/local
program_transform_name = s,x,x,
psdir = ${docdir}
sbindir = ${exec_prefix}/sbin
sharedstatedir = ${prefix}/com
simulate_m0_cmd = 
simulavr_cmd = 
srcdir = ../../../../beebs/src/qsort
sysconfdir = ${prefix}/etc
target = arm-none-eabi
target_alias = 
target_cpu = arm
target_os = eabi
target_vendor = none
top_build_prefix = ../../
top_builddir = ../..
top_srcdir = ../../../../beebs
qsort_SOURCES = qsort.c ${platform_src}
platform_src = $(top_srcdir)/src/platformcode/platformcode.c \
	$(am__append_2) $(am__append_4) $(am__append_6) \
	$(am__append_8) $(am__append_9) $(am__append_10)
all: all-am

.SUFFIXES:
.SUFFIXES: .c .lo .o .obj .s
$(srcdir)/Makefile.in: # $(srcdir)/Makefile.am $(top_srcdir)/src/common.mk.am $(am__configure_deps)
	@for dep in $?; do \
	  case '$(am__configure_deps)' in \
	    *$$dep*) \
	      ( cd $(top_builddir) && $(MAKE) $(AM_MAKEFLAGS) am--refresh ) \
	        && { if test -f $@; then exit 0; else break; fi; }; \
	      exit 1;; \
	  esac; \
	done; \
	echo ' cd $(top_srcdir) && $(AUTOMAKE) --gnu src/qsort/Makefile'; \
	$(am__cd) $(top_srcdir) && \
	  $(AUTOMAKE) --gnu src/qsort/Makefile
.PRECIOUS: Makefile
Makefile: $(srcdir)/Makefile.in $(top_builddir)/config.status
	@case '$?' in \
	  *config.status*) \
	    cd $(top_builddir) && $(MAKE) $(AM_MAKEFLAGS) am--refresh;; \
	  *) \
	    echo ' cd $(top_builddir) && $(SHELL) ./config.status $(subdir)/$@ $(am__depfiles_maybe)'; \
	    cd $(top_builddir) && $(SHELL) ./config.status $(subdir)/$@ $(am__depfiles_maybe);; \
	esac;
$(top_srcdir)/src/common.mk.am:

$(top_builddir)/config.status: $(top_srcdir)/configure $(CONFIG_STATUS_DEPENDENCIES)
	cd $(top_builddir) && $(MAKE) $(AM_MAKEFLAGS) am--refresh

$(top_srcdir)/configure: # $(am__configure_deps)
	cd $(top_builddir) && $(MAKE) $(AM_MAKEFLAGS) am--refresh
$(ACLOCAL_M4): # $(am__aclocal_m4_deps)
	cd $(top_builddir) && $(MAKE) $(AM_MAKEFLAGS) am--refresh
$(am__aclocal_m4_deps):
install-binPROGRAMS: $(bin_PROGRAMS)
	@$(NORMAL_INSTALL)
	@list='$(bin_PROGRAMS)'; test -n "$(bindir)" || list=; \
	if test -n "$$list"; then \
	  echo " $(MKDIR_P) '$(DESTDIR)$(bindir)'"; \
	  $(MKDIR_P) "$(DESTDIR)$(bindir)" || exit 1; \
	fi; \
	for p in $$list; do echo "$$p $$p"; done | \
	sed 's/$(EXEEXT)$$//' | \
	while read p p1; do if test -f $$p \
	 || test -f $$p1 \
	  ; then echo "$$p"; echo "$$p"; else :; fi; \
	done | \
	sed -e 'p;s,.*/,,;n;h' \
	    -e 's|.*|.|' \
	    -e 'p;x;s,.*/,,;s/$(EXEEXT)$$//;$(transform);s/$$/$(EXEEXT)/' | \
	sed 'N;N;N;s,\n, ,g' | \
	$(AWK) 'BEGIN { files["."] = ""; dirs["."] = 1 } \
	  { d=$$3; if (dirs[d] != 1) { print "d", d; dirs[d] = 1 } \
	    if ($$2 == $$4) files[d] = files[d] " " $$1; \
	    else { print "f", $$3 "/" $$4, $$1; } } \
	  END { for (d in files) print "f", d, files[d] }' | \
	while read type dir files; do \
	    if test "$$dir" = .; then dir=; else dir=/$$dir; fi; \
	    test -z "$$files" || { \
	    echo " $(INSTALL_PROGRAM_ENV) $(LIBTOOL) $(AM_LIBTOOLFLAGS) $(LIBTOOLFLAGS) --mode=install $(INSTALL_PROGRAM) $$files '$(DESTDIR)$(bindir)$$dir'"; \
	    $(INSTALL_PROGRAM_ENV) $(LIBTOOL) $(AM_LIBTOOLFLAGS) $(LIBTOOLFLAGS) --mode=install $(INSTALL_PROGRAM) $$files "$(DESTDIR)$(bindir)$$dir" || exit $$?; \
	    } \
	; done

uninstall-binPROGRAMS:
	@$(NORMAL_UNINSTALL)
	@list='$(bin_PROGRAMS)'; test -n "$(bindir)" || list=; \
	files=`for p in $$list; do echo "$$p"; done | \
	  sed -e 'h;s,^.*/,,;s/$(EXEEXT)$$//;$(transform)' \
	      -e 's/$$/$(EXEEXT)/' \
	`; \
	test -n "$$list" || exit 0; \
	echo " ( cd '$(DESTDIR)$(bindir)' && rm -f" $$files ")"; \
	cd "$(DESTDIR)$(bindir)" && rm -f $$files

clean-binPROGRAMS:
	@list='$(bin_PROGRAMS)'; test -n "$$list" || exit 0; \
	echo " rm -f" $$list; \
	rm -f $$list || exit $$?; \
	test -n "$(EXEEXT)" || exit 0; \
	list=`for p in $$list; do echo "$$p"; done | sed 's/$(EXEEXT)$$//'`; \
	echo " rm -f" $$list; \
	rm -f $$list

qsort$(EXEEXT): $(qsort_OBJECTS) $(qsort_DEPENDENCIES) $(EXTRA_qsort_DEPENDENCIES) 
	@rm -f qsort$(EXEEXT)
	$(AM_V_CCLD)$(LINK) $(qsort_OBJECTS) $(qsort_LDADD) $(LIBS)

mostlyclean-compile:
	-rm -f *.$(OBJEXT)

distclean-compile:
	-rm -f *.tab.c

include ./$(DEPDIR)/platformcode.Po
include ./$(DEPDIR)/qsort.Po
include ./$(DEPDIR)/startup.Po

.c.o:
	$(AM_V_CC)$(COMPILE) -MT $@ -MD -MP -MF $(DEPDIR)/$*.Tpo -c -o $@ $<
	$(AM_V_at)$(am__mv) $(DEPDIR)/$*.Tpo $(DEPDIR)/$*.Po
#	$(AM_V_CC)source='$<' object='$@' libtool=no \
#	DEPDIR=$(DEPDIR) $(CCDEPMODE) $(depcomp) \
#	$(AM_V_CC_no)$(COMPILE) -c -o $@ $<

.c.obj:
	$(AM_V_CC)$(COMPILE) -MT $@ -MD -MP -MF $(DEPDIR)/$*.Tpo -c -o $@ `$(CYGPATH_W) '$<'`
	$(AM_V_at)$(am__mv) $(DEPDIR)/$*.Tpo $(DEPDIR)/$*.Po
#	$(AM_V_CC)source='$<' object='$@' libtool=no \
#	DEPDIR=$(DEPDIR) $(CCDEPMODE) $(depcomp) \
#	$(AM_V_CC_no)$(COMPILE) -c -o $@ `$(CYGPATH_W) '$<'`

.c.lo:
	$(AM_V_CC)$(LTCOMPILE) -MT $@ -MD -MP -MF $(DEPDIR)/$*.Tpo -c -o $@ $<
	$(AM_V_at)$(am__mv) $(DEPDIR)/$*.Tpo $(DEPDIR)/$*.Plo
#	$(AM_V_CC)source='$<' object='$@' libtool=yes \
#	DEPDIR=$(DEPDIR) $(CCDEPMODE) $(depcomp) \
#	$(AM_V_CC_no)$(LTCOMPILE) -c -o $@ $<

platformcode.o: $(top_srcdir)/src/platformcode/platformcode.c
	$(AM_V_CC)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -MT platformcode.o -MD -MP -MF $(DEPDIR)/platformcode.Tpo -c -o platformcode.o `test -f '$(top_srcdir)/src/platformcode/platformcode.c' || echo '$(srcdir)/'`$(top_srcdir)/src/platformcode/platformcode.c
	$(AM_V_at)$(am__mv) $(DEPDIR)/platformcode.Tpo $(DEPDIR)/platformcode.Po
#	$(AM_V_CC)source='$(top_srcdir)/src/platformcode/platformcode.c' object='platformcode.o' libtool=no \
#	DEPDIR=$(DEPDIR) $(CCDEPMODE) $(depcomp) \
#	$(AM_V_CC_no)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -c -o platformcode.o `test -f '$(top_srcdir)/src/platformcode/platformcode.c' || echo '$(srcdir)/'`$(top_srcdir)/src/platformcode/platformcode.c

platformcode.obj: $(top_srcdir)/src/platformcode/platformcode.c
	$(AM_V_CC)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -MT platformcode.obj -MD -MP -MF $(DEPDIR)/platformcode.Tpo -c -o platformcode.obj `if test -f '$(top_srcdir)/src/platformcode/platformcode.c'; then $(CYGPATH_W) '$(top_srcdir)/src/platformcode/platformcode.c'; else $(CYGPATH_W) '$(srcdir)/$(top_srcdir)/src/platformcode/platformcode.c'; fi`
	$(AM_V_at)$(am__mv) $(DEPDIR)/platformcode.Tpo $(DEPDIR)/platformcode.Po
#	$(AM_V_CC)source='$(top_srcdir)/src/platformcode/platformcode.c' object='platformcode.obj' libtool=no \
#	DEPDIR=$(DEPDIR) $(CCDEPMODE) $(depcomp) \
#	$(AM_V_CC_no)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -c -o platformcode.obj `if test -f '$(top_srcdir)/src/platformcode/platformcode.c'; then $(CYGPATH_W) '$(top_srcdir)/src/platformcode/platformcode.c'; else $(CYGPATH_W) '$(srcdir)/$(top_srcdir)/src/platformcode/platformcode.c'; fi`

startup.o: $(top_srcdir)/src/platformcode/startup.c
	$(AM_V_CC)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -MT startup.o -MD -MP -MF $(DEPDIR)/startup.Tpo -c -o startup.o `test -f '$(top_srcdir)/src/platformcode/startup.c' || echo '$(srcdir)/'`$(top_srcdir)/src/platformcode/startup.c
	$(AM_V_at)$(am__mv) $(DEPDIR)/startup.Tpo $(DEPDIR)/startup.Po
#	$(AM_V_CC)source='$(top_srcdir)/src/platformcode/startup.c' object='startup.o' libtool=no \
#	DEPDIR=$(DEPDIR) $(CCDEPMODE) $(depcomp) \
#	$(AM_V_CC_no)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -c -o startup.o `test -f '$(top_srcdir)/src/platformcode/startup.c' || echo '$(srcdir)/'`$(top_srcdir)/src/platformcode/startup.c

startup.obj: $(top_srcdir)/src/platformcode/startup.c
	$(AM_V_CC)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -MT startup.obj -MD -MP -MF $(DEPDIR)/startup.Tpo -c -o startup.obj `if test -f '$(top_srcdir)/src/platformcode/startup.c'; then $(CYGPATH_W) '$(top_srcdir)/src/platformcode/startup.c'; else $(CYGPATH_W) '$(srcdir)/$(top_srcdir)/src/platformcode/startup.c'; fi`
	$(AM_V_at)$(am__mv) $(DEPDIR)/startup.Tpo $(DEPDIR)/startup.Po
#	$(AM_V_CC)source='$(top_srcdir)/src/platformcode/startup.c' object='startup.obj' libtool=no \
#	DEPDIR=$(DEPDIR) $(CCDEPMODE) $(depcomp) \
#	$(AM_V_CC_no)$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(AM_CFLAGS) $(CFLAGS) -c -o startup.obj `if test -f '$(top_srcdir)/src/platformcode/startup.c'; then $(CYGPATH_W) '$(top_srcdir)/src/platformcode/startup.c'; else $(CYGPATH_W) '$(srcdir)/$(top_srcdir)/src/platformcode/startup.c'; fi`

.s.o:
	$(AM_V_CCAS)$(CCASCOMPILE) -c -o $@ $<

.s.obj:
	$(AM_V_CCAS)$(CCASCOMPILE) -c -o $@ `$(CYGPATH_W) '$<'`

.s.lo:
	$(AM_V_CCAS)$(LTCCASCOMPILE) -c -o $@ $<

pic32mx_startup.o: $(top_srcdir)/src/platformcode/pic32mx_startup.s
	$(AM_V_CCAS)$(CCAS) $(AM_CCASFLAGS) $(CCASFLAGS) -c -o pic32mx_startup.o `test -f '$(top_srcdir)/src/platformcode/pic32mx_startup.s' || echo '$(srcdir)/'`$(top_srcdir)/src/platformcode/pic32mx_startup.s

pic32mx_startup.obj: $(top_srcdir)/src/platformcode/pic32mx_startup.s
	$(AM_V_CCAS)$(CCAS) $(AM_CCASFLAGS) $(CCASFLAGS) -c -o pic32mx_startup.obj `if test -f '$(top_srcdir)/src/platformcode/pic32mx_startup.s'; then $(CYGPATH_W) '$(top_srcdir)/src/platformcode/pic32mx_startup.s'; else $(CYGPATH_W) '$(srcdir)/$(top_srcdir)/src/platformcode/pic32mx_startup.s'; fi`

msp430.o: $(top_srcdir)/src/platformcode/msp430.s
	$(AM_V_CCAS)$(CCAS) $(AM_CCASFLAGS) $(CCASFLAGS) -c -o msp430.o `test -f '$(top_srcdir)/src/platformcode/msp430.s' || echo '$(srcdir)/'`$(top_srcdir)/src/platformcode/msp430.s

msp430.obj: $(top_srcdir)/src/platformcode/msp430.s
	$(AM_V_CCAS)$(CCAS) $(AM_CCASFLAGS) $(CCASFLAGS) -c -o msp430.obj `if test -f '$(top_srcdir)/src/platformcode/msp430.s'; then $(CYGPATH_W) '$(top_srcdir)/src/platformcode/msp430.s'; else $(CYGPATH_W) '$(srcdir)/$(top_srcdir)/src/platformcode/msp430.s'; fi`

mostlyclean-libtool:
	-rm -f *.lo

clean-libtool:
	-rm -rf .libs _libs

ID: $(am__tagged_files)
	$(am__define_uniq_tagged_files); mkid -fID $$unique
tags: tags-am
TAGS: tags

tags-am: $(TAGS_DEPENDENCIES) $(am__tagged_files)
	set x; \
	here=`pwd`; \
	$(am__define_uniq_tagged_files); \
	shift; \
	if test -z "$(ETAGS_ARGS)$$*$$unique"; then :; else \
	  test -n "$$unique" || unique=$$empty_fix; \
	  if test $$# -gt 0; then \
	    $(ETAGS) $(ETAGSFLAGS) $(AM_ETAGSFLAGS) $(ETAGS_ARGS) \
	      "$$@" $$unique; \
	  else \
	    $(ETAGS) $(ETAGSFLAGS) $(AM_ETAGSFLAGS) $(ETAGS_ARGS) \
	      $$unique; \
	  fi; \
	fi
ctags: ctags-am

CTAGS: ctags
ctags-am: $(TAGS_DEPENDENCIES) $(am__tagged_files)
	$(am__define_uniq_tagged_files); \
	test -z "$(CTAGS_ARGS)$$unique" \
	  || $(CTAGS) $(CTAGSFLAGS) $(AM_CTAGSFLAGS) $(CTAGS_ARGS) \
	     $$unique

GTAGS:
	here=`$(am__cd) $(top_builddir) && pwd` \
	  && $(am__cd) $(top_srcdir) \
	  && gtags -i $(GTAGS_ARGS) "$$here"
cscopelist: cscopelist-am

cscopelist-am: $(am__tagged_files)
	list='$(am__tagged_files)'; \
	case "$(srcdir)" in \
	  [\\/]* | ?:[\\/]*) sdir="$(srcdir)" ;; \
	  *) sdir=$(subdir)/$(srcdir) ;; \
	esac; \
	for i in $$list; do \
	  if test -f "$$i"; then \
	    echo "$(subdir)/$$i"; \
	  else \
	    echo "$$sdir/$$i"; \
	  fi; \
	done >> $(top_builddir)/cscope.files

distclean-tags:
	-rm -f TAGS ID GTAGS GRTAGS GSYMS GPATH tags

distdir: $(DISTFILES)
	@srcdirstrip=`echo "$(srcdir)" | sed 's/[].[^$$\\*]/\\\\&/g'`; \
	topsrcdirstrip=`echo "$(top_srcdir)" | sed 's/[].[^$$\\*]/\\\\&/g'`; \
	list='$(DISTFILES)'; \
	  dist_files=`for file in $$list; do echo $$file; done | \
	  sed -e "s|^$$srcdirstrip/||;t" \
	      -e "s|^$$topsrcdirstrip/|$(top_builddir)/|;t"`; \
	case $$dist_files in \
	  */*) $(MKDIR_P) `echo "$$dist_files" | \
			   sed '/\//!d;s|^|$(distdir)/|;s,/[^/]*$$,,' | \
			   sort -u` ;; \
	esac; \
	for file in $$dist_files; do \
	  if test -f $$file || test -d $$file; then d=.; else d=$(srcdir); fi; \
	  if test -d $$d/$$file; then \
	    dir=`echo "/$$file" | sed -e 's,/[^/]*$$,,'`; \
	    if test -d "$(distdir)/$$file"; then \
	      find "$(distdir)/$$file" -type d ! -perm -700 -exec chmod u+rwx {} \;; \
	    fi; \
	    if test -d $(srcdir)/$$file && test $$d != $(srcdir); then \
	      cp -fpR $(srcdir)/$$file "$(distdir)$$dir" || exit 1; \
	      find "$(distdir)/$$file" -type d ! -perm -700 -exec chmod u+rwx {} \;; \
	    fi; \
	    cp -fpR $$d/$$file "$(distdir)$$dir" || exit 1; \
	  else \
	    test -f "$(distdir)/$$file" \
	    || cp -p $$d/$$file "$(distdir)/$$file" \
	    || exit 1; \
	  fi; \
	done
check-am: all-am
check: check-am
all-am: Makefile $(PROGRAMS)
installdirs:
	for dir in "$(DESTDIR)$(bindir)"; do \
	  test -z "$$dir" || $(MKDIR_P) "$$dir"; \
	done
install: install-am
install-exec: install-exec-am
install-data: install-data-am
uninstall: uninstall-am

install-am: all-am
	@$(MAKE) $(AM_MAKEFLAGS) install-exec-am install-data-am

installcheck: installcheck-am
install-strip:
	if test -z '$(STRIP)'; then \
	  $(MAKE) $(AM_MAKEFLAGS) INSTALL_PROGRAM="$(INSTALL_STRIP_PROGRAM)" \
	    install_sh_PROGRAM="$(INSTALL_STRIP_PROGRAM)" INSTALL_STRIP_FLAG=-s \
	      install; \
	else \
	  $(MAKE) $(AM_MAKEFLAGS) INSTALL_PROGRAM="$(INSTALL_STRIP_PROGRAM)" \
	    install_sh_PROGRAM="$(INSTALL_STRIP_PROGRAM)" INSTALL_STRIP_FLAG=-s \
	    "INSTALL_PROGRAM_ENV=STRIPPROG='$(STRIP)'" install; \
	fi
mostlyclean-generic:

clean-generic:

distclean-generic:
	-test -z "$(CONFIG_CLEAN_FILES)" || rm -f $(CONFIG_CLEAN_FILES)
	-test . = "$(srcdir)" || test -z "$(CONFIG_CLEAN_VPATH_FILES)" || rm -f $(CONFIG_CLEAN_VPATH_FILES)

maintainer-clean-generic:
	@echo "This command is intended for maintainers to use"
	@echo "it deletes files that may require special tools to rebuild."
clean: clean-am

clean-am: clean-binPROGRAMS clean-generic clean-libtool mostlyclean-am

distclean: distclean-am
	-rm -rf ./$(DEPDIR)
	-rm -f Makefile
distclean-am: clean-am distclean-compile distclean-generic \
	distclean-tags

dvi: dvi-am

dvi-am:

html: html-am

html-am:

info: info-am

info-am:

install-data-am:

install-dvi: install-dvi-am

install-dvi-am:

install-exec-am: install-binPROGRAMS

install-html: install-html-am

install-html-am:

install-info: install-info-am

install-info-am:

install-man:

install-pdf: install-pdf-am

install-pdf-am:

install-ps: install-ps-am

install-ps-am:

installcheck-am:

maintainer-clean: maintainer-clean-am
	-rm -rf ./$(DEPDIR)
	-rm -f Makefile
maintainer-clean-am: distclean-am maintainer-clean-generic

mostlyclean: mostlyclean-am

mostlyclean-am: mostlyclean-compile mostlyclean-generic \
	mostlyclean-libtool

pdf: pdf-am

pdf-am:

ps: ps-am

ps-am:

uninstall-am: uninstall-binPROGRAMS

.MAKE: install-am install-strip

.PHONY: CTAGS GTAGS TAGS all all-am check check-am clean \
	clean-binPROGRAMS clean-generic clean-libtool cscopelist-am \
	ctags ctags-am distclean distclean-compile distclean-generic \
	distclean-libtool distclean-tags distdir dvi dvi-am html \
	html-am info info-am install install-am install-binPROGRAMS \
	install-data install-data-am install-dvi install-dvi-am \
	install-exec install-exec-am install-html install-html-am \
	install-info install-info-am install-man install-pdf \
	install-pdf-am install-ps install-ps-am install-strip \
	installcheck installcheck-am installdirs maintainer-clean \
	maintainer-clean-generic mostlyclean mostlyclean-compile \
	mostlyclean-generic mostlyclean-libtool pdf pdf-am ps ps-am \
	tags tags-am uninstall uninstall-am uninstall-binPROGRAMS


# Tell versions [3.59,3.63) of GNU make to not export all variables.
# Otherwise a system limit (for SysV at least) may be exceeded.
.NOEXPORT:
