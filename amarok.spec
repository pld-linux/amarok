# TODO:
#	* postgresql support alongside mysql
#	* NMM audio backend support (fix build - propably some BRs)
#	* make descriptions less useless
#	* HelixPlayer engine (fix build - propably some BRs)
#	* track http://websvn.kde.org/trunk/extragear/multimedia/amarok/TODO?rev=470324&r1=470292&r2=470324
#
# Conditional builds:
%bcond_without	arts		# disable arts engine
%bcond_without	gstreamer	# disable gstreamer
%bcond_without	mas		# disable MAS audio backend
%bcond_without	xine		# disable xine engine
%bcond_without	xmms 		# disable xmms wrapping
%bcond_without	zeroconf	# disable support for zeroconf
%bcond_with	included_sqlite # use included sqlite, not the distro's
%bcond_with	helix		# enable HelixPlayer engine
%bcond_with	nmm             # enable NMM audio backend
%bcond_with	mysql		# enable mysql support
%bcond_with	akode		# enable aKode engine (too buggy/incomplete)
%bcond_with	altlyrics	# use alternative lyrics provider
Summary:	A KDE audio player
Summary(pl):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	1.3.3
Release:	2
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/amarok/%{name}-%{version}.tar.bz2
# Source0-md5:	13f02c3cce06d9c1d0511171d736efa3
Patch0:		kde-common-gcc4.patch
Patch1:		%{name}-lyricsurl.patch
URL:		http://amarok.kde.org/
#BuildRequires:	kdebindings-kjsembed-devel
#BuildRequires:	unsermake >= 040511
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	arts-qt-devel
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_gstreamer:BuildRequires:	gstreamer-plugins-devel >= 0.8.1}
BuildRequires:	kdebase-devel
%{?with_akode:BuildRequires:	kdemultimedia-akode}
BuildRequires:	kdemultimedia-devel >= 9:3.1.93
BuildRequires:	libltdl-devel
BuildRequires:	libmusicbrainz-devel
BuildRequires:	libvisual-devel >= 0.2.0
%{?with_mysql:BuildRequires:		mysql-devel}
BuildRequires:	pcre-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRequires:	sed >= 4.0
%{?!with_included_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	taglib-devel >= 1.4
%{?with_xine:BuildRequires:		xine-lib-devel >= 2:1.0-0.rc5.0}
%{?with_xmms:BuildRequires:		xmms-devel}
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

%package akode
Summary:	Plugin akode
Summary(pl):	Wtyczka akode
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-plugin = %{version}-%{release}

%description akode
Plugin akode.

%description akode -l pl
Wtyczka akode.

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
Requires:	%{name} = %{version}-%{release}
Requires:	gstreamer-audio-effects
Requires:	gstreamer-audiosink
Requires:	gstreamer-mad
Requires:	gstreamer-musicbrainz
Requires:	gstreamer-vorbis
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

%package zeroconf
Summary:	Zeroconf data
Summary(pl):	Dane dla zeroconf
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	kdenetwork-kdnssd
Provides:	%{name}-plugin = %{version}-%{release}

%description zeroconf
Zeroconf data.

%description zeroconf -l pl
Dane dla zeroconf.

%package scripts
Summary:	amaroK scripts
Summary(pl):	Skrypty amaroKa
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	kdebase-kdialog
Requires:	python-PyQt

%description scripts
amaroK scripts allow you extend amaroK functionality.

You can learn more about scripts in amaroK from here:
<http://amarok.kde.org/wiki/index.php/Scripts>.

%description scripts -l pl
Skrypty amaroKa pozwalaj±ce rozszerzaæ jego funkcjonalno¶æ.

Wiêcej o skryptach w amaroKu mo¿na dowiedzieæ siê st±d:
<http://amarok.kde.org/wiki/index.php/Scripts>.

%prep
%setup -q
%patch0 -p1
%{?with_altlyrics:%patch1 -p1}
%{__sed} -i -e 's/Categories=.*/Categories=Qt;KDE;AudioVideo;Player;/' \
	amarok/src/amarok.desktop \

# see kde bug #110909
sed -i -e 's/amarok_live//' amarok/src/scripts/Makefile.am

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

cp -f /usr/share/automake/config.sub admin

#export UNSERMAKE=/usr/share/unsermake/unsermake

%{__make} -f admin/Makefile.common cvs

%configure \
	--disable-rpath \
	%{!?with_arts:--without-arts} \
	%{?with_mas:--with-mas} \
	%{!?with_xine:--without-xine} \
	%{!?with_gstreamer:--without-gstreamer} \
	%{!?with_akode:--without-akode} \
	%{?with_helix:--with-helix} \
	%{?with_nmm:--with-nmm} \
	%{?with_mysql:--with-mysql} \
	--disable-final \
	--with-qt-libraries=%{_libdir} \
	--with%{?!with_included_sqlite:out}-included-sqlite

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
if [ "$1" = 1 ]; then
	echo "Remember to install libvisual-plugins-* packages if you"
	echo "want to have a visualizations in amaroK."
fi

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
%dir %{_datadir}/apps/amarok
%dir %{_datadir}/apps/amarok/scripts
%{_datadir}/apps/amarok/*.rc
%{_datadir}/apps/amarok/data
%{_datadir}/apps/amarok/icons
%{_datadir}/apps/amarok/images
%{_datadir}/apps/amarok/themes
%{_datadir}/apps/konqueror/servicemenus/amarok_append.desktop
%{_datadir}/apps/konqsidebartng/add/amarok.desktop
%{_datadir}/apps/konqsidebartng/entries/amarok.desktop
%{_datadir}/apps/konqsidebartng/kicker_entries/amarok.desktop
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

%if %{with akode}
%files akode
%defattr(644,root,root,755)
%{_libdir}/kde3/libamarok_aKode-engine.la
%attr(755,root,root) %{_libdir}/kde3/libamarok_aKode-engine.so
%{_datadir}/services/amarok_aKode-engine.desktop
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
%{_datadir}/config.kcfg/xinecfg.kcfg
%{_datadir}/services/amarok_xine-engine.desktop
#%{_datadir}/services/amarok_xineengine_plugin.desktop
%endif

%if %{with zeroconf}
%files zeroconf
%defattr(644,root,root,755)
%{_datadir}/apps/zeroconf/_shoutcast._tcp
%endif

%files scripts
%defattr(644,root,root,755)

%dir %{_datadir}/apps/amarok/scripts/alarm
%{_datadir}/apps/amarok/scripts/alarm/README
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/alarm/alarm.py

%dir %{_datadir}/apps/amarok/scripts/graphequalizer
%{_datadir}/apps/amarok/scripts/graphequalizer/README
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/graphequalizer/graphequalizer

%dir %{_datadir}/apps/amarok/scripts/playlist2html
%{_datadir}/apps/amarok/scripts/playlist2html/README
%{_datadir}/apps/amarok/scripts/playlist2html/Playlist.py
%{_datadir}/apps/amarok/scripts/playlist2html/PlaylistServer.py
%{_datadir}/apps/amarok/scripts/playlist2html/playlist2html.py

%dir %{_datadir}/apps/amarok/scripts/templates
%{_datadir}/apps/amarok/scripts/templates/amarok.rb
%{_datadir}/apps/amarok/scripts/templates/python_qt_template.py
%{_datadir}/apps/amarok/scripts/templates/ruby_qt_template.rb

%dir %{_datadir}/apps/amarok/scripts/webcontrol
%{_datadir}/apps/amarok/scripts/webcontrol/README
%{_datadir}/apps/amarok/scripts/webcontrol/Globals.py
%{_datadir}/apps/amarok/scripts/webcontrol/Playlist.py
%{_datadir}/apps/amarok/scripts/webcontrol/RequestHandler.py
%{_datadir}/apps/amarok/scripts/webcontrol/amarok_cut.png
%{_datadir}/apps/amarok/scripts/webcontrol/controlbackground.png
%{_datadir}/apps/amarok/scripts/webcontrol/main.css
%{_datadir}/apps/amarok/scripts/webcontrol/main.js
%{_datadir}/apps/amarok/scripts/webcontrol/player_end.png
%{_datadir}/apps/amarok/scripts/webcontrol/player_pause.png
%{_datadir}/apps/amarok/scripts/webcontrol/player_play.png
%{_datadir}/apps/amarok/scripts/webcontrol/player_start.png
%{_datadir}/apps/amarok/scripts/webcontrol/player_stop.png
%{_datadir}/apps/amarok/scripts/webcontrol/template.thtml
%{_datadir}/apps/amarok/scripts/webcontrol/vol_speaker.png
%{_datadir}/apps/amarok/scripts/webcontrol/WebPublisher.py
%attr(755,root,root)  %{_datadir}/apps/amarok/scripts/webcontrol/WebControl.py

%dir %{_datadir}/apps/amarok/scripts/common
%{_datadir}/apps/amarok/scripts/common/Publisher.py
%{_datadir}/apps/amarok/scripts/common/Zeroconf.py

%dir %{_datadir}/apps/amarok/scripts/shouter
%{_datadir}/apps/amarok/scripts/shouter/README
%{_datadir}/apps/amarok/scripts/shouter/ChangeLog
%{_datadir}/apps/amarok/scripts/shouter/Amarok.py
%{_datadir}/apps/amarok/scripts/shouter/Globals.py
%{_datadir}/apps/amarok/scripts/shouter/Playlist.py
%{_datadir}/apps/amarok/scripts/shouter/Services.py
%{_datadir}/apps/amarok/scripts/shouter/ShouterConfig.py
%{_datadir}/apps/amarok/scripts/shouter/ShouterExceptions.py
%{_datadir}/apps/amarok/scripts/shouter/SocketErrors.py
%{_datadir}/apps/amarok/scripts/shouter/StreamConfig.py
%{_datadir}/apps/amarok/scripts/shouter/StreamController.py
%{_datadir}/apps/amarok/scripts/shouter/StreamPublisher.py
%{_datadir}/apps/amarok/scripts/shouter/binfuncs.py
%{_datadir}/apps/amarok/scripts/shouter/debug.py
%{_datadir}/apps/amarok/scripts/shouter/propfind-req.xml
%dir %{_datadir}/apps/amarok/scripts/shouter/silence
%{_datadir}/apps/amarok/scripts/shouter/silence/silence-48.mp3
%dir %{_datadir}/apps/amarok/scripts/shouter/test
%{_datadir}/apps/amarok/scripts/shouter/test/client.py
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/shouter/Shouter.py

%if 0
%dir %{_datadir}/apps/amarok/scripts/amarok_live
%{_datadir}/apps/amarok/scripts/amarok_live/README
%{_datadir}/apps/amarok/scripts/amarok_live/amarok.live.remaster.part1.sh
%{_datadir}/apps/amarok/scripts/amarok_live/amarok.live.remaster.part2.sh
%attr(755,root,root)  %{_datadir}/apps/amarok/scripts/amarok_live/amarok_live.py
%endif
