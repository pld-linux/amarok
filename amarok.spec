
%define		_ver		1.0
%define		_snap		040511
%define		_packager	adgor

Summary:	A KDE audio player
Summary(pl):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	%{_ver}
Release:	0.%{_snap}.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://ep09.pld-linux.org/~%{_packager}/kde/%{name}-%{_snap}.tar.bz2
# Source0-md5:	ad33ab910393bba33f27bd90400498e9
#Source0:	http://dl.sourceforge.net/amarok/%{name}-%{version}.tar.bz2
URL:		http://amarok.sf.net/
Buildrequires:	arts-qt-devel
Buildrequires:	automake
BuildRequires:	kdemultimedia-devel >= 9:3.1.93
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sed >= 4.0
BuildRequires:	taglib-devel >= 0.95
BuildRequires:	unsermake >= 040511
BuildRequires:	xine-lib-devel
Requires:	kdebase-core >= 9:3.1.93
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl
Odtwarzacz audio dla KDE.

%prep
%setup -q -n %{name}-%{_snap}

%build
cp -f /usr/share/automake/config.sub admin

export UNSERMAKE=/usr/share/unsermake/unsermake

%{__make} -f admin/Makefile.common cvs

%configure \
	--disable-rpath \
	--with-qt-libraries=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir}

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/amarok
%attr(755,root,root) %{_bindir}/amarok_xmmswrapper
%attr(755,root,root) %{_bindir}/amarokapp
%{_libdir}/kde3/libamarok_artsengine_plugin.la
%attr(755,root,root) %{_libdir}/kde3/libamarok_artsengine_plugin.so
%{_libdir}/libamarokarts.la
%attr(755,root,root) %{_libdir}/libamarokarts.so
%{_libdir}/mcop/Amarok
%{_libdir}/mcop/amarokarts.mcopclass
%{_libdir}/mcop/amarokarts.mcoptype
%{_datadir}/apps/amarok
%{_datadir}/config.kcfg/amarok.kcfg
%{_datadir}/services/amarok_artsengine_plugin.desktop
%{_datadir}/servicetypes/amarok_plugin.desktop
%{_desktopdir}/kde/amarok.desktop
%{_iconsdir}/[!l]*/*/apps/amarok.png
%{_datadir}/config/*
