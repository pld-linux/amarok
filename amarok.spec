
%define		_snap	031107

Summary:	A KDE audio player
Summary(pl):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	0.6.91.%{_snap}
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
# From kdenonbeta kde cvs module
Source0:	http://www.kernel.pl/~adgor/kde/%{name}-%{_snap}.tar.bz2
# Source0-md5:	046ef6af15e25ad1e5fa7ccdca4af99e
URL:		http://www.xs4all.nl/~jjvrieze/kmplayer.html
BuildRequires:	kdemultimedia-devel >= 9:3.1.93	
BuildRequires:	taglib-devel >= 0.95	
Requires:	kdebase-core >= 9:3.1.93
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl
Odtwarzacz audio dla KDE.

%prep
%setup -q -n %{name}-%{_snap}

%build

%{__make} -f admin/Makefile.common cvs 

%configure \
	--disable-rpath \
	--enable-final

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_appsdir=%{_applnkdir}
	
install -d $RPM_BUILD_ROOT%{_desktopdir}/kde

mv $RPM_BUILD_ROOT{%{_applnkdir}/Multimedia/amarok.desktop,%{_desktopdir}/kde}	

echo "Categories=Qt;KDE;AudioVideo" \
	>> $RPM_BUILD_ROOT%{_desktopdir}/kde/amarok.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/amarok
%{_libdir}/libamarokarts.la
%attr(755,root,root) %{_libdir}/libamarokarts.so
%{_libdir}/mcop/Amarok
%{_libdir}/mcop/amarokarts.mcopclass
%{_libdir}/mcop/amarokarts.mcoptype
%{_datadir}/apps/amarok
%{_desktopdir}/kde/amarok.desktop
%{_iconsdir}/[!l]*/*/apps/amarok.png
