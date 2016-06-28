# TODO:
# - Add daemon startup scripts
#   https://github.com/moosefs/moosefs/blob/master/systemd/moosefs-master.service.in
# - Verify if CGI server works, dependencies
# - Fix x32 asm code inside crcutil-1.0
# - Consider using external libcrcutil package

Summary:	Open Source Distributed File System
Summary(pl.UTF-8):	Rozporoszony system plików Open Source
Name:		lizardfs
Version:	3.9.4
Release:	0.4
License:	GPL v3
Group:		Applications
Source0:	https://github.com/lizardfs/lizardfs/archive/v.%{version}.tar.gz
# Source0-md5:	71766d18a5066506e54d952ab6056bd3
Patch0:		%{name}-cmake_fix.patch
URL:		https://github.com/lizardfs/lizardfs
BuildRequires:	/usr/bin/a2x
BuildRequires:	asciidoc
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.4.0
BuildRequires:	docbook-dtd45-xml
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	zlib-devel
ExclusiveArch:	%{ix86} %{x8664}

# Requires:
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
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

%package master
Summary:	Master/shadow metadata server
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description master
Master/shadow metadata server

%package chunkserver
Summary:	Chunk server
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description chunkserver
Chunk server

%package metalogger
Summary:	Metalogger
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description metalogger
Metalogger

%package cgiserver
Summary:	CGI server
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description cgiserver
CGI server

%prep
%setup -q -n %{name}-v.%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake 	../   \
      -DBUILD_SHARED_LIBS=FALSE \
      -DCMAKE_INSTALL_PREFIX:PATH=/  \
      -DENABLE_DEBIAN_PATHS=TRUE
      
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# %{_prefix}%{_sysconfdir}/mfs/ ?
install -d $RPM_BUILD_ROOT%{_sysconfdir}
## mv $RPM_BUILD_ROOT%{_prefix}%{_sysconfdir}/mfs/ $RPM_BUILD_ROOT%{_sysconfdir}/mfs/

install -d $RPM_BUILD_ROOT/var/lib/%{name}
cp $RPM_BUILD_ROOT/var/lib/mfs/metadata.mfs.empty $RPM_BUILD_ROOT%{_sysconfdir}/mfs/
install -d $RPM_BUILD_ROOT/var/lib/%{name}/master
install -d $RPM_BUILD_ROOT/var/lib/%{name}/chunkserver
mv $RPM_BUILD_ROOT/var/lib/mfs/metadata.mfs.empty $RPM_BUILD_ROOT/var/lib/%{name}/master/metadata.mfs

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

%files
%defattr(644,root,root,755)
%doc doc COPYING README UPGRADE NEWS INSTALL
%dir %{_sysconfdir}/mfs
%dir %attr(750,root,root) /var/lib/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/globaliolimits.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/iolimits.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsexports.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsgoals.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsmount.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfstopology.cfg.dist
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
%{_mandir}/man1/mfs*.1*
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

%files master
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfsmaster
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsmaster.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/metadata.mfs.empty
%dir %attr(750,mfs,mfs) /var/lib/%{name}/master
%config(noreplace) %verify(not md5 mtime size) /var/lib/%{name}/master/metadata.mfs

%files chunkserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfschunkserver
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfschunkserver.cfg.dist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfshdd.cfg.dist
%dir %attr(750,mfs,mfs) /var/lib/%{name}/chunkserver

%files metalogger
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mfs/mfsmetalogger.cfg.dist
# %dir %attr(750,mfs,mfs) /var/lib/%{name}/metalogger

%files cgiserver
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lizardfs-cgiserver
%attr(755,root,root) %{_sbindir}/mfscgiserv
%{_datadir}/mfscgi/
# %dir %attr(750,mfs,mfs) /var/lib/%{name}/cgiserver
