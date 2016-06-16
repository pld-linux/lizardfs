# TODO: 
# - Add daemon startup scripts
# - Verify if CGI server works, dependencies 

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


%package master
Summary:        Master/shadow metadata server
Group:          Applications
Requires:	%{name} == %{version}-%{release}
%description master
Master/shadow metadata server


%package chunkserver
Summary:        Chunk server
Group:          Applications
Requires:	%{name} == %{version}-%{release}
%description chunkserver
Chunk server


%package metalogger
Summary:        Metalogger
Group:          Applications
Requires:	%{name} == %{version}-%{release}
%description metalogger
Metalogger


%package cgiserver
Summary:        CGI server
Group:          Applications
Requires:	%{name} == %{version}-%{release}
%description cgiserver
CGI server

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
	
# /usr/etc/mfs/ ?
install -d $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT/usr/etc/mfs/  $RPM_BUILD_ROOT/etc/mfs/

install -d $RPM_BUILD_ROOT/var/lib/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# NOTE: Using same user/group as for MooseFS from mfs.spec
%groupadd -g 282 mfs
%useradd -u 282 -d /var/lib/%{name} -g mfs -c "XXX User" %{name}

%post

%preun

%postun
if [ "$1" = "0" ]; then
        %userremove mfs
        %groupremove mfs
fi

%files
%defattr(644,root,root,755)
%doc doc COPYING README UPGRADE NEWS INSTALL
## %attr(755,root,root) %{_bindir}/*
%dir /etc/mfs
%dir /var/lib/%{name}
%config(noreplace) %verify(not md5 mtime size)        /etc/mfs/globaliolimits.cfg.dist
%config(noreplace) %verify(not md5 mtime size)        /etc/mfs/iolimits.cfg.dist
%config(noreplace) %verify(not md5 mtime size)        /etc/mfs/mfsexports.cfg.dist
%config(noreplace) %verify(not md5 mtime size)        /etc/mfs/mfsgoals.cfg.dist
%config(noreplace) %verify(not md5 mtime size)        /etc/mfs/mfsmount.cfg.dist
%config(noreplace) %verify(not md5 mtime size)        /etc/mfs/mfstopology.cfg.dist
%{_mandir}

%attr(755,root,root) %{_bindir}/lizardfs-admin
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
%attr(755,root,root) %{_bindir}/mfssnapshot
%attr(755,root,root) %{_bindir}/mfstools

%attr(755,root,root) %{_sbindir}/mfsmetadump
%attr(755,root,root) %{_sbindir}/mfsmetarestore
%attr(755,root,root) %{_sbindir}/mfsrestoremaster

%files master
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfsmaster
%config(noreplace) %verify(not md5 mtime size) /etc/mfs/mfsmaster.cfg.dist
%config(noreplace) %verify(not md5 mtime size) /usr/var/lib/mfs/metadata.mfs.empty


%files chunkserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfschunkserver
%config(noreplace) %verify(not md5 mtime size) /etc/mfs/mfschunkserver.cfg.dist
%config(noreplace) %verify(not md5 mtime size)        /etc/mfs/mfshdd.cfg.dist


%files metalogger
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%config(noreplace) %verify(not md5 mtime size) /etc/mfs/mfsmetalogger.cfg.dist

%files cgiserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lizardfs-cgiserver
%attr(755,root,root) %{_sbindir}/mfscgiserv
/usr/share/mfscgi/
## %config(noreplace) %verify(not md5 mtime size) /etc/mfs/mfsmetalogger.cfg.dist


