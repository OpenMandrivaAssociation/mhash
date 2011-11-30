%define major 2
%define libname %mklibname mhash %{major}
%define develname %mklibname mhash -d

Summary:	Thread-safe hash library
Name:		mhash
Version:	0.9.9.9
Release:	%mkrel 7
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README TODO doc/*.c doc/skid2* 
%{_includedir}/*.h
%dir %{_includedir}/mutils
%{_includedir}/mutils/*.h
%{_libdir}/*.so
%{_mandir}/man3/*
