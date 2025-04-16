# TODO:
# - systemd service files to metalogger, cgiserver packages
# - Fix cgiserver
# - fix judy lib usage on x32 arch

Summary:	Open Source Distributed File System
Summary(pl.UTF-8):	Rozporoszony system plików Open Source
Name:		lizardfs
Version:	3.12.0
Release:	1
License:	GPL v3
Group:		Applications/File
Source0:	https://github.com/lizardfs/lizardfs/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e584aa9534f900ca04d40a4772e01302
Source1:	%{name}-master.service
Source2:	%{name}-chunkserver.service
Patch0:		system-spdlog.patch
Patch1:		x32.patch
Patch2:		0001-Add-missing-header.patch
Patch3:		spdlog.patch
Patch4:		%{name}-thrift-c++11.patch
Patch5:		%{name}-libsuffix.patch
URL:		https://github.com/lizardfs/lizardfs
BuildRequires:	/usr/bin/a2x
BuildRequires:	asciidoc
BuildRequires:	boost-devel >= 1.48.0
BuildRequires:	cmake >= 3.4.0
BuildRequires:	crcutil-devel >= 1.0
BuildRequires:	db-devel >= 5.2
BuildRequires:	docbook-dtd45-xml
%ifarch x32
BuildConflicts:	judy-devel
%else
BuildRequires:	judy-devel
%endif
BuildRequires:	libfuse-devel
BuildRequires:	libisal-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	polonaise-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	spdlog-devel >= 1.12-2
BuildRequires:	systemd-devel
BuildRequires:	thrift-devel
BuildRequires:	zlib-devel
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	systemd-units >= 0.38
Provides:	group(mfs)
Provides:	user(mfs)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LizardFS is a highly reliable, scalable and efficient distributed file
system. It spreads data over a number of physical servers, making it
visible to an end user as a single file system.

%description -l pl.UTF-8
LizardFS is jest niezawodnym, skalowalnym i efektywnym rozproszonym
systemem plików. Rozkłada dane na rózne fizyczne serwery, dająć
użytkownikowi końcowemu widok pojedynczego systemu plików.

%package libs
Summary:	LizardFS client libraries
Summary(pl.UTF-8):	Biblioteki klienta LizardFS
Group:		Libraries

%description libs
LizardFS client libraries.

%description libs -l pl.UTF-8
Biblioteki klienta LizardFS.

%package devel
Summary:	Header files for LizardFS client libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek klienta LizardFS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for LizardFS client libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek klienta LizardFS.

%package static
Summary:	Static LizardFS client libraries
Summary(pl.UTF-8):	Statyczne biblioteki klienta LizardFS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LizardFS client libraries.

%description static -l pl.UTF-8
Statyczne biblioteki klienta LizardFS.

%package master
Summary:	LizardFS master/shadow metadata server
Summary(pl.UTF-8):	Główny i zapasowy serwer metadanych LizardFS
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description master
LizardFS master/shadow metadata server.

%description master -l pl.UTF-8
Główny i zapasowy serwer metadanych LizardFS.

%package chunkserver
Summary:	LizardFS chunk server
Summary(pl.UTF-8):	Serwer porcji danych LizardFS
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description chunkserver
LizardFS chunk server.

%description chunkserver -l pl.UTF-8
Serwer porcji danych LizardFS.

%package metalogger
Summary:	LizardFS metalogger server
Summary(pl.UTF-8):	Serwer logujący zmiany metadanych LizardFS
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description metalogger
LizardFS metalogger server.

%description metalogger -l pl.UTF-8
Serwer logujący zmiany metadanych LizardFS.

%package cgiserver
Summary:	LizardFS CGI server
Summary(pl.UTF-8):	Serwer CGI LizardFS
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description cgiserver
LizardFS CGI server.

%description cgiserver -l pl.UTF-8
Serwer CGI LizardFS.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%{__rm} -r external/crcutil-1.0

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python2(\s|$),#!%{__python}\1,' \
	src/cgi/chart.cgi.in \
	src/cgi/lizardfs-cgiserver.py.in \
	src/cgi/mfs.cgi.in \
	src/cgi/cgiserv.py.in

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+bash(\s|$),#!/bin/bash\1,' \
	src/master/mfsrestoremaster.in \
	src/tools/mfstools.sh

%build
install -d build
cd build
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_INSTALL_PREFIX:PATH=/  \
	-DENABLE_CLIENT_LIB=ON \
	-DENABLE_DEBIAN_PATHS=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{systemdunitdir}}
install -d $RPM_BUILD_ROOT/var/lib/%{name}
cp -p $RPM_BUILD_ROOT/var/lib/mfs/metadata.mfs.empty $RPM_BUILD_ROOT%{_sysconfdir}/mfs
install -d $RPM_BUILD_ROOT/var/lib/%{name}/master
install -d $RPM_BUILD_ROOT/var/lib/%{name}/chunkserver
%{__mv} $RPM_BUILD_ROOT/var/lib/mfs/metadata.mfs.empty $RPM_BUILD_ROOT/var/lib/%{name}/master/metadata.mfs

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}-master.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}-chunkserver.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# NOTE: Using same user/group (mfs) as for MooseFS from mfs.spec
%groupadd -g 282 mfs
%useradd -u 282 -d /var/lib/%{name} -g mfs -c "MooseFS/LizardFS Daemon" mfs

%postun
if [ "$1" = "0" ]; then
	%userremove mfs
	%groupremove mfs
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post master
%systemd_post %{name}-master.service

%preun master
%systemd_preun %{name}-master.service

%postun master
%systemd_reload

%post chunkserver
%systemd_post %{name}-chunkserver.service

%preun chunkserver
%systemd_preun %{name}-chunkserver.service

%postun chunkserver
%systemd_reload

%files
%defattr(644,root,root,755)
%doc doc COPYING README.md UPGRADE NEWS INSTALL
%dir %{_sysconfdir}/mfs
%dir %attr(750,root,root) /var/lib/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/globaliolimits.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/iolimits.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsexports.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsgoals.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsmount.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfstopology.cfg.dist
%attr(755,root,root) %{_bindir}/lizardfs
%attr(755,root,root) %{_bindir}/lizardfs-admin
%attr(755,root,root) %{_bindir}/lizardfs-polonaise-server
%attr(755,root,root) %{_bindir}/lizardfs-probe
%attr(755,root,root) %{_bindir}/mfsappendchunks
%attr(755,root,root) %{_bindir}/mfscheckfile
%attr(755,root,root) %{_bindir}/mfsdeleattr
%attr(755,root,root) %{_bindir}/mfsdirinfo
%attr(755,root,root) %{_bindir}/mfsfileinfo
%attr(755,root,root) %{_bindir}/mfsfilerepair
%attr(755,root,root) %{_bindir}/mfsgeteattr
%attr(755,root,root) %{_bindir}/mfsgetgoal
%attr(755,root,root) %{_bindir}/mfsgettrashtime
%attr(755,root,root) %{_bindir}/mfsmakesnapshot
%attr(755,root,root) %{_bindir}/mfsmount
%attr(755,root,root) %{_bindir}/mfsrepquota
%attr(755,root,root) %{_bindir}/mfsrgetgoal
%attr(755,root,root) %{_bindir}/mfsrgettrashtime
%attr(755,root,root) %{_bindir}/mfsrsetgoal
%attr(755,root,root) %{_bindir}/mfsrsettrashtime
%attr(755,root,root) %{_bindir}/mfsseteattr
%attr(755,root,root) %{_bindir}/mfssetgoal
%attr(755,root,root) %{_bindir}/mfssetquota
%attr(755,root,root) %{_bindir}/mfssettrashtime
%attr(755,root,root) %{_bindir}/mfstools.sh
%attr(755,root,root) %{_sbindir}/mfsmetadump
%attr(755,root,root) %{_sbindir}/mfsmetarestore
%attr(755,root,root) %{_sbindir}/mfsrestoremaster
%{_mandir}/man1/mfs*.1*
%{_mandir}/man1/lizardfs-*.1*
%{_mandir}/man1/lizardfs.1*
%{_mandir}/man5/globaliolimits.cfg.5*
%{_mandir}/man5/iolimits.cfg.5*
%{_mandir}/man5/mfs*.cfg.5*
%{_mandir}/man7/lizardfs.7*
%{_mandir}/man7/mfs.7
%{_mandir}/man7/moosefs.7
%{_mandir}/man8/lizardfs-admin.8*
%{_mandir}/man8/lizardfs-cgiserver.8*
%{_mandir}/man8/lizardfs-probe.8
%{_mandir}/man8/mfs*.8*
/etc/bash_completion.d/lizardfs

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblizardfs-client.so
%attr(755,root,root) %{_libdir}/liblizardfsmount_shared.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/lizardfs
%{_libdir}/liblizardfs-client-cpp_pic.a

%files static
%defattr(644,root,root,755)
%{_libdir}/liblizardfs-client.a
%{_libdir}/liblizardfs-client_pic.a
%{_libdir}/liblizardfs-client-cpp.a

%files master
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfsmaster
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsmaster.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/metadata.mfs.empty
%dir %attr(750,mfs,mfs) /var/lib/%{name}/master
%config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/master/metadata.mfs
%{systemdunitdir}/%{name}-master.service

%files chunkserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfschunkserver
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfschunkserver.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfshdd.cfg.dist
%dir %attr(750,mfs,mfs) /var/lib/%{name}/chunkserver
%{systemdunitdir}/%{name}-chunkserver.service

%files metalogger
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsmetalogger.cfg.dist
# %dir %attr(750,mfs,mfs) /var/lib/%{name}/metalogger

%files cgiserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lizardfs-cgiserver
%attr(755,root,root) %{_sbindir}/mfscgiserv
%{_datadir}/mfscgi
