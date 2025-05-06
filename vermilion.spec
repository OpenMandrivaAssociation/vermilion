%global debug_package %{nil}
%global commit 9b84b995510dd17d60685aab5f466c244c575f3f
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		vermilion
Version:	1.git%{shortcommit}
Release:	1
Source0:	https://github.com/vaxerski/vermilion/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:    vermilion-pnpm-store.tar.gz
Source2:    %{name}.desktop
Summary:	Vermilion is a clean, minimal and simple music player for MPD, Tidal, Spotify and more.
URL:		https://github.com/vaxerski/vermilion
License:	BSD-3-Clause
Group:		Applications/Music

BuildRequires:	pnpm
BuildRequires:	nodejs-electron-builder
BuildRequires:	castlabs-electron-releases-35.1.5+wvcus

%description
Vermilion is a clean, minimal and simple music player for MPD, Tidal, Spotify and more.

%prep
%autosetup -n Vermilion-%{commit} -p1
tar -xzf %{SOURCE1}
mkdir -p %{builddir}/Vermilion-%{commit}/electron_cache

%build
pnpm config set store-dir %{_builddir}/Vermilion-%{commit}/pnpm-store
pnpm install --frozen-lockfile --offline
pnpm run build
ELECTRON_CACHE=%{_prefix}/src/electron electron-builder --dir

%install
install -d %{buildroot}%{_datadir}/applications/ %{buildroot}%{_datadir}/%{name} %{buildroot}%{_bindir}
cp -r dist/*-unpacked/* %{buildroot}%{_datadir}/%{name}
install -Dm755 %{SOURCE2} %{buildroot}%{_datadir}/applications/
install -Dm644 assets/logo.png %{buildroot}%{_datadir}/pixmaps/vermilion.png
install -Dm644 assets/logo256.png %{buildroot}%{_iconsdir}/hicolor/256x256/app/%{name}.png
install -Dm644 assets/logo1024.png %{buildroot}%{_iconsdir}/hicolor/1024x1024/app/%{name}.png
ln -s %{_datadir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%{_iconsdir}/hicolor/256x256/app/%{name}.png
%{_iconsdir}/hicolor/1024x1024/app/%{name}.png
%{_datadir}/pixmaps/vermilion.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
