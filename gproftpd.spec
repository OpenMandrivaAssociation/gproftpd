Summary:	GNOME GUI Tool for Proftpd Server Configuration
Name:		gproftpd
Version:	8.3.2
Release:	%mkrel 2
Group:		System/Configuration/Networking
License:	GPL
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynup.net/linux/gproftpd/%{name}-%{version}.tar.bz2
Source1:	%{name}.pam-0.77.bz2
Source2:	%{name}.pam.bz2
Requires:	proftpd >= 1.2.8
Requires:	usermode-consoleonly
BuildRequires:	gtk+2-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GProftpd is a fast and easy to use GNOME2 administration tool for
the Proftpd standalone server.

%prep

%setup -q

# fix conditional pam config file
%if %{mdkversion} < 200610
bzcat %{SOURCE1} > %{name}.pam
%else
bzcat %{SOURCE2} > %{name}.pam
%endif

%build
# (Abel) otherwise it would try to find files such as /var/lib/log/xferlog
%define _localstatedir /var

%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall
rm -fr $RPM_BUILD_ROOT/%_docdir

install -d %{buildroot}%{_sysconfdir}/pam.d/
install -m0644 %{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}

# locales
%find_lang %name

# Mandriva Icons
install -D -m644 pixmaps/%{name}32.png %{buildroot}%{_iconsdir}/%{name}.png
install -D -m644 pixmaps/%{name}16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m644 pixmaps/%{name}48.png %{buildroot}%{_liconsdir}/%{name}.png

# Mandriva Menus
install -d %{buildroot}/%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
 command="%{_sbindir}/%{name}" \
 title="GProftpd" \
 longtitle="Proftpd administration tool" \
 needs="x11" \
 icon="%{name}.png" \
 section="System/Configuration/Networking" \
 xdg="true" 
EOF

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GProftpd
Comment=Proftpd administration tool
Exec=%{_sbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
EOF


# Prepare usermode entry
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_sbindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog README
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}.real
%{_sbindir}/gprostats
%{_datadir}/pixmaps/*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*
%defattr(0600,root,root,0700)
%config(noreplace) %{_sysconfdir}/%{name}


