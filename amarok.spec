#
# TODO
# - use mysql-embedded in the future and try not to link with static mysqld lib
# - amarok now requires his own database which is not automaticly created
# Add spec:
# libmygpo-qt (1.0.5 or higher)  <http://wiki.gpodder.org/wiki/Libmygpo-qt>
#     Enable gpodder.net service
# -- Performing Test COMPLEX_TAGLIB_FILENAME - Failed
# /home/users/builder/rpm/BUILD/amarok-2.5.0/build/CMakeFiles/CMakeTmp/src.cxx:5:38: error: cannot convert 'const wchar_t*' to 'TagLib::FileName {aka const char*}' in initialization
%define		state	stable
%define		qtver	4.7.1
%define		kdever	4.5.5

Summary:	A KDE audio player
Summary(pl.UTF-8):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	2.8.0
Release:	3
License:	GPL v2+ and LGPL v2.1+
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.kde.org/pub/kde/%{state}/amarok/%{version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	53cfcb4819668b10e13b061478c7b32a
Patch0:		%{name}-upnp-dep.patch
URL:		http://amarok.kde.org/
BuildRequires:	QtNetwork-devel >= %{qtver}
BuildRequires:	QtSql-devel >= %{qtver}
BuildRequires:	automoc4 >= 0.9.88
BuildRequires:	cmake >= 2.8.0
BuildRequires:	curl-devel
BuildRequires:	ffmpeg-devel >= 0.7.1
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	herqq-devel
BuildRequires:	kde4-kdelibs-devel >= %{kdever}
BuildRequires:	libaio-devel
BuildRequires:	libgpod-devel >= 0.7.0
BuildRequires:	liblastfm-devel
BuildRequires:	libmtp-devel >= 1.0.4
BuildRequires:	libofa-devel
BuildRequires:	libwrap-devel
BuildRequires:	loudmouth-devel
BuildRequires:	mysql-devel >= 5.1.31-3
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	qca-devel
BuildRequires:	qjson-devel >= 0.5
BuildRequires:	qt4-build >= %{qtver}
BuildRequires:	qt4-qmake >= %{qtver}
BuildRequires:	qtscriptbindings
BuildRequires:	rpmbuild(macros) >= 1.600
BuildRequires:	soprano-devel
BuildRequires:	strigi-devel >= 0.7.0
BuildRequires:	taglib-devel >= 1.7
BuildRequires:	taglib-extras-devel >= 1.0.0
BuildRequires:	xorg-lib-libXpm-devel
Requires(post,postun):	/sbin/ldconfig
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
%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DKDE4_BUILD_TESTS=OFF \
	-DWITH_MYSQL_EMBEDDED=OFF \
	../

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir}

# remove unsupported locale
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/sr@ijekavian*

# remove .so symlinks so that noone gets the stupid idea to package them
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libamarok*.so

%find_lang %{name} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post		-p /sbin/ldconfig
%postun		-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/amarok
%attr(755,root,root) %{_bindir}/amarokpkg
%attr(755,root,root) %{_bindir}/amarokcollectionscanner
%attr(755,root,root) %{_bindir}/amarokmp3tunesharmonydaemon
%attr(755,root,root) %{_bindir}/amarok_afttagger
%attr(755,root,root) %{_bindir}/amzdownloader
%attr(755,root,root) %ghost %{_libdir}/libamarok-sqlcollection.so.?
%attr(755,root,root) %{_libdir}/libamarok-sqlcollection.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamarokocsclient.so.?
%attr(755,root,root) %{_libdir}/libamarokocsclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamaroklib.so.?
%attr(755,root,root) %{_libdir}/libamaroklib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamarokpud.so.?
%attr(755,root,root) %{_libdir}/libamarokpud.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamarokcore.so.?
%attr(755,root,root) %{_libdir}/libamarokcore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamarokshared.so.?
%attr(755,root,root) %{_libdir}/libamarokshared.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamarok-transcoding.so.?
%attr(755,root,root) %{_libdir}/libamarok-transcoding.so.*.*.*
#%%attr(755,root,root) %ghost %{_libdir}/libamarokqtjson.so.?
#%%attr(755,root,root) %{_libdir}/libamarokqtjson.so.*.*.*
%attr(755,root,root) %{_libdir}/libampache_account_login.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-audiocdcollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-daapcollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-ipodcollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-mtpcollection.so
#%%attr(755,root,root) %{_libdir}/kde4/amarok_collection-mysqlecollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-mysqlservercollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-umscollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_containment_vertical.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_analyzer.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_albums.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_currenttrack.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_info.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_labels.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_lyrics.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_photos.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_wikipedia.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_current.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_info.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_labels.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_lyrics.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_photos.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_wikipedia.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_ampache.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_jamendo.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_magnatunestore.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_mp3tunes.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_opmldirectory.so
%attr(755,root,root) %{_libdir}/kde4/amarok_service_amazonstore.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_ampache.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_magnatunestore.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_mp3tunes.so
%attr(755,root,root) %{_libdir}/kde4/kcm_amarok_service_amazonstore.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-playdarcollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_collection-upnpcollection.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_tabs.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_tabs.so
%dir %{_datadir}/apps/amarok
%dir %{_datadir}/apps/amarok/scripts
%{_datadir}/apps/amarok/data
%{_datadir}/apps/amarok/icons
%{_datadir}/apps/amarok/images
%{_datadir}/apps/amarok/amarok.notifyrc
%{_datadir}/apps/desktoptheme
%{_datadir}/apps/solid/actions/amarok-play-audiocd.desktop
%{_datadir}/config.kcfg/amarokconfig.kcfg
%{_datadir}/config/amarok.knsrc
%{_datadir}/config/amarokapplets.knsrc
%{_datadir}/dbus-1/interfaces/org.freedesktop.MediaPlayer.player.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.MediaPlayer.root.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.MediaPlayer.tracklist.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.Collection.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.App.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.Mpris1Extensions.Player.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.Mpris2Extensions.Player.xml
%{_desktopdir}/kde4/amarok_containers.desktop
%{_desktopdir}/kde4/amzdownloader.desktop
%{_datadir}/kde4/services/amarok.protocol
%{_datadir}/kde4/services/amarokitpc.protocol
%{_datadir}/kde4/services/ServiceMenus/amarok_append.desktop
%{_datadir}/kde4/services/amarok_collection-audiocdcollection.desktop
%{_datadir}/kde4/services/amarok_collection-daapcollection.desktop
%{_datadir}/kde4/services/amarok_collection-ipodcollection.desktop
%{_datadir}/kde4/services/amarok_collection-mtpcollection.desktop
#%%{_datadir}/kde4/services/amarok_collection-mysqlecollection.desktop
%{_datadir}/kde4/services/amarok_collection-mysqlservercollection.desktop
%{_datadir}/kde4/services/amarok_collection-umscollection.desktop
%{_datadir}/kde4/services/amarok-containment-vertical.desktop
%{_datadir}/kde4/services/amarok-context-applet-analyzer.desktop
%{_datadir}/kde4/services/amarok-context-applet-albums.desktop
%{_datadir}/kde4/services/amarok-context-applet-currenttrack.desktop
%{_datadir}/kde4/services/amarok-context-applet-info.desktop
%{_datadir}/kde4/services/amarok-context-applet-labels.desktop
%{_datadir}/kde4/services/amarok-context-applet-lyrics.desktop
%{_datadir}/kde4/services/amarok-context-applet-photos.desktop
%{_datadir}/kde4/services/amarok-context-applet-wikipedia.desktop
%{_datadir}/kde4/services/amarok-data-engine-current.desktop
%{_datadir}/kde4/services/amarok-data-engine-info.desktop
%{_datadir}/kde4/services/amarok-data-engine-labels.desktop
%{_datadir}/kde4/services/amarok-data-engine-lyrics.desktop
%{_datadir}/kde4/services/amarok-data-engine-photos.desktop
%{_datadir}/kde4/services/amarok-data-engine-wikipedia.desktop
%{_datadir}/kde4/services/amarok_service_amazonstore.desktop
%{_datadir}/kde4/services/amarok_service_amazonstore_config.desktop
%{_datadir}/kde4/services/amarok_service_ampache.desktop
%{_datadir}/kde4/services/amarok_service_ampache_config.desktop
%{_datadir}/kde4/services/amarok_service_jamendo.desktop
%{_datadir}/kde4/services/amarok_service_magnatunestore.desktop
%{_datadir}/kde4/services/amarok_service_magnatunestore_config.desktop
%{_datadir}/kde4/services/amarok_service_mp3tunes.desktop
%{_datadir}/kde4/services/amarok_service_mp3tunes_config.desktop
%{_datadir}/kde4/services/amarok_service_opmldirectory.desktop
%{_datadir}/kde4/services/amarok-context-applet-tabs.desktop
%{_datadir}/kde4/services/amarok-data-engine-tabs.desktop
%{_datadir}/kde4/services/amarok_collection-playdarcollection.desktop
%{_datadir}/kde4/services/amarok_collection-upnpcollection.desktop
%{_datadir}/kde4/servicetypes/amarok_codecinstall.desktop
%{_datadir}/kde4/servicetypes/amarok_context_applet.desktop
%{_datadir}/kde4/servicetypes/amarok_data_engine.desktop
%{_datadir}/kde4/servicetypes/amarok_plugin.desktop
%{_desktopdir}/kde4/amarok.desktop
%{_iconsdir}/*/*/apps/amarok.*
%{_datadir}/config/amarok_homerc
%attr(755,root,root) %{_datadir}/apps/kconf_update/*.pl
%{_datadir}/apps/kconf_update/amarok.upd
%{_datadir}/mime/packages/amzdownloader.xml

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
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxScalableEmblem.svgz
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxService.html
%{_datadir}/apps/amarok/scripts/librivox_service/script.spec
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxEmblem.png
%{_datadir}/apps/amarok/scripts/librivox_service/LibrivoxIcon.png
%{_datadir}/apps/amarok/scripts/librivox_service/audio_book128.png
%dir %{_datadir}/apps/amarok/scripts/free_music_charts_service
%{_datadir}/apps/amarok/scripts/free_music_charts_service/FMCEmblem.png
%{_datadir}/apps/amarok/scripts/free_music_charts_service/FMCIcon.png
%{_datadir}/apps/amarok/scripts/free_music_charts_service/FMCShow.png
%{_datadir}/apps/amarok/scripts/free_music_charts_service/main.js
%{_datadir}/apps/amarok/scripts/free_music_charts_service/script.spec
