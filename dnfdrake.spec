%global gb3_ver %(gbc3 -V || echo 3.18.2)

Summary:	A frontend for DNF
Name:		dnfdrake
Version:	3.6.12
Release:	2
License:	GPLv3
Group:		Graphical desktop/KDE
URL:           https://mib.pianetalinux.org
#URL:		https://github.com/astrgl/dnfdrake
Source0:	https://github.com/astrgl/dnfdrake/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	gambas3-devel
BuildRequires:	gambas3-gb-dbus
BuildRequires:	gambas3-gb-form
BuildRequires:	gambas3-gb-form-stock
BuildRequires:	gambas3-gb-gtk3
BuildRequires:	gambas3-gb-gui
BuildRequires:	gambas3-gb-image
BuildRequires:	gambas3-gb-qt5
BuildRequires:	imagemagick

Requires:	sudo
Requires:	createrepo_c
Requires:	dnf-utils
Requires:	gambas3-runtime = %{gb3_ver}
Requires:	gambas3-devel
Requires:	gambas3-gb-dbus
Requires:	gambas3-gb-form
Requires:	gambas3-gb-form-stock
Requires:	gambas3-gb-gtk3
Requires:	gambas3-gb-gui
Requires:	gambas3-gb-image
Requires:	gambas3-gb-qt5
Requires:	lsb-release
Requires:	python-dnf-plugin-versionlock
Requires:	xrandr
Requires:	dnfdraketray

Suggests:	dnfdrake

BuildArch: noarch

%files
%license FILE-EXTRA/license
%{_bindir}/%{name}.gambas
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.svg

#---------------------------------------------------------------------------

%description
DnfDrake is a frontend for DNF package manager
Powerful like a terminal and simple like a GUI!

%prep
%autosetup -p1

%build
gbc3 -e -a -g -t -f public-module -f public-control -j%{?_smp_mflags}
gba3

# unversion binary
mv %{name}-%{version}.gambas %{name}.gambas

%install
# binary
install -Dm 0755 %{name}.gambas -t %{buildroot}/%{_bindir}/

# data files
install -Dm 0644 FILE-EXTRA/%{name}-*-* -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 0644 FILE-EXTRA/%{name}-COMMAND -t %{buildroot}/%{_datadir}/%{name}/

#.desktop
install -Dm 0755 FILE-EXTRA/%{name}.desktop -t %{buildroot}/%{_datadir}/applications

# icons
install -Dm 0644 %{name}.svg -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
for d in 16 32 48 64 72 128 256 512
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -scale ${d}x${d} %{name}.svg \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -scale 32x32 %{name}.svg %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

