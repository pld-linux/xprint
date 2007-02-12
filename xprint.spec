%define		_date		2002-12-01
%define		_rel		008
Summary:	Xprint - advanced print API for X11-based applications
Summary(pl.UTF-8):   Xprint - zaawansowane API do drukowania dla aplikacji opartych na X11
Name:		xprint
Version:	0.0.%{_rel}
Release:	2
License:	MIT
Group:		X11/XFree86
Source0:	http://puck.informatik.med.uni-giessen.de/download/%{name}_mozdev_org_source-%{_date}-trunk.tar.gz
# Source0-md5:	a196f07e60c381263d252f3a53f9f036
Requires:	rc-scripts
Requires:	xprint-initrc
Requires(post,preun):	/sbin/chkconfig
URL:		http://xprint.mozdev.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
Xprint provides an advanced print API for X11-based (incl. CDE,
Xt/Motif-, Xt/LessTif-, Xt/Athena-, Qt- and Mozilla-based)
applications.

%description -l pl.UTF-8
Xprint udostępnia zaawansowane API do drukowania dla aplikacji
opartych na X11 (w tym opartych na CDE, Xt/Motifie, Xt/LessTifie,
Xt/Athenie, Qt, Mozilli).

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
install -d $RPM_BUILD_ROOT%{_bindir}

install src/xprint_main/xc/programs/Xserver/Xprt $RPM_BUILD_ROOT%{_bindir}

cd src/xprint_main/xc/programs/Xserver/XpConfig
DIRS=`find C -type d | egrep -v "CVS|Imakefile|Makefile"`
for DIR in $DIRS; do mkdir -p $RPM_BUILD_ROOT/etc/X11/xserver/$DIR; done
FILES=`find C -type f | egrep -v "CVS|Imakefile|Makefile"`
for FILE in $FILES; do cp $FILE $RPM_BUILD_ROOT/etc/X11/xserver/$FILE; done

%clean
rm -rf $RPM_BUILD_ROOT

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

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%doc src/xprint_main/xc/doc/hardcopy/XPRINT/Xprint_FAQ.txt
/etc/X11/xserver/C/print/Xprinters
/etc/X11/xserver/C/print/attributes
/etc/X11/xserver/C/print/ddx-config
/etc/X11/xserver/C/print/models/HPDJ1600C
/etc/X11/xserver/C/print/models/HPLJ4family
/etc/X11/xserver/C/print/models/PSdefault
/etc/X11/xserver/C/print/models/PSspooldir/model-config
%attr(755,root,root) /etc/X11/xserver/C/print/models/PSspooldir/spooltodir.sh
/etc/X11/xserver/C/print/models/SPSPARC2
