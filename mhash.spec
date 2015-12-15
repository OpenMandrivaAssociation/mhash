%define major 2
%define libname %mklibname mhash %{major}
%define devname %mklibname mhash -d
%define _disable_rebuild_configure 1

Summary:	Thread-safe hash library
Name:		mhash
Version:	0.9.9.9
Release:	18
Group:		System/Libraries
License:	LGPLv2+
Url:		http://mhash.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/mhash/%{name}-%{version}.tar.gz
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

%package -n	%{devname}
Summary:	Header files and libraries for developing apps which will use mhash
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The mhash-devel package contains the header files and libraries needed to
develop programs that use the mhash library.

%prep
%setup -q
%apply_patches
autoreconf -fis

%build
%configure2_5x \
	--disable-static \
	--enable-shared

# If this exits, the multiarch patch needs an update.
grep 'define SIZEOF_' include/mutils/mhash_config.h && exit 1

%make

%check
make check

%install
%makeinstall_std

# install _all_ headers
install -m0644 include/*.h %{buildroot}%{_includedir}/
install -m0644 include/mutils/*.h %{buildroot}%{_includedir}/mutils/

# Eliminate some autoheader definitions which should not enter a public API.
# There are more which wait for a fix upstream.
sed -i 's!\(#define \(PACKAGE\|VERSION \).*\)!/* \1 */!g' %{buildroot}%{_includedir}/mutils/mhash_config.h

%files -n %{libname}
%{_libdir}/libmhash.so.%{major}*

%files -n %{devname}
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README TODO doc/*.c doc/skid2* 
%{_includedir}/*.h
%dir %{_includedir}/mutils
%{_includedir}/mutils/*.h
%{_libdir}/*.so
%{_mandir}/man3/*

