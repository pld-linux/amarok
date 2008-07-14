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
Version:	1.4.9.1
Release:	12
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.kde.org/pub/kde/stable/amarok/%{version}/src/%{name}-%{version}.tar.bz2
# Source0-md5:	aa588778379a391ad3f4b3fc770217e4
Patch0:		%{name}-helixplayer-morearchs.patch
Patch1:		%{name}-libnjb.patch
Patch2:		%{name}-smp.patch
Patch3:		%{name}-sparc.patch
Patch4:		kde-ac260-lt.patch
Patch5:		kde-common-PLD.patch
Patch6:		%{name}-gcc4.patch
Patch7:		%{name}-titleorder.patch
Patch8:		%{name}-mongrel.patch
URL:		http://amarok.kde.org/
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
%{?with_gstreamer:BuildRequires:	gstreamer-devel >= 0.10.0}
BuildRequires:	kdebase-devel
%{?with_akode:BuildRequires:	kdemultimedia-akode}
BuildRequires:	kdemultimedia-devel >= 9:3.1.93
%{?with_mp3players:BuildRequires:	libgpod-devel >= 0.6.0}
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
BuildRequires:	sed >= 4.0
%{!?with_included_sqlite:BuildRequires:	sqlite3-devel >= 3.3}
BuildRequires:	taglib-devel >= 1.4
%{?with_xine:BuildRequires:	xine-lib-devel >= 1.1.1}
Requires(post):	/sbin/ldconfig
Requires:	%{name}-plugin = %{version}-%{release}
Requires:	kdebase-core >= 9:3.1.93
Requires:	kdelibs-libs >= 9:3.5.9
Requires:	ruby-mongrel
Suggests:	kdemultimedia(audiocd) >= 9:3.1.93
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
Suggests:	python-PyKDE
Obsoletes:	amarok-arts
Obsoletes:	amarok-xmms
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# temporary hack for proper libgpod::itdb_get_mountpoint() detection.
%define		filterout_ld	-Wl,--as-needed

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
Requires:	kdenetwork-kdnssd
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
Requires:	kdebase-kdialog
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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%{__sed} -i -e 's/Categories=.*/Categories=Qt;KDE;AudioVideo;Player;/' \
	amarok/src/amarok.desktop \

# see kde bug #110909
%{__sed} -i -e 's/amarok_live//' amarok/src/scripts/Makefile.am

# kill env, call interpreter directly, so rpm automatics could rule
%{__sed} -i -e '
	1s,#!.*bin/env.*ruby,#!%{_bindir}/ruby,
	1s,#!.*bin/env.*python,#!%{__python},
' amarok/src/scripts/*/*.{py,rb} amarok/src/amarok_proxy.rb

%build
cp -f /usr/share/automake/config.sub admin
%{__make} -f admin/Makefile.common cvs

# hack: passing something other than "no" or "yes" to --with-helix allows
# us to pass HELIX_LIBS
%configure \
	HELIX_LIBS=%{_libdir}/helixplayer \
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--disable-rpath \
	--with%{!?with_mas:out}-mas \
	--with%{!?with_xine:out}-xine \
	--with%{!?with_gstreamer:out}-gstreamer10 \
	--with%{!?with_akode:out}-akode \
	--with%{!?with_helix:out}-helix%{?with_helix:=usegivenpath} \
	--with%{!?with_nmm:out}-nmm \
	--with%{!?with_mp3players:out}-libgpod \
	--with%{!?with_mp3players:out}-libnjb \
	--with%{!?with_mp3players:out}-libmtp \
	--with%{!?with_mp3players:out}-ifp \
	--%{?with_mysql:en}%{!?with_mysql:dis}able-mysql \
	--%{?with_mysql:en}%{!?with_mysql:dis}able-postgresql \
	--disable-final \
	--with-mp4v2 \
	--with-qt-libraries=%{_libdir} \
	--with%{!?with_included_sqlite:out}-included-sqlite

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	ruby_rubylibdir=%{ruby_rubylibdir} \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir}

# remove bogus dir
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/xx

rm $RPM_BUILD_ROOT%{_libdir}/kde3/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libamarok.{so,la}

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
%find_lang amarok --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files -f amarok.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/amarok
%attr(755,root,root) %{_bindir}/amarokapp
%attr(755,root,root) %{_bindir}/amarokcollectionscanner
%attr(755,root,root) %{_bindir}/amarok_libvisual
# used by last.fm and daap
%attr(755,root,root) %{_bindir}/amarok_proxy.rb
# used by daap
%attr(755,root,root) %{_bindir}/amarok_daapserver.rb
%attr(755,root,root) %{_libdir}/libamarok.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libamarok.so.0
%attr(755,root,root) %{_libdir}/kde3/konqsidebar_universalamarok.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_generic-mediadevice.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_void-engine_plugin.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_daap-mediadevice.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_massstorage-device.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_nfs-device.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_smb-device.so
%dir %{_datadir}/apps/amarok
%dir %{_datadir}/apps/amarok/scripts
%{_datadir}/apps/amarok/*.rc
%{_datadir}/apps/amarok/data
%{_datadir}/apps/amarok/icons
%{_datadir}/apps/amarok/images
%{_datadir}/apps/amarok/themes
%{_datadir}/apps/konqueror/servicemenus/amarok_append.desktop
%{_datadir}/apps/konqueror/servicemenus/amarok_addaspodcast.desktop
%{_datadir}/apps/konqueror/servicemenus/amarok_play_audiocd.desktop
%{_datadir}/apps/konqsidebartng/add/amarok.desktop
%{_datadir}/apps/konqsidebartng/entries/amarok.desktop
%{_datadir}/apps/konqsidebartng/kicker_entries/amarok.desktop
%{_datadir}/apps/profiles/amarok.profile.xml
%{_datadir}/config/amarokrc
%{_datadir}/config.kcfg/amarok.kcfg
%{_datadir}/services/amarok_generic-mediadevice.desktop
%{_datadir}/services/amarok_void-engine_plugin.desktop
%{_datadir}/services/amarok_daap-mediadevice.desktop
%{_datadir}/services/amarok_massstorage-device.desktop
%{_datadir}/services/amarok_nfs-device.desktop
%{_datadir}/services/amarok_smb-device.desktop
%{_datadir}/services/amaroklastfm.protocol
%{_datadir}/services/amarokitpc.protocol
%{_datadir}/services/amarokpcast.protocol
%{_datadir}/servicetypes/amarok_codecinstall.desktop
%{_datadir}/servicetypes/amarok_plugin.desktop
%{_desktopdir}/kde/amarok.desktop
%{_iconsdir}/*/*/apps/amarok.*

# TODO: move to subpackage
%dir %{ruby_rubylibdir}/amarok
# used by daap
%{ruby_rubylibdir}/amarok/codes.rb
# used by daap and lyrics_lyrc
%{ruby_rubylibdir}/amarok/debug.rb

# TODO: move to subpackage
%if %{with mp3players}
%attr(755,root,root) %{_libdir}/kde3/libamarok_ifp-mediadevice.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_ipod-mediadevice.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_mtp-mediadevice.so
%attr(755,root,root) %{_libdir}/kde3/libamarok_njb-mediadevice.so
%{_datadir}/services/amarok_ifp-mediadevice.desktop
%{_datadir}/services/amarok_ipod-mediadevice.desktop
%{_datadir}/services/amarok_mtp-mediadevice.desktop
%{_datadir}/services/amarok_njb-mediadevice.desktop
%endif

%if %{with akode}
%files akode
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde3/libamarok_aKode-engine.so
%{_datadir}/services/amarok_aKode-engine.desktop
%endif

%if %{with gstreamer}
%files gstreamer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde3/libamarok_gst10engine_plugin.so
%{_datadir}/config.kcfg/gstconfig.kcfg
%{_datadir}/services/amarok_gst10engine_plugin.desktop
%endif

%if %{with helix}
%files helix
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde3/libamarok_helixengine_plugin.so
%{_datadir}/config.kcfg/helixconfig.kcfg
%{_datadir}/services/amarok_helixengine_plugin.desktop
%endif

%if %{with xine}
%files xine
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/kde3/libamarok_xine-engine.so
%{_datadir}/config.kcfg/xinecfg.kcfg
%{_datadir}/services/amarok_xine-engine.desktop
%endif

%if 0
%if %{with zeroconf}
%files zeroconf
%defattr(644,root,root,755)
#%{_datadir}/apps/zeroconf/_shoutcast._tcp
%endif
%endif

%files scripts
%defattr(644,root,root,755)
%dir %{_datadir}/apps/amarok/scripts/common
%{_datadir}/apps/amarok/scripts/common/Publisher.py
%{_datadir}/apps/amarok/scripts/common/Zeroconf.py

%dir %{_datadir}/apps/amarok/scripts/templates
%{_datadir}/apps/amarok/scripts/templates/amarok.rb
%{_datadir}/apps/amarok/scripts/templates/python_qt_template.py
%{_datadir}/apps/amarok/scripts/templates/ruby_qt_template.rb

# amarok searches for executable programs for scripts
# to figure out which files need to have execute permission, use this
# find command:
# $ find $RPM_BUILD_ROOT/usr/share/apps/amarok/scripts -perm +1

#%dir %{_datadir}/apps/amarok/scripts/graphequalizer
#%{_datadir}/apps/amarok/scripts/graphequalizer/README
#%attr(755,root,root) %{_datadir}/apps/amarok/scripts/graphequalizer/graphequalizer

%dir %{_datadir}/apps/amarok/scripts/playlist2html
%{_datadir}/apps/amarok/scripts/playlist2html/README
%{_datadir}/apps/amarok/scripts/playlist2html/Playlist.py
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/playlist2html/PlaylistServer.py
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/playlist2html/playlist2html.py
%{_datadir}/apps/amarok/scripts/playlist2html/PlaylistServer.spec
%{_datadir}/apps/amarok/scripts/playlist2html/playlist2html.spec


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
%{_datadir}/apps/amarok/scripts/webcontrol/WebControl.spec
%{_datadir}/apps/amarok/scripts/webcontrol/smallstar.png
%{_datadir}/apps/amarok/scripts/webcontrol/star.png
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/webcontrol/WebControl.py

%dir %{_datadir}/apps/amarok/scripts/lyrics_astraweb
%{_datadir}/apps/amarok/scripts/lyrics_astraweb/COPYING
%{_datadir}/apps/amarok/scripts/lyrics_astraweb/README
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/lyrics_astraweb/lyrics_astraweb.rb
%{_datadir}/apps/amarok/scripts/lyrics_astraweb/lyrics_astraweb.spec

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

%if 0
%dir %{_datadir}/apps/amarok/scripts/amarok_live
%{_datadir}/apps/amarok/scripts/amarok_live/README
%{_datadir}/apps/amarok/scripts/amarok_live/amarok.live.remaster.part1.sh
%{_datadir}/apps/amarok/scripts/amarok_live/amarok.live.remaster.part2.sh
%attr(755,root,root) %{_datadir}/apps/amarok/scripts/amarok_live/amarok_live.py
%endif
