%define major 2
%define libname %mklibname mhash %{major}
%define develname %mklibname mhash -d

Summary:	Thread-safe hash library
Name:		mhash
Version:	0.9.9.9
Release:	8
Group:		System/Libraries
License:	LGPLv2+
Patch2: mhash-0.9.9.9-align.patch
Patch3: mhash-0.9.9.9-force64bit-tiger.patch
# Taken from Gentoo: 
# http://mirror.its.uidaho.edu/pub/gentoo-portage/app-crypt/mhash/files/mhash-0.9.9-fix-snefru-segfault.patch
Patch4: mhash-0.9.9.9-fix-snefru-segfault.patch
# Taken from Gentoo:
# http://mirror.its.uidaho.edu/pub/gentoo-portage/app-crypt/mhash/files/mhash-0.9.9-fix-mem-leak.patch
Patch5: mhash-0.9.9.9-fix-mem-leak.patch
# Taken from Gentoo:
# http://mirror.its.uidaho.edu/pub/gentoo-portage/app-crypt/mhash/files/mhash-0.9.9-fix-whirlpool-segfault.patch
Patch6: mhash-0.9.9.9-fix-whirlpool-segfault.patch
# Taken from Gentoo:
# http://mirror.its.uidaho.edu/pub/gentoo-portage/app-crypt/mhash/files/mhash-0.9.9-autotools-namespace-stomping.patch
Patch7: mhash-0.9.9.9-autotools-namespace-stomping.patch
# Taken from openpkg:
# http://www.mail-archive.com/openpkg-cvs@openpkg.org/msg26353.html
Patch8: mhash-0.9.9.9-maxint.patch
# Taken from Jitesh Shah
# http://ftp.uk.linux.org/pub/armlinux/fedora/diffs-f11/mhash/0001-Alignment-fixes.patch
Patch9: mhash-0.9.9.9-alignment.patch
# Fix keygen_test
Patch10: mhash-0.9.9.9-keygen_test_fix.patch
URL:		http://mhash.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/mhash/%{name}-%{version}.tar.gz

%description
Mhash is a thread-safe hash library, implemented in C, and provides a uniform
interface to a large number of hash algorithms (MD5, SHA-1, HAVAL, RIPEMD128,
RIPEMD160, TIGER, GOST). These algorithms can be used to compute checksums,
message digests, and other signatures. The HMAC support implements the basics
for message authentication,  following RFC 2104.

%package -n	%{libname}
Summary:	Thread-safe hash library
Group:		System/Libraries

%description -n	%{libname}
Mhash is a thread-safe hash library, implemented in C, and provides a uniform
interface to a large number of hash algorithms (MD5, SHA-1, HAVAL, RIPEMD128,
RIPEMD160, TIGER, GOST). These algorithms can be used to compute checksums,
message digests, and other signatures. The HMAC support implements the basics
for message authentication,  following RFC 2104.

%package -n	%{develname}
Summary:	Header files and libraries for developing apps which will use mhash
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	mhash-devel = %{version}-%{release}
Obsoletes:	%{mklibname mhash 2 -d}

%description -n	%{develname}
Mhash is a thread-safe hash library, implemented in C, and provides a uniform
interface to a large number of hash algorithms (MD5, SHA-1, HAVAL, RIPEMD128,
RIPEMD160, TIGER, GOST). These algorithms can be used to compute checksums,
message digests, and other signatures. The HMAC support implements the basics
for message authentication,  following RFC 2104.

The mhash-devel package contains the header files and libraries needed to
develop programs that use the mhash library.

Install the mhash-devel package if you want to develop applications that will
use the mhash library.

%prep

%setup -q
%patch2 -p1 -b .alignment
%patch3 -p1 -b .force64bit-tiger
%patch4 -p1 -b .fix-snefru-segfault
%patch5 -p1 -b .fix-mem-leak
%patch6 -p1 -b .fix-whirlpool-segfault
%patch7 -p1 -b .fix-autotool-stomping
%patch8 -p1 -b .maxint
%patch9 -p1 -b .alignment2
%patch10 -p1 -b .fix

%build
autoreconf -fis

%configure2_5x \
    --disable-static \
    --enable-shared

# If this exits, the multiarch patch needs an update.
grep 'define SIZEOF_' include/mutils/mhash_config.h && exit 1

%make

%check
make check

%install
rm -rf %{buildroot}

%makeinstall_std

# install _all_ headers
install -m0644 include/*.h %{buildroot}%{_includedir}/
install -m0644 include/mutils/*.h %{buildroot}%{_includedir}/mutils/

# Eliminate some autoheader definitions which should not enter a public API.
# There are more which wait for a fix upstream.
sed -i 's!\(#define \(PACKAGE\|VERSION \).*\)!/* \1 */!g' %{buildroot}%{_includedir}/mutils/mhash_config.h

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README TODO doc/*.c doc/skid2* 
%{_includedir}/*.h
%dir %{_includedir}/mutils
%{_includedir}/mutils/*.h
%{_libdir}/*.so
%{_mandir}/man3/*


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.9.9-6mdv2011.0
+ Revision: 666422
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.9.9-5mdv2011.0
+ Revision: 606640
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.9.9-4mdv2010.1
+ Revision: 519041
- rebuild

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9.9.9-3mdv2010.0
+ Revision: 453399
- sync with mhash-0.9.9.9-3.fc12.src.rpm

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.9.9-1mdv2009.1
+ Revision: 316254
- 0.9.9.9

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.9.9-6mdv2009.0
+ Revision: 223257
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.9.9-5mdv2008.1
+ Revision: 153075
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.9.9-4mdv2008.0
+ Revision: 89929
- rebuild

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.9-3mdv2008.0
+ Revision: 83414
- fix deps

* Thu Sep 06 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.9-2mdv2008.0
+ Revision: 81139
- bump release due to build system problems
- 0.9.9


* Tue Feb 20 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9.8-1mdv2007.0
+ Revision: 123011
- 0.9.8
- drop the ppc patch, it's implemented upstream

* Fri Dec 22 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.7-2mdv2007.1
+ Revision: 101493
- patch0: fix haval on ppc for testsuite

* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.7-1mdv2007.1
+ Revision: 74194
- Import mhash

* Mon Jun 26 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.7-1mdk
- 0.9.7

* Fri Mar 31 2006 Götz Waschk <waschk@mandriva.org> 0.9.6-1mdk
- drop patches
- New release 0.9.6

* Fri Jan 20 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.4a-3mdk
- patch1: fix MIX32 byteswap macro (for big endian systems)

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.4a-2mdk
- install missing headers
- fix the test suite on x86_64 (P0 by Giuseppe Ghibò)
- fix deps

* Tue Jan 10 2006 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.4a-1mdk
- 0.9.4a

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.2-2mdk
- make it build on 10.0 too

* Thu Jan 13 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.2-1mdk
- 0.9.2
- run the test suite

* Mon Apr 19 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.9.1-1mdk
- 0.9.1

