# TODO
# - try not to link with static mysql

%define		state	stable
%define		qtver	4.5.0

Summary:	A KDE audio player
Summary(pl.UTF-8):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	2.1
Release:	2
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.kde.org/pub/kde/%{state}/amarok/%{version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	76e5496a1bf2a8116210143f6479c1fb
Patch0:		%{name}-link.patch
Patch1:		%{name}-qthreadpool.patch
URL:		http://amarok.kde.org/
BuildRequires:	Qt3Support-devel >= %{qtver}
BuildRequires:	QtCore-devel >= %{qtver}
BuildRequires:	QtDBus-devel >= %{qtver}
BuildRequires:	QtDesigner-devel >= %{qtver}
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtOpenGL-devel >= %{qtver}
BuildRequires:	QtScript-devel >= %{qtver}
BuildRequires:	QtSql-devel >= %{qtver}
BuildRequires:	QtSvg-devel >= %{qtver}
BuildRequires:	QtTest-devel >= %{qtver}
BuildRequires:	QtUiTools-devel >= %{qtver}
BuildRequires:	QtWebKit-devel >= %{qtver}
BuildRequires:	QtXml-devel >= %{qtver}
BuildRequires:	automoc4
BuildRequires:	cmake >= 2.6.1-2
BuildRequires:	curl-devel
BuildRequires:	giflib-devel
BuildRequires:	glib2-devel
BuildRequires:	kde4-kdebase-devel
BuildRequires:	kde4-kdemultimedia-devel
BuildRequires:	libgpod-devel >= 0.7.0
BuildRequires:	libifp-devel >= 1.0.0.2
BuildRequires:	libmtp-devel >= 0.3.0
BuildRequires:	libnjb-devel >= 2.2.4
BuildRequires:	libvisual-devel >= 0.4.0
BuildRequires:	loudmouth-devel
BuildRequires:	mpeg4ip-devel >= 1:1.6
BuildRequires:	mysql-devel >= 5.1.31-3
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-qmake >= %{qtver}
BuildRequires:	qtscriptbindings
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	soprano-devel >= 2.1
BuildRequires:	strigi-devel >= 0.5.10
BuildRequires:	taglib-devel
BuildRequires:	taglib-extras-devel >= 0.1
BuildRequires:	utempter-devel
BuildRequires:	xorg-lib-libXpm-devel
Requires(post,postun):	/sbin/ldconfig
Requires:	kde4-kdebase-core
Requires:	kde4-kdemultimedia-audiocd
Requires:	kde4-phonon
Requires:	qtscriptbindings
Suggests:	libvisual-plugin-actor-JESS
Suggests:	libvisual-plugin-actor-bumpscope
Suggests:	libvisual-plugin-actor-corona
Suggests:	libvisual-plugin-actor-flower
Suggests:	libvisual-plugin-actor-gdkpixbuf
Suggests:	libvisual-plugin-actor-gforce
Suggests:	libvisual-plugin-actor-gstreamer
Suggests:	libvisual-plugin-actor-infinite
Suggests:	libvisual-plugin-actor-jakdaw
Suggests:	libvisual-plugin-actor-lv_analyzer
Suggests:	libvisual-plugin-actor-lv_gltest
Suggests:	libvisual-plugin-actor-lv_scope
Suggests:	libvisual-plugin-actor-madspin
Suggests:	libvisual-plugin-actor-nastyfft
Suggests:	libvisual-plugin-actor-oinksie
Suggests:	libvisual-plugin-input-alsa
Suggests:	libvisual-plugin-input-esd
Suggests:	libvisual-plugin-input-jack
Suggests:	libvisual-plugin-input-mplayer
Suggests:	libvisual-plugin-morph-alphablend
Suggests:	libvisual-plugin-morph-flash
Suggests:	libvisual-plugin-morph-slide
Suggests:	libvisual-plugin-morph-tentacle
Obsoletes:	amarok-arts
Obsoletes:	amarok-xmms
# It should require mysql-embeded
Requires:	mysql >= 5.1.31-3
Conflicts:	mysql < 5.1.31-3
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl.UTF-8
Odtwarzacz audio dla KDE.

%package scripts
Summary:	amaroK scripts
Summary(pl.UTF-8):	Skrypty amaroKa
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	kde4-kdebase-kdialog

%description scripts
amaroK scripts allow you extend amaroK functionality.

You can learn more about scripts in amaroK from here:
<http://amarok.kde.org/amarokwiki/index.php/Script-Writing_HowTo>.

%description scripts -l pl.UTF-8
Skrypty amaroKa pozwalające rozszerzać jego funkcjonalność.

Więcej o skryptach w amaroKu można dowiedzieć się stąd:
<http://amarok.kde.org/amarokwiki/index.php/Script-Writing_HowTo>.

%prep
%setup -q
%patch0 -p0
#%patch1 -p0

%build
install -d build
cd build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DCMAKE_BUILD_TYPE=%{!?debug:release}%{?debug:debug} \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64 \
%endif
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir}

# remove bogus dir
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/xx

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/amarok
%attr(755,root,root) %{_bindir}/amarokcollectionscanner
%attr(755,root,root) %{_bindir}/amarokmp3tunesharmonydaemon
%attr(755,root,root) %{_bindir}/amarok_afttagger
%attr(755,root,root) %ghost %{_libdir}/libamaroklib.so.?
%attr(755,root,root) %{_libdir}/libamaroklib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamarokpud.so.?
%attr(755,root,root) %{_libdir}/libamarokpud.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediadevicelib.so.?
%attr(755,root,root) %{_libdir}/libmediadevicelib.so.*.*.*
%attr(755,root,root) %{_libdir}/strigi/strigita_audible.so
%attr(755,root,root) %{_libdir}/strigi/strigita_mp4.so
%attr(755,root,root) %{_libdir}/kde4/amarok_containment_vertical.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_bookmark.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_currenttrack.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_lyrics.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_serviceinfo.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_wikipedia.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_albums.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_opmldirectory.so
%attr(755,root,root) %{_libdir}/kde4/libamarok_collection-ipodcollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_current.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_lyrics.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_service.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_wikipedia.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_ampache.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_jamendo.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_lastfm.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_magnatunestore.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_mp3tunes.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_shoutcast.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_ampache.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_lastfm.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_magnatunestore.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_mp3tunes.so
%attr(755,root,root) %{_libdir}/kde4/libamarok_collection-daapcollection.so
%attr(755,root,root) %{_libdir}/kde4/libamarok_collection-sqlcollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_mediadevices.so
%attr(755,root,root) %{_libdir}/kde4/libamarok_collection-mtpcollection.so
%attr(755,root,root) %{_libdir}/kde4/libamarok_massstorage-device.so
%attr(755,root,root) %{_libdir}/libamarok_service_liblastfm.so
%dir %{_datadir}/apps/amarok
%dir %{_datadir}/apps/amarok/scripts
%{_datadir}/apps/amarok/data
%{_datadir}/apps/amarok/icons
%{_datadir}/apps/amarok/images
%{_datadir}/apps/desktoptheme
%{_datadir}/config.kcfg/amarokconfig.kcfg
%{_datadir}/config/amarok.knsrc
%{_datadir}/dbus-1/interfaces/org.freedesktop.MediaPlayer.player.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.MediaPlayer.root.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.MediaPlayer.tracklist.xml
%{_datadir}/kde4/services/amarok.protocol
%{_datadir}/kde4/services/amaroklastfm.protocol
%{_datadir}/kde4/services/ServiceMenus/amarok_append.desktop
%{_datadir}/kde4/services/amarok-containment-vertical.desktop
%{_datadir}/kde4/services/amarok-context-applet-bookmark.desktop
%{_datadir}/kde4/services/amarok-context-applet-currenttrack.desktop
%{_datadir}/kde4/services/amarok-context-applet-lyrics.desktop
%{_datadir}/kde4/services/amarok-context-applet-serviceinfo.desktop
%{_datadir}/kde4/services/amarok-context-applet-wikipedia.desktop
%{_datadir}/kde4/services/amarok-context-applet-mediadevices.desktop
%{_datadir}/kde4/services/amarok_collection-mtpcollection.desktop
%{_datadir}/kde4/services/amarok-data-engine-current.desktop
%{_datadir}/kde4/services/amarok-data-engine-lyrics.desktop
%{_datadir}/kde4/services/amarok-data-engine-service.desktop
%{_datadir}/kde4/services/amarok-data-engine-wikipedia.desktop
%{_datadir}/kde4/services/amarok_collection-daapcollection.desktop
%{_datadir}/kde4/services/amarok_collection-sqlcollection.desktop
%{_datadir}/kde4/services/amarok_service_ampache.desktop
%{_datadir}/kde4/services/amarok_service_ampache_config.desktop
%{_datadir}/kde4/services/amarok_service_jamendo.desktop
%{_datadir}/kde4/services/amarok_service_lastfm.desktop
%{_datadir}/kde4/services/amarok_service_lastfm_config.desktop
%{_datadir}/kde4/services/amarok_service_magnatunestore.desktop
%{_datadir}/kde4/services/amarok_service_magnatunestore_config.desktop
%{_datadir}/kde4/services/amarok_service_mp3tunes.desktop
%{_datadir}/kde4/services/amarok_service_mp3tunes_config.desktop
%{_datadir}/kde4/services/amarok_service_shoutcast.desktop
%{_datadir}/kde4/services/amarok-context-applet-albums.desktop
%{_datadir}/kde4/services/amarok_collection-ipodcollection.desktop
%{_datadir}/kde4/services/amarok_massstorage-device.desktop
%{_datadir}/kde4/services/amarok_service_opmldirectory.desktop
%{_datadir}/kde4/servicetypes/amarok_context_applet.desktop
%{_datadir}/kde4/servicetypes/amarok_data_engine.desktop
%{_datadir}/kde4/servicetypes/amarok_plugin.desktop
%{_datadir}/kde4/servicetypes/amarok_codecinstall.desktop
%{_desktopdir}/kde4/amarok.desktop
%{_iconsdir}/*/*/apps/amarok.*
%{_datadir}/config/amarok_homerc

%files scripts
%defattr(644,root,root,755)
%dir %{_datadir}/apps/amarok/scripts/radio_station_service
%{_datadir}/apps/amarok/scripts/radio_station_service/main.js
%{_datadir}/apps/amarok/scripts/radio_station_service/script.spec
%dir %{_datadir}/apps/amarok/scripts/script_console
%{_datadir}/apps/amarok/scripts/script_console/main.js
%{_datadir}/apps/amarok/scripts/script_console/script.spec
%dir %{_datadir}/apps/amarok/scripts/lyrics_lyricwiki
%{_datadir}/apps/amarok/scripts/lyrics_lyricwiki/main.js
%{_datadir}/apps/amarok/scripts/lyrics_lyricwiki/script.spec
%dir %{_datadir}/apps/amarok/scripts/librivox_service
%{_datadir}/apps/amarok/scripts/librivox_service/main.js
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxLogo.png
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxService.html
%{_datadir}/apps/amarok/scripts/librivox_service/script.spec
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxEmblem.png
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxIcon.png
%{_datadir}/apps/amarok/scripts/librivox_service/audio_book128.png
