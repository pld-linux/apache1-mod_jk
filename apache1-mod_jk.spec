%define		mod_name	jk
%define		apxs		/usr/sbin/apxs1
Summary:	Apache module that handles communication between Tomcat and Apache 1.3.x
Summary(pl.UTF-8):	Moduł Apache'a obsługujący komunikację między Tomcatem a Apachem 1.3.x
Name:		apache1-mod_%{mod_name}
Version:	1.2.25
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.apache.org/dist/tomcat/tomcat-connectors/jk/source/tomcat-connectors-%{version}-src.tar.gz
# Source0-md5:	4f614130c85f86d8d3359a03230db8a3
Source1:	%{name}.conf
URL:		http://jakarta.apache.org/builds/jakarta-tomcat-connectors/jk/doc/
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1-mod_dir >= 1.3.33-2
Obsoletes:	jakarta-tomcat-connectors-jk
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
JK is a replacement to the elderly mod_jserv. It was a completely new
Tomcat-Apache plug-in that handles the communication between Tomcat
and Apache.

%description -l pl.UTF-8
JK jest zamiennikiem starego mod_jserv. Jest całkowicie nową wtyczką
Tomcat-Apache obsługującą komunikację między Tomcatem a Apachem.

%prep
%setup -q -n tomcat-connectors-%{version}-src

%build
cd native

./buildconf.sh

%configure \
	--enable-EAPI \
	--with-apxs=%{apxs}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d,/var/lock/mod_jk}

cd native

install apache-1.3/mod_%{mod_name}.so.0.0.0 $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc native/{CHANGES,README} docs/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
%attr(750,http,http) /var/lock/mod_jk
