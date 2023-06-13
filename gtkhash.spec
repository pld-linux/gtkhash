#
# Conditional build:
%bcond_without	caja		# Caja extension (MATE)
%bcond_with	nautilus	# Nautilus extension (GNOME) [not ready for nautilus 4]
%bcond_without	nemo		# Nemo extension (Cinnamon)
%bcond_without	thunar		# Thunar extension (XFCE)

Summary:	Desktop utility to calculate checksums
Summary(pl.UTF-8):	Graficzne narzędzie do liczenia sum kontrolnych
Name:		gtkhash
Version:	1.5
Release:	1
License:	GPL v2+
Group:		X11/Applications
#Source0Download: https://github.com/gtkhash/gtkhash/releases
Source0:	https://github.com/gtkhash/gtkhash/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	4bab8c0da1f7e14888c813576bc57c08
URL:		https://gtkhash.org/
%{?with_thunar:BuildRequires:	Thunar-devel >= 1.7.0}
# gtk3 based
%{?with_caja:BuildRequires:	caja-devel >= 1.18.0}
%{?with_nemo:BuildRequires:	cinnamon-nemo-devel}
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	glib2-devel >= 1:2.48
BuildRequires:	gtk+3-devel >= 3.18
# crypto can be also libcrypto (openssl >= 1.1), linux-crypto (AF_ALG), mbedtls, nettle
BuildRequires:	libb2-devel
BuildRequires:	libgcrypt-devel >= 1.6.0
%{?with_nautilus:BuildRequires:	nautilus-devel >= 3}
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2-devel >= 1:2.48
Requires:	gtk+3-devel >= 3.18
Requires:	libgcrypt >= 1.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GtkHash is a desktop utility for computing message digests or
checksums. Most well-known hash functions are supported, including
MD5, SHA1, SHA2 (SHA256/SHA512), SHA3 and BLAKE2.

It's designed to be an easy to use, graphical alternative to
command-line tools such as md5sum.

%description -l pl.UTF-8
GtkHash to graficzne narzędzie do obliczania skrótów lub sum
kontrolnych danych. Obsługiwane są bajbardziej popularne funkcje
skrótu, w tym MD5, SHA1, SHA2 (SHA256/SHA512), SHA3 oraz BLAKE2.

Program jest zaprojektowany jako łatwa w użyciu graficzna alternatywa
dla narzędzi linii poleceń, takich jak md5sum.

%package -n Thunar-gtkhash
Summary:	GtkHash extension for Thunar
Summary(pl.UTF-8):	Rozszerzenie GtkHash dla zarządcy plików Thunar
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	Thunar >= 1.7.0

%description -n Thunar-gtkhash
Caja GtkHash extension for computing message digests or checksums.

%description -n Thunar-gtkhash -l pl.UTF-8
Rozszerzenie Nautilusa GtkHash do obliczania skrótów lub sum
kontrolnych.

%package -n caja-extension-gtkhash
Summary:	GtkHash extension for Caja
Summary(pl.UTF-8):	Rozszerzenie GtkHash dla zarządcy plików Caja
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	caja >= 1.18

%description -n caja-extension-gtkhash
Caja GtkHash extension for computing message digests or checksums.

%description -n caja-extension-gtkhash -l pl.UTF-8
Rozszerzenie Caja GtkHash do obliczania skrótów lub sum kontrolnych.

%package -n nautilus-extension-gtkhash
Summary:	GtkHash extension for Nautilus
Summary(pl.UTF-8):	Rozszerzenie GtkHash dla zarządcy plików Nautilus
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus >= 3

%description -n nautilus-extension-gtkhash
Caja GtkHash extension for computing message digests or checksums.

%description -n nautilus-extension-gtkhash -l pl.UTF-8
Rozszerzenie Nautilusa GtkHash do obliczania skrótów lub sum
kontrolnych.

# must be the last because of Epoch (cinnamon-nemo-extensions.spec 4.x contained gtkhash extension)
%package -n cinnamon-nemo-extension-gtkhash
Summary:	GtkHash extension for Nemo
Summary(pl.UTF-8):	Rozszerzenie GtkHash dla zarządcy plików Nemo
Epoch:		1
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	cinnamon-nemo

%description -n cinnamon-nemo-extension-gtkhash
Nemo GtkHash extension for computing message digests or checksums.

%description -n cinnamon-nemo-extension-gtkhash -l pl.UTF-8
Rozszerzenie Nemo GtkHash do obliczania skrótów lub sum kontrolnych.

%prep
%setup -q

%build
%configure \
	%{?with_caja:--enable-caja} \
	%{?with_nautilus:--enable-nautilus} \
	%{?with_nemo:--enable-nemo} \
	--disable-silent-rules \
	%{?with_thunar:--enable-thunar}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with caja}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/caja/extensions-*/libgtkhash-properties-caja.la
%endif
%if %{with nautilus}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-*/libgtkhash-properties-nautilus.la
%endif
%if %{with nemo}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/nemo/extensions-*/libgtkhash-properties-nemo.la
%endif
%if %{with thunar}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/thunarx-*/libgtkhash-properties-thunar.la
%endif

# unify
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{nb_NO,nb}
# bn_BD has one more translation than bn (as of gtkhash 1.5)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/bn
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{bn_BD,bn}
# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_bindir}/gtkhash
%{_datadir}/glib-2.0/schemas/org.gtkhash.gschema.xml
%if %{with caja} || %{with nautilus} || %{with nemo} || %{with thunar}
%{_datadir}/glib-2.0/schemas/org.gtkhash.plugin.gschema.xml
%endif
%{_datadir}/metainfo/org.gtkhash.gtkhash.appdata.xml
%{_desktopdir}/org.gtkhash.gtkhash.desktop
%{_iconsdir}/hicolor/*x*/apps/org.gtkhash.gtkhash.png
%{_iconsdir}/hicolor/scalable/apps/org.gtkhash.gtkhash.svg

%if %{with thunar}
%files -n Thunar-gtkhash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/thunarx-3/libgtkhash-properties-thunar.so
%{_datadir}/metainfo/org.gtkhash.thunar.metainfo.xml
%endif

%if %{with caja}
%files -n caja-extension-gtkhash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/caja/extensions-2.0/libgtkhash-properties-caja.so
%{_datadir}/caja/extensions/libgtkhash-properties-caja.caja-extension
%{_datadir}/metainfo/org.gtkhash.caja.metainfo.xml
%endif

%if %{with nautilus}
%files -n nautilus-extension-gtkhash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-3.0/libgtkhash-properties-nautilus.so
%{_datadir}/metainfo/org.gtkhash.nautilus.metainfo.xml
%endif

%if %{with nemo}
%files -n cinnamon-nemo-extension-gtkhash
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nemo/extensions-3.0/libgtkhash-properties-nemo.so
%{_datadir}/metainfo/org.gtkhash.nemo.metainfo.xml
%endif
