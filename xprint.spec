%define		_date		2002-12-01
%define		_rel		008
%define		_init_ver	0.2

Summary:	Xprint - advanced print API for X11-based applications
Summary(pl):	Xprint - zaawansowane API do drukowania dla aplikacji opartych na X11
Name:		xprint
Version:	0.0.%{_rel}
Release:	1
License:	MIT
Group:		X11/XFree86
Source0:	http://puck.informatik.med.uni-giessen.de/download/%{name}_mozdev_org_source-%{_date}-trunk.tar.gz
Source1:	xprintscripts-%{_init_ver}.tgz
Requires:	%{name}-initrc
URL:		http://xprint.mozdev.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Xprint provides an advanced print API for X11-based (incl. CDE,
Xt/Motif-, Xt/LessTif-, Xt/Athena-, Qt- and Mozilla-based)
applications.

%description -l pl
Xprint udostêpnia zaawansowane API do drukowania dla aplikacji
opartych na X11 (w tym opartych na CDE, Xt/Motifie, Xt/LessTifie,
Xt/Athenie, Qt, Mozilli).

%package initrc
Summary:	Init scripts for Xprint servers
Summary(pl):	Skrypty startowe dla serwerów Xprint
Group:		X11/XFree86
Version:	%{_init_ver}
Requires:	%{name}-shellscript

%description initrc
Init scripts for Xprint servers.

%description initrc -l pl
Skrypty startowe dla serwerów Xprint.

%package shellscript
Summary:	Init scripts for Xprint servers
Summary(pl):	Skrypt inicjalizuj±cy dla serwerów Xprint
Group:		X11/XFree86
Version:	%{_init_ver}

%description shellscript
Init scripts for Xprint servers.

%description shellscript -l pl
Skrypt inicjalizuj±cy dla serwerów Xprint.

%prep
%setup -q -n %{name}

%build
cd src/xprint_main
%{__make} -S -C xc World DEFAULT_OS_CPU_FROB=%{_target_cpu} \
	"BOOTSTRAPCFLAGS=%{rpmcflags}" \
	"CCOPTIONS=%{rpmcflags}" \
	"CXXOPTIONS=%{rpmcflags}" \
	"CXXDEBUGFLAGS=" "CDEBUGFLAGS="
cd ../..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_bindir}
install src/xprint_main/xc/programs/Xserver/Xprt $RPM_BUILD_ROOT/%{_bindir}

gzip -dc %{SOURCE1} | tar -xf - -C $RPM_BUILD_ROOT 

%post
/sbin/chkconfig --add xprint
if [ -f /var/lock/subsys/Xprint1 ]; then
	/etc/rc.d/init.d/xprint restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/xprint start\" to start Xprint daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/Xprint1 ]; then
		/etc/rc.d/init.d/xprint stop 1>&2
	fi
	/sbin/chkconfig --del xprint
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%doc src/xprint_main/xc/doc/hardcopy/XPRINT/Xprint_FAQ.txt

%files initrc
%defattr(644,root,root,755)
%dir %{_sysconfdir}/sysconfig/Xprint
%attr(754,root,root) /etc/rc.d/init.d/xprint
%dir /etc/sysconfig/Xprint
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/Xprint/*

%files shellscript
%defattr(644,root,root,755)
%attr(755,root,root) /etc/profile.d/*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/xprint
