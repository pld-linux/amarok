# TODO:
# - postgresql support alongside mysql
# - NMM audio backend support (fix build - propably some BRs)
# - make descriptions less useless
# - track http://websvn.kde.org/trunk/extragear/multimedia/amarok/TODO?rev=470324&r1=470292&r2=470324
# - include /usr/bin/amarok_proxy.rb (proxy server for last.fm, but req. ruby)
# - main package pulls /usr/bin/ruby
# - monitor http://bugs.kde.org/show_bug.cgi?id=137390 to remove the temporary fix
# - ProjectM (see README)
# - karma & MFS (see README)
#
# Conditional builds:
%bcond_with	gstreamer	# enable gstreamer (gst10 not stable)
%bcond_without	mas		# disable MAS audio backend
%bcond_without	xine		# disable xine engine
%bcond_without	zeroconf	# disable support for zeroconf
%bcond_without	included_sqlite # don't use included sqlite (VERY BAD IDEA), needs sqlite >= 3.3 otherwise
%bcond_without	helix		# disable HelixPlayer engine
%bcond_without	mp3players	# disable iPod and iRiver MP3 players support
%bcond_with	nmm		# enable NMM audio backend
%bcond_with	mysql		# enable MySQL support
%bcond_with	pgsql		# enable PostgreSQL support
#
%ifarch i386
%undefine	with_helix
%endif

Summary:	A KDE audio player
Summary(pl.UTF-8):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	1.86
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.kde.org/pub/kde/unstable/amarok/%{version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	acf43672687a5f261ce36d668338a4c1
Patch0:		kde4-kdeextragear-multimedia-NJB.patch
URL:		http://amarok.kde.org/
BuildRequires:	QtScript-devel
BuildRequires:	QtUiTools-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
%{?with_gstreamer:BuildRequires:	gstreamer-devel >= 0.10.0}
BuildRequires:	kde4-kdebase-devel
BuildRequires:	kde4-kdemultimedia-devel
%{?with_mp3players:BuildRequires:	libgpod-devel >= 0.4.2}
%{?with_mp3players:BuildRequires:	libifp-devel >= 1.0.0.2}
BuildRequires:	libltdl-devel
%{?with_mp3players:BuildRequires:	libmtp-devel >= 0.1.1}
%{?with_mp3players:BuildRequires:	libnjb-devel >= 2.2.4}
%{?with_pgsql:BuildRequires:		libpqxx-devel}
BuildRequires:	libtunepimp-devel >= 0.5.1-6
BuildRequires:	libvisual-devel >= 0.4.0
BuildRequires:	mpeg4ip-devel >= 1:1.6
%{?with_mysql:BuildRequires:		mysql-devel}
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	ruby-devel >= 1.8
%{!?with_included_sqlite:BuildRequires:	sqlite3-devel >= 3.3}
BuildRequires:	strigi-devel >= 0.5.5
BuildRequires:	taglib-devel
%{?with_xine:BuildRequires:	xine-lib-devel >= 1.1.1}
Requires(post):	/sbin/ldconfig
Requires:	%{name}-plugin = %{version}-%{release}
Requires:	kde4-kdebase-core
Requires:	kde4-kdemultimedia-audiocd
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
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl.UTF-8
Odtwarzacz audio dla KDE.

%package akode
Summary:	Plugin akode
Summary(pl.UTF-8):	Wtyczka akode
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-plugin = %{version}-%{release}

%description akode
Plugin akode.

%description akode -l pl.UTF-8
Wtyczka akode.

%package helix
Summary:	Helix/Realplayer playback support for amarok
Summary(pl.UTF-8):	Wsparcie dla odtwarzania przez Helix/Realplayera dla amaroka
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	helix-core
Provides:	%{name}-plugin = %{version}-%{release}

%description helix
Helix/Realplayer playback support for amarok.

%description helix -l pl.UTF-8
Wsparcie dla odtwarzania przez Helix/Realplayera dla amaroka.

%package gstreamer
Summary:	Plugin gstreamer
Summary(pl.UTF-8):	Wtyczka gstreamer
Group:		X11/Applications/Multimedia
# deps, to get it working:
# mp3 decoder:	gstreamer-mad
# ogg decoder:	gstreamer-vorbis
# audio output driver:	gstreamer-audiosink-alsa
# from gstreamer-audio-effects to control volume, etc
# needed libs:
#  at least /usr/lib/gstreamer-0.8/libgstresample.so
#  probably /usr/lib/gstreamer-0.8/libgstadder.so
#  and probably /usr/lib/gstreamer-0.8/libgstvolume.so
# gstreamer-musicbrainz for being able to edit id3 tags on files.
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer-audio-effects
Requires:	gstreamer-audiosink
Requires:	gstreamer-mad
Requires:	gstreamer-musicbrainz
Requires:	gstreamer-vorbis
Provides:	%{name}-plugin = %{version}-%{release}

%description gstreamer
Plugin gstreamer.

%description gstreamer -l pl.UTF-8
Wtyczka gstreamer.

%package xine
Summary:	Plugin xine
Summary(pl.UTF-8):	Wtyczka xine
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	xine-plugin-audio
Provides:	%{name}-plugin = %{version}-%{release}

%description xine
Plugin xine.

%description xine -l pl.UTF-8
Wtyczka xine.

%package zeroconf
Summary:	Zeroconf data
Summary(pl.UTF-8):	Dane dla zeroconf
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	kde4-kdenetwork-kdnssd
Provides:	%{name}-plugin = %{version}-%{release}

%description zeroconf
Zeroconf data.

%description zeroconf -l pl.UTF-8
Dane dla zeroconf.

%package scripts
Summary:	amaroK scripts
Summary(pl.UTF-8):	Skrypty amaroKa
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	kde4-kdebase-kdialog
Requires:	python-PyQt
Requires:	ruby-modules

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
		-DCMAKE_INSTALL_PREFIX=%{_prefix} \
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/amarok
%attr(755,root,root) %{_bindir}/amarokcollectionscanner
%attr(755,root,root) %{_libdir}/libamaroklib.so
%attr(755,root,root) %{_libdir}/libamaroklib.so.*.*.*
%attr(755,root,root) %{_libdir}/libamarok_taglib.so
%attr(755,root,root) %{_libdir}/libamarok_taglib.so.1
%attr(755,root,root) %{_libdir}/libamarok_taglib.so.1.0.0
%attr(755,root,root) %{_libdir}/libamaroklib.so.1
%attr(755,root,root) %{_libdir}/libamarokplasma.so
%attr(755,root,root) %{_libdir}/libamarokplasma.so.1
%attr(755,root,root) %{_libdir}/libamarokplasma.so.1.0.0
%attr(755,root,root) %{_libdir}/strigi/strigita_audible.so
%attr(755,root,root) %{_libdir}/strigi/strigita_mp4.so
%attr(755,root,root) %{_libdir}/kde4/amarok_containment_context.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_currenttrack.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_lastfmevents.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_lyrics.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_serviceinfo.so
%attr(755,root,root) %{_libdir}/kde4/amarok_context_applet_wikipedia.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_current.so
%attr(755,root,root) %{_libdir}/kde4/amarok_data_engine_lastfm.so
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
%attr(755,root,root) %{_libdir}/kde4/libamarok_generic-mediadevice.so
%attr(755,root,root) %{_libdir}/kde4/libamarok_phonon-engine.so
%attr(755,root,root) %{_libdir}/kde4/libamarok_void-engine_plugin.so
%dir %{_datadir}/apps/amarok
%dir %{_datadir}/apps/amarok/scripts
%{_datadir}/apps/amarok/data
%{_datadir}/apps/amarok/icons
%{_datadir}/apps/amarok/images
%{_datadir}/apps/desktoptheme
%{_datadir}/apps/profiles/amarok.profile.xml
%{_datadir}/config/amarokrc
%{_datadir}/config.kcfg/amarok.kcfg
%{_datadir}/kde4/services/amarok_generic-mediadevice.desktop
%{_datadir}/kde4/services/amarok_void-engine_plugin.desktop
%{_datadir}/dbus-1/interfaces/org.kde.amarok.collection.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.context.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.mediabrowser.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.player.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.playlist.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.playlistbrowser.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.script.xml
%{_datadir}/kde4/services/ServiceMenus/amarok_append.desktop
%{_datadir}/kde4/services/amarok-containment-context.desktop
%{_datadir}/kde4/services/amarok-context-applet-currenttrack.desktop
%{_datadir}/kde4/services/amarok-context-applet-lastfmevents.desktop
%{_datadir}/kde4/services/amarok-context-applet-lyrics.desktop
%{_datadir}/kde4/services/amarok-context-applet-serviceinfo.desktop
%{_datadir}/kde4/services/amarok-context-applet-wikipedia.desktop
%{_datadir}/kde4/services/amarok-data-engine-current.desktop
%{_datadir}/kde4/services/amarok-data-engine-lastfm.desktop
%{_datadir}/kde4/services/amarok-data-engine-lyrics.desktop
%{_datadir}/kde4/services/amarok-data-engine-service.desktop
%{_datadir}/kde4/services/amarok-data-engine-wikipedia.desktop
%{_datadir}/kde4/services/amarok_collection-daapcollection.desktop
%{_datadir}/kde4/services/amarok_collection-sqlcollection.desktop
%{_datadir}/kde4/services/amarok_phonon-engine.desktop
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
%{_datadir}/kde4/servicetypes/amarok_context_applet.desktop
%{_datadir}/kde4/servicetypes/amarok_data_engine.desktop
%{_datadir}/kde4/servicetypes/amarok_plugin.desktop
%{_desktopdir}/kde4/amarok.desktop
%{_iconsdir}/*/*/apps/amarok.*

%if %{with xine}
%files xine
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde4/libamarok_xine-engine.so
%{_datadir}/config.kcfg/xinecfg.kcfg
%{_datadir}/kde4/services/amarok_xine-engine.desktop
%endif

%files scripts
%defattr(644,root,root,755)
%dir %{_datadir}/apps/amarok/scripts/lyrics_lyrc
%{_datadir}/apps/amarok/scripts/lyrics_lyrc/COPYING
%{_datadir}/apps/amarok/scripts/lyrics_lyrc/README
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/lyrics_lyrc/lyrics_lyrc.rb
%{_datadir}/apps/amarok/scripts/lyrics_lyrc/lyrics_lyrc.spec

%dir %{_datadir}/apps/amarok/scripts/score_default
%{_datadir}/apps/amarok/scripts/score_default/COPYING
%{_datadir}/apps/amarok/scripts/score_default/README
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/score_default/score_default.rb
%{_datadir}/apps/amarok/scripts/score_default/score_default.spec
%dir %{_datadir}/apps/amarok/scripts/score_impulsive
%{_datadir}/apps/amarok/scripts/score_impulsive/COPYING
%{_datadir}/apps/amarok/scripts/score_impulsive/README
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/score_impulsive/score_impulsive.rb
%{_datadir}/apps/amarok/scripts/score_impulsive/score_impulsive.spec

%dir %{_datadir}/apps/amarok/scripts/ruby_debug
%{_datadir}/apps/amarok/scripts/ruby_debug/debug.rb
