#
# Conditional builds:
%bcond_without	xmms 		# disable xmms wrapping
%bcond_without	gstreamer	# disable gstreamer

Summary:	A KDE audio player
Summary(pl):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	1.0
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/amarok/%{name}-%{version}.tar.bz2
# Source0-md5:	c52d89bde4c51b17ca7cce767b4515f3
URL:		http://amarok.sf.net/
Buildrequires:	alsa-lib-devel
Buildrequires:	arts-qt-devel
Buildrequires:	automake
%{?with_gstreamer:BuildRequires:	gstreamer-devel >= 0.8.1}
BuildRequires:	kdemultimedia-devel >= 9:3.1.93
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sed >= 4.0
BuildRequires:	taglib-devel >= 0.95
BuildRequires:	unsermake >= 040511
BuildRequires:	xine-lib-devel
%{?with_xmms:Buildrequires:	xmms-devel}
Requires:	kdebase-core >= 9:3.1.93
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl
Odtwarzacz audio dla KDE.

%package gstreamer
Summary:	Plugin gstramer
Summary(pl):	Wtyczka gstreamer
Group:		X11/Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description gstreamer
Plugin gstramer.

%description gstreamer -l pl
Wtyczka gstreamer.

%prep
%setup -q -n %{name}-%{version}

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
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir}

%find_lang amarok --all-name --with-kde 

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/amarok
%doc AUTHORS ChangeLog README TODO
%{?with_xmms:%attr(755,root,root) %{_bindir}/amarok_xmmswrapper}
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

%if %{with gstreamer}
%files gstreamer
%defattr(644,root,root,755)
%{_libdir}/kde3/libamarok_gstengine_plugin.la
%attr(755,root,root) %{_libdir}/kde3/libamarok_gstengine_plugin.so
%{_datadir}/services/amarok_gstengine_plugin.desktop
%endif
