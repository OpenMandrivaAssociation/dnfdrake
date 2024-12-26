%define gb3_ver %(if rpm -q gambas-devel &>/dev/null; then rpm -q --qf '%%{version}' gambas-devel; else echo -n 3.19; fi)
%define gb3_major %(echo %{gb3_ver} |cut -d. -f1-2)
%define gb3_next_major %(echo -n $(echo %{gb3_major} |cut -d. -f1).; GB_MINOR=$(echo %{gb3_ver}|cut -d. -f2); echo -n $((GB_MINOR+1)))

Summary:	A frontend for DNF
Name:		dnfdrake
Version:	4.2.97
Release:	3
License:	GPLv3
Group:		Graphical desktop/KDE
URL:		https://mib.pianetalinux.org
#URL:		https://github.com/astrgl/dnfdrake
#Source0:	https://github.com/astrgl/dnfdrake/archive/%{version}/%{name}-%{version}.tar.gz
Source:		%{name}-%{version}.tar.gz

BuildRequires:	gambas-devel
BuildRequires:	gambas-gb.dbus
BuildRequires:	gambas-gb.form
BuildRequires:	gambas-gb.form.stock
BuildRequires:	gambas-gb.gui
BuildRequires:	gambas-gb.image
BuildRequires:	gambas-gui-backend
BuildRequires:	imagemagick

Requires:	sudo
Requires:	createrepo_c
Requires:	dnf-utils
Requires:	(gambas-runtime >= %{gb3_major} with gambas-runtime < %{gb3_next_major})
Requires:	(gambas-gb.dbus >= %{gb3_major} with gambas-gb.dbus < %{gb3_next_major})
Requires:	(gambas-gb.form >= %{gb3_major} with gambas-gb.form < %{gb3_next_major})
Requires:	(gambas-gb.form.stock >= %{gb3_major} with gambas-gb.form.stock < %{gb3_next_major})
Requires:	(gambas-gb.gui >= %{gb3_major} with gambas-gb.gui < %{gb3_next_major})
Requires:	(gambas-gui-backend >= %{gb3_major} with gambas-gui-backend < %{gb3_next_major})
Requires:	(gambas-gb.image >= %{gb3_major} with gambas-gb.image < %{gb3_next_major})
Requires:	lsb-release
Requires:	python-dnf-plugin-versionlock
Requires:	xrandr
Requires:	draketray

BuildArch: noarch

%description
DnfDrake is a frontend for DNF package manager
Powerful like a terminal and simple like a GUI!


%files
%license FILE-EXTRA/license
%{_bindir}/%{name}.gambas
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.xpm
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.svg

#---------------------------------------------------------------------------

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
install -Dm 0644 FILE-EXTRA/license -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 0644 FILE-EXTRA/COPYING* -t %{buildroot}/%{_datadir}/%{name}/


install -Dm 0644 FILE-EXTRA/%{name}-COMMAND -t %{buildroot}/%{_datadir}/%{name}/

# logos
install -Dm 0644 LINUX.png -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 0644 OMA-BD.png -t %{buildroot}/%{_datadir}/%{name}/
install -Dm 0644 OMA.png -t %{buildroot}/%{_datadir}/%{name}/

#.desktop
install -Dm 0755 FILE-EXTRA/%{name}.desktop -t %{buildroot}/%{_datadir}/applications

# icons
install -Dm 0644 ICONS-EXTRA/* -t %{buildroot}%{_datadir}/%{name}/
install -Dm 0644 ICONS-EXTRA/* -t %{buildroot}%{_datadir}/%{name}/icons/
install -Dm 0644 %{name}.svg -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
for d in 16 32 48 64 72 128 256 512
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -scale ${d}x${d} %{name}.svg \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -scale 32x32 %{name}.svg %{buildroot}%{_datadir}/pixmaps/%{name}.xpm
