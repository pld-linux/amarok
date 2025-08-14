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
%define		qtver	6.7.0
%define		kdever	4.5.5

Summary:	A KDE audio player
Summary(pl.UTF-8):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	3.3.1
Release:	3
License:	GPL v2+ and LGPL v2.1+
Group:		X11/Applications/Multimedia
Source0:	https://download.kde.org/%{state}/amarok/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	4df9c10823a96b58631c4ff9b15d12ed
URL:		http://amarok.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Qt5Compat-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
%ifarch %{x8664}
BuildRequires:	Qt6WebEngine-devel >= %{qtver}
%endif
BuildRequires:	fftw3-devel
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 6.0.0
BuildRequires:	kf6-karchive-devel >= 6.0.0
BuildRequires:	kf6-kcmutils-devel >= 6.0.0
BuildRequires:	kf6-kcolorscheme-devel >= 6.16.0
BuildRequires:	kf6-kcoreaddons-devel >= 6.16.0
BuildRequires:	kf6-kcrash-devel >= 6.0.0
BuildRequires:	kf6-kdbusaddons-devel >= 6.0.0
BuildRequires:	kf6-kdnssd-devel >= 6.0.0
BuildRequires:	kf6-kdoctools-devel >= 6.0.0
BuildRequires:	kf6-kglobalaccel-devel >= 6.0.0
BuildRequires:	kf6-kguiaddons-devel >= 6.16.0
BuildRequires:	kf6-ki18n-devel >= 6.16.0
BuildRequires:	kf6-kiconthemes-devel >= 6.0.0
BuildRequires:	kf6-kio-devel >= 6.16.0
BuildRequires:	kf6-knotifications-devel >= 6.0.0
BuildRequires:	kf6-kpackage-devel >= 6.0.0
BuildRequires:	kf6-kstatusnotifieritem-devel >= 6.0.0
BuildRequires:	kf6-ktexteditor-devel >= 6.0.0
BuildRequires:	kf6-ktextwidgets-devel >= 6.0.0
BuildRequires:	kf6-kwindowsystem-devel >= 6.0.0
BuildRequires:	kf6-solid-devel >= 6.0.0
BuildRequires:	kf6-threadweaver-devel >= 6.0.0
BuildRequires:	libmtp-devel >= 1.0.0
#BuildRequires:	mysql8.4-devel
# switching back to mysql 8.0 as it's available on 32bit architectures
BuildRequires:	mysql8.0-devel
BuildRequires:	pkgconfig
BuildRequires:	taglib-devel
Requires(post,postun):	/sbin/ldconfig
Obsoletes:	amarok-arts < 3.3.0
Obsoletes:	amarok-xmms < 3.3.0
# It should require mysql-embeded
Requires:	%{name}-data = %{version}-%{release}
#Requires:	mysql8.0 >= 5.1.31-3
#Conflicts:	mysql < 5.1.31-3
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl.UTF-8
Odtwarzacz audio dla KDE.

%package data
Summary:	Data files for amarok
Summary(pl.UTF-8):	Dane dla amarok
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	amarok-scripts < 3.3.0

%description data
Data files for amarok.

%description data -l pl.UTF-8
Dane dla amarok.


%prep
%setup -q

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DWITH_EMBEDDED_DB=OFF

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{sr,zh_CN}

# not supported by glibc yet
%{__rm} -rf $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name} --all-name --with-kde --with-qm

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
/etc/xdg/amarok_homerc
%attr(755,root,root) %{_bindir}/amarok
%attr(755,root,root) %{_bindir}/amarok_afttagger
%attr(755,root,root) %{_bindir}/amarokcollectionscanner
%{_libdir}/libamarok-sqlcollection.so
%ghost %{_libdir}/libamarok-sqlcollection.so.1
%attr(755,root,root) %{_libdir}/libamarok-sqlcollection.so.*.*
%{_libdir}/libamarok-transcoding.so
%ghost %{_libdir}/libamarok-transcoding.so.1
%attr(755,root,root) %{_libdir}/libamarok-transcoding.so.*.*
%{_libdir}/libamarokcore.so
%ghost %{_libdir}/libamarokcore.so.1
%attr(755,root,root) %{_libdir}/libamarokcore.so.*.*
%{_libdir}/libamaroklib.so
%ghost %{_libdir}/libamaroklib.so.1
%attr(755,root,root) %{_libdir}/libamaroklib.so.*.*
%{_libdir}/libamarokpud.so
%{_libdir}/libamarokshared.so
%ghost %{_libdir}/libamarokshared.so.1
%attr(755,root,root) %{_libdir}/libamarokshared.so.*.*
%attr(755,root,root) %{_libdir}/libampache_account_login.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_collection-audiocdcollection.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_collection-daapcollection.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_collection-mtpcollection.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_collection-mysqlcollection.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_collection-playdarcollection.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_collection-umscollection.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_importer-amarok.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_importer-banshee.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_importer-clementine.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_importer-fastforward.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_importer-itunes.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_importer-rhythmbox.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_service_ampache.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_service_magnatunestore.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_service_opmldirectory.so
%attr(755,root,root) %{_libdir}/qt6/plugins/amarok_storage-mysqlserverstorage.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kcm_amarok_service_ampache.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kcm_amarok_service_magnatunestore.so
%dir %{_libdir}/qt6/qml/org/kde/amarok
%dir %{_libdir}/qt6/qml/org/kde/amarok/albums
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/amarok/albums/libamarok_context_applet_albums.so
%{_libdir}/qt6/qml/org/kde/amarok/albums/qmldir
%dir %{_libdir}/qt6/qml/org/kde/amarok/analyzer
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/amarok/analyzer/libamarok_context_applet_analyzer.so
%{_libdir}/qt6/qml/org/kde/amarok/analyzer/qmldir
%dir %{_libdir}/qt6/qml/org/kde/amarok/currenttrack
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/amarok/currenttrack/libamarok_context_applet_currenttrack.so
%{_libdir}/qt6/qml/org/kde/amarok/currenttrack/qmldir
%dir %{_libdir}/qt6/qml/org/kde/amarok/lyrics
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/amarok/lyrics/libamarok_context_applet_lyrics.so
%{_libdir}/qt6/qml/org/kde/amarok/lyrics/qmldir
%dir %{_libdir}/qt6/qml/org/kde/amarok/photos
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/amarok/photos/libamarok_context_applet_photos.so
%{_libdir}/qt6/qml/org/kde/amarok/photos/qmldir
%dir %{_libdir}/qt6/qml/org/kde/amarok/qml
%{_libdir}/qt6/qml/org/kde/amarok/qml/Applet.qml
%{_libdir}/qt6/qml/org/kde/amarok/qml/AppletHeader.qml
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/amarok/qml/libqml_plugin.so
%{_libdir}/qt6/qml/org/kde/amarok/qml/qmldir

%ifarch %{x8664}
%dir %{_libdir}/qt6/qml/org/kde/amarok/wikipedia
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/amarok/wikipedia/libamarok_context_applet_wikipedia.so
%{_libdir}/qt6/qml/org/kde/amarok/wikipedia/qmldir
%endif

%files data
%defattr(644,root,root,755)
%{_datadir}/amarok
%{_desktopdir}/org.kde.amarok.desktop
%{_desktopdir}/org.kde.amarok_containers.desktop
%{_datadir}/config.kcfg/amarokconfig.kcfg
%{_datadir}/dbus-1/interfaces/org.kde.amarok.App.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.Collection.xml
%{_datadir}/dbus-1/interfaces/org.kde.amarok.Mpris2Extensions.Player.xml
%{_datadir}/dbus-1/services/org.kde.amarok.service
%{_iconsdir}/hicolor/*x*/apps/amarok.png
%{_datadir}/kio/servicemenus/amarok_append.desktop
%{_datadir}/knotifications6/amarok.notifyrc
%{_datadir}/kpackage/amarok
%dir %{_datadir}/kpackage/genericqml/org.kde.amarok.context
%dir %{_datadir}/kpackage/genericqml/org.kde.amarok.context/contents
%dir %{_datadir}/kpackage/genericqml/org.kde.amarok.context/contents/ui
%dir %{_datadir}/kpackage/genericqml/org.kde.amarok.context/contents/ui/toolbar
%{_datadir}/kpackage/genericqml/org.kde.amarok.context/contents/ui/main.qml
%{_datadir}/kpackage/genericqml/org.kde.amarok.context/contents/ui/toolbar/AppletToolbar.qml
%{_datadir}/kpackage/genericqml/org.kde.amarok.context/contents/ui/toolbar/AppletToolbarAddItem.qml
%{_datadir}/kpackage/genericqml/org.kde.amarok.context/contents/ui/toolbar/AppletToolbarAppletItem.qml
%{_datadir}/kpackage/genericqml/org.kde.amarok.context/metadata.json
%{_datadir}/metainfo/org.kde.amarok.albums.appdata.xml
%{_datadir}/metainfo/org.kde.amarok.analyzer.appdata.xml
%{_datadir}/metainfo/org.kde.amarok.appdata.xml
%{_datadir}/metainfo/org.kde.amarok.context.appdata.xml
%{_datadir}/metainfo/org.kde.amarok.currenttrack.appdata.xml
%{_datadir}/metainfo/org.kde.amarok.lyrics.appdata.xml
%{_datadir}/metainfo/org.kde.amarok.photos.appdata.xml
%{_datadir}/solid/actions/amarok-play-audiocd.desktop

%ifarch %{x8664}
%{_datadir}/metainfo/org.kde.amarok.wikipedia.appdata.xml
%endif
