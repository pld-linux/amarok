
Summary:	A KDE audio player
Summary(pl):	Odtwarzacz audio dla KDE
Name:		amarok
Version:	0.8.3
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://dl.sourceforge.net/amarok/%{name}-%{version}.tar.bz2
# Source0-md5:	bdd9532e983ca85711e93929c008a5ba
URL:		http://amarok.sf.net/
BuildRequires:	kdemultimedia-devel >= 9:3.1.93
BuildRequires:	rpmbuild(macros) >= 1.129	
BuildRequires:	sed >= 4.0
BuildRequires:	taglib-devel >= 0.95	
Requires:	kdebase-core >= 9:3.1.93
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A KDE audio player.

%description -l pl
Odtwarzacz audio dla KDE.

%prep
%setup -q

%build
%configure \
	--disable-rpath \
	--enable-final

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_appsdir=%{_applnkdir} \
	kde_htmldir=%{_kdedocdir}
install -d $RPM_BUILD_ROOT%{_desktopdir}/kde

mv $RPM_BUILD_ROOT{%{_applnkdir}/Multimedia/amarok.desktop,%{_desktopdir}/kde}	

# Grrr...
sed -i 's/Categories=Audio/Categories=AudioVideo/' \
	$RPM_BUILD_ROOT%{_desktopdir}/kde/amarok.desktop

%find_lang %{name} --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
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
