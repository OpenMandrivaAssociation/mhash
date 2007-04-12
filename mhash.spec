%define major 2
%define libname %mklibname mhash %{major}

Summary:	Thread-safe hash library
Name:		mhash
Version:	0.9.8
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
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

%package -n	%{libname}-devel
Summary:	Header files and libraries for developing apps which will use mhash
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libmhash-devel = %{version}
Provides:	mhash-devel = %{version}

%description -n	%{libname}-devel
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

%build

%configure2_5x \
    --enable-static \
    --enable-shared

%make

%check
make check

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall

# install _all_ headers
install -m0644 include/*.h %{buildroot}%{_includedir}/
install -m0644 include/mutils/*.h %{buildroot}%{_includedir}/mutils/

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL ChangeLog NEWS README TODO doc/*.c doc/skid2* 
%{_includedir}/*.h
%dir %{_includedir}/mutils
%{_includedir}/mutils/*.h
%{_libdir}/*.a
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_mandir}/man3/*


