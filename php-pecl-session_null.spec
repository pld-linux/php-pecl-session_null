%define		modname	session_null
Summary:	null session save handler for PHP
Summary(pl.UTF-8):	Obsługa zapisywania sesji w bazie null dla PHP
Name:		php-pecl-%{modname}
Version:	0.5
Release:	3
License:	MIT
Group:		Development/Languages/PHP
Source0:	http://glen.alkohol.ee/pld/%{modname}-%{version}.tar.bz2
# Source0-md5:	230c008bde95b0d888edbddb7b55e455
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(session_null)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
null session save handler for PHP.

%description -l pl.UTF-8
Obsługa zapisywania sesji w bazie null dla PHP.

%prep
%setup -q -n %{modname}-%{version}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
