%define _disable_ld_no_undefined 1

%define pkgname CWiid
%define pre 0
%define rel 16

%if %pre
%define release %mkrel 1.%{pre}.%{rel}
%define distname %{name}-%{version}_%{pre}
%else
%define release %mkrel %{rel}
%define distname %{name}-%{version}
%endif

%define lib_major 1
%define lib_name %mklibname %{name} %{lib_major}
%define devel_name %mklibname %{name} -d
%define plugins_dir %{_libdir}/%{name}/plugins

Summary:	Cwiid Wiimote Interface
Name:		cwiid
Version:	0.6.02
Release:	%{release}
License:        GPL
Group:          System/Kernel and hardware
Url:            http://abstrakraft.org/cwiid/

Source0:	http://www.abstrakraft.org/%{distname}.tar.xz
Source1:	cwiid.service
Source2:	cwiid.sysconfig
Patch1:		linking.patch
BuildRequires:	bison
BuildRequires:	pkgconfig(bluez)
BuildRequires:	flex
BuildRequires:	lib64gtk+2.0-devel
Requires:	python-%{name}

%description
%{pkgname} is a Wiimote Interface.
The %{name} package contains the following parts:
1.%{name} library - abstracts the interface to the wiimote by hiding
  the details of the underlying Bluetooth connection
2.wmif - provides a simple text-based interface to the wiimote.
3.wmgui - provides a simple GTK gui to the wiimote.

%package -n	%{lib_name}
Summary:	%{pkgname} Wiimote library
Group:		System/Libraries

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with the %{pkgname} Wiimote library.

%package -n	%{devel_name}
Summary:	Development headers and libraries for %{pkgname}
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devel_name}
This package contains the header files and libraries needed for
developing programs using the %{pkgname} Wiimote library.

%prep
%setup -q -n %{distname}
%autopatch -p1

%build
autoreconf -vfi
%configure \
    --disable-ldconfig \
    --docdir=%{_docdir}/%{name} \
    --without-python

%make_build -j1 WARNFLAGS="%{optflags} -Wall -Wno-deprecated-declarations"

%install
%make_install
install -m 0644 -D %{SOURCE1} %{buildroot}%{_unitdir}/cwiid.service
install -m 0644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

find %{buildroot} -name "*.a" -delete

%post
%_post_service cwiid

%preun
%_preun_service cwiid

%files
%doc README.md
%doc %{_docdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/wminput/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/cwiid.service
%{_bindir}/lswm
%{_bindir}/wmgui
%{_bindir}/wminput
%{_mandir}/man1/*.1*

%files -n %{lib_name}
%{_libdir}/lib%{name}.so.%{lib_major}{,.*}
%{plugins_dir}/*.so

%files -n %{devel_name}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/cwiid.pc

