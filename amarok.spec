# TODO
# warning: Installed (but unpackaged) file(s) found:
#   /usr/lib/kde3/libamarok_aKode-engine.la
#   /usr/lib/kde3/libamarok_aKode-engine.so
#   /usr/share/apps/konqsidebartng/entries/amarok.desktop
#   /usr/share/apps/konqsidebartng/kicker_entries/amarok.desktop
#   /usr/share/services/amarok_aKode-engine.desktop
# - aKode engine?
#
# Conditional builds:
%bcond_without	arts		# disable arts engine
%bcond_without	gstreamer	# disable gstreamer
%bcond_without	xine		# disable xine engine
%bcond_without	xmms 		# disable xmms wrapping
%bcond_with	mysql			# enable mysql support
%bcond_with	akode			# enable aKode engine (too buggy/incomplete)
#
Summary:	A KDE audio player
Summary(pl):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	1.2.4
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/amarok/%{name}-%{version}.tar.bz2
# Source0-md5:	9a3bb2c043d1db169c6a370aff439e0f
URL:		http://amarok.kde.org/
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	arts-qt-devel
BuildRequires:	automake
%{?with_gstreamer:BuildRequires:	gstreamer-plugins-devel >= 0.8.1}
BuildRequires:	kdebase-devel
BuildRequires:	kdemultimedia-akode
BuildRequires:	kdemultimedia-devel >= 9:3.1.93
BuildRequires:	libmusicbrainz-devel
BuildRequires:	libvisual-devel >= 0.2.0
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
BuildRequires:	taglib-devel >= 1.3.1
#BuildRequires:	unsermake >= 040511
%{?with_xine:BuildRequires:		xine-lib-devel >= 2:1.0-0.rc5.0}
%{?with_xmms:BuildRequires:		xmms-devel}
%{?with_mysql:BuildRequires:		mysql-devel}
#BuildRequires:	kdebindings-kjsembed-devel
Requires:	%{name}-plugin = %{version}-%{release}
Requires:	kdebase-core >= 9:3.1.93
Requires:	kdemultimedia-audiocd >= 9:3.1.93
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl
Odtwarzacz audio dla KDE.

%package arts
Summary:	Plugin arts
Summary(pl):	Wtyczka arts
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-plugin = %{version}-%{release}

%description arts
Plugin arts.

%description arts -l pl
Wtyczka arts.

%package gstreamer
Summary:	Plugin gstreamer
Summary(pl):	Wtyczka gstreamer
Group:		X11/Applications/Multimedia
# deps, to get it working:
# mp3 decoder: gstreamer-mad
# ogg decoder: gstreamer-vorbis
# audio output driver: gstreamer-audiosink-alsa
# from gstreamer-audio-effects to control volume, etc
# needed libs:
#  at least /usr/lib/gstreamer-0.8/libgstresample.so 
#  probably /usr/lib/gstreamer-0.8/libgstadder.so
#  and probably /usr/lib/gstreamer-0.8/libgstvolume.so
# gstreamer-musicbrainz for being able to edit id3 tags on files.
Requires:	gstreamer-audio-effects
Requires:	gstreamer-audiosink
Requires:	gstreamer-mad
Requires:	gstreamer-vorbis
Requires:	gstreamer-musicbrainz
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-plugin = %{version}-%{release}

%description gstreamer
Plugin gstreamer.

%description gstreamer -l pl
Wtyczka gstreamer.

%package xine
Summary:	Plugin xine
Summary(pl):	Wtyczka xine
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	xine-plugin-audio
Provides:	%{name}-plugin = %{version}-%{release}

%description xine
Plugin xine.

%description xine -l pl
Wtyczka xine.

%prep
%setup -q

%{__sed} -i -e 's/Categories=.*/Categories=Qt;KDE;AudioVideo;Player;/' \
	amarok/src/amarok.desktop \

%build
cp -f /usr/share/automake/config.sub admin

#export UNSERMAKE=/usr/share/unsermake/unsermake

%{__make} -f admin/Makefile.common cvs

%configure \
	--disable-rpath \
	%{!?with_arts:--without-arts} \
	%{!?with_xine:--without-xine} \
	%{!?with_gstreamer:--without-gstreamer} \
	%{?with_mysql:--with-mysql} \
	--disable-final \
	--with-qt-libraries=%{_libdir} \
	--without-included-sqlite

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir}

# remove bogus dir
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/xx

%find_lang amarok --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "Remember to install libvisual-plugins-* packages if you"
echo "want to have a visualizations in amarok."

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/amarok
%{?with_xmms:%attr(755,root,root) %{_bindir}/amarok_xmmswrapper2}
%attr(755,root,root) %{_bindir}/amarokapp
%attr(755,root,root) %{_bindir}/amarok_libvisual
#%attr(755,root,root) %{_bindir}/release_amarok
%{_libdir}/kde3/konqsidebar_universalamarok.la
%attr(755,root,root) %{_libdir}/kde3/konqsidebar_universalamarok.so
%{_libdir}/kde3/libamarok_void-engine_plugin.la
%attr(755,root,root) %{_libdir}/kde3/libamarok_void-engine_plugin.so
%{_datadir}/apps/amarok
%{_datadir}/apps/konqueror/servicemenus/amarok_append.desktop
%{_datadir}/apps/konqsidebartng/add/amarok.desktop
%{_datadir}/apps/profiles/amarok.profile.xml
%{_datadir}/config/amarokrc
%{_datadir}/config.kcfg/amarok.kcfg
%{_datadir}/services/amarok_void-engine_plugin.desktop
%{_datadir}/servicetypes/amarok_plugin.desktop
%{_desktopdir}/kde/amarok.desktop
%{_iconsdir}/*/*/apps/amarok.*

%if %{with arts}
%files arts
%defattr(644,root,root,755)
%{_libdir}/kde3/libamarok_artsengine_plugin.la
%attr(755,root,root) %{_libdir}/kde3/libamarok_artsengine_plugin.so
%{_libdir}/libamarokarts.la
%attr(755,root,root) %{_libdir}/libamarokarts.so
%{_libdir}/mcop/Amarok
%{_libdir}/mcop/amarokarts.mcopclass
%{_libdir}/mcop/amarokarts.mcoptype
%{_datadir}/services/amarok_artsengine_plugin.desktop
%endif

%if %{with gstreamer}
%files gstreamer
%defattr(644,root,root,755)
%{_libdir}/kde3/libamarok_gstengine_plugin.la
%attr(755,root,root) %{_libdir}/kde3/libamarok_gstengine_plugin.so
%{_datadir}/config.kcfg/gstconfig.kcfg
%{_datadir}/services/amarok_gstengine_plugin.desktop
%endif

%if %{with xine}
%files xine
%defattr(644,root,root,755)
%{_libdir}/kde3/libamarok_xine-engine.la
%attr(755,root,root) %{_libdir}/kde3/libamarok_xine-engine.so
%{_datadir}/services/amarok_xine-engine.desktop
#%{_datadir}/services/amarok_xineengine_plugin.desktop
%endif
