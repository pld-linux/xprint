%define		_date		2002-12-01
%define		_rel		008

Summary:	Xprint
Name:		xprint
Version:	0.0.%{_rel}
Release:	0.1
License:	MIT
Group:		X11/XFree86
Source0:	http://puck.informatik.med.uni-giessen.de/download/%{name}_mozdev_org_source-%{_date}-trunk.tar.gz
Source1:	xprintscripts.tgz
Requires:	%{name}-initrc
URL:		http://xprint.mozdev.org
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Xprint provides an advanched print API for X11-based
(incl. CDE, Xt/Motif-, Xt/LessTif-, Xt/Athena-, Qt- and
Mozilla-based) applications.

%package initrc
Summary:	Init scripts for Xprint servers
Group:		X11/XFree86
Version:	0.1
Requires:	%{name}-shellscript

%description initrc
Init scripts for Xprint servers

%package shellscript
Summary:	Init scripts for Xprint servers
Group:		X11/XFree86
Version:	0.1

%description shellscript
Init scripts for Xprint servers

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
%attr(744,root,root) %{_sysconfdir}/rc.d/init.d/xprint
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/Xprint/*

%files shellscript
%defattr(644,root,root,755)
%attr(755,root,root) %{_sysconfdir}/profile.d/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/xprint
