Summary:	Open Source Distributed File System
Summary(pl.UTF-8):	Rozporoszony system plików Open Source
Name:		lizardfs
Version:	3.9.4
Release:	0.1
License:	GPL v3
Group:		Applications
Source0:	https://github.com/%{name}/%{name}/archive/v.%{version}.tar.gz
# Source0-md5:	71766d18a5066506e54d952ab6056bd3
Patch0:          %{name}-cmake_fix.patch
URL:		https://github.com/lizardfs/lizardfs
BuildRequires:  cmake >= 3.4.0
BuildRequires:  zlib-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig
BuildRequires:  /usr/bin/a2x			# asciidoc
BuildRequires:  docbook-dtd45-xml
BuildRequires:  libfuse-devel
# Requires:	
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LizardFS is a highly reliable, scalable and efficient distributed file system. 
It spreads data over a number of physical servers, making it visible to an end user as a single file system.

%description -l pl.UTF-8
LizardFS is jest niezawodnym, skalowalnym i efektywnym rozproszonym systemem plików.
Rozkłada dane na rózne fizyczne serwery, dająć użytkownikowi końcowemu widok pojedynczego systemu plików.

%prep
%setup -q -n lizardfs-v.%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_BUILD_TYPE=Release  \
        ../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc COPYING README UPGRADE NEWS INSTALL
%attr(755,root,root) %{_bindir}/*
