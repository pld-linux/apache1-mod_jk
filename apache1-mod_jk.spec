%define		apxs		/usr/sbin/apxs1
Summary:	Apache module that handles communication between Tomcat and Apache 1.3.x
Summary(pl):	Modu³ Apache'a obs³uguj±cy komunikacjê miêdzy Tomcatem a Apachem 1.3.x
%define		mod_name	jk
Name:		apache1-mod_%{mod_name}
Version:	1.2.5
Release:	0.1
License:	Apache
Group:		Networking/Daemons
Source0:	http://sunsite.icm.edu.pl/pub/www/apache/dist/jakarta/tomcat-connectors/jk/source/jakarta-tomcat-connectors-jk-%{version}-src.tar.gz
# Source0-md5:	55727c871286e010222bb0fb91f21d08
Source1:	%{name}.conf
Patch0:		jakarta-tomcat-connectors-jk-jkpass.patch
URL:		http://jakarta.apache.org/builds/jakarta-tomcat-connectors/jk/doc/
BuildRequires:	%{apxs}
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	perl-base
PreReq:		apache(EAPI) < 2.0.0
PreReq:		apache(EAPI) >= 1.3.9
Requires(post,preun):	%{apxs}
Requires(post,preun):	%{__perl}
Requires(post,preun):	grep
Requires(preun):	fileutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	jakarta-tomcat-connectors-jk

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_apacheconfdir	%(%{apxs} -q SYSCONFDIR)
%define		_apacheconf	%{_apacheconfdir}/apache.conf

%description
JK is a replacement to the elderly mod_jserv. It was a completely new
Tomcat-Apache plug-in that handles the communication between Tomcat
and Apache.

%description -l pl
JK jest zamiennikiem starego mod_jserv. Jest ca³kowicie now± wtyczk±
Tomcat-Apache obs³uguj±c± komunikacjê miêdzy Tomcatem a Apachem.

%prep
%setup -q -n jakarta-tomcat-connectors-jk-%{version}-src
%patch0 -p1

%build
cd jk/native

./buildconf.sh

%configure \
	--enable-EAPI \
	--with-apxs=%{apxs}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_apacheconf},/var/lock/mod_jk}

cd jk/native

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	APXS="%{apxs} -S LIBEXECDIR=$RPM_BUILD_ROOT$(%{apxs} -q LIBEXECDIR)" \
	libexecdir=$RPM_BUILD_ROOT%{_pkglibdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_apacheconfdir}/mod_jk.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f %{_apacheconf} ] && ! grep -q "^Include.*mod_jk.conf" %{_apacheconf}; then
	echo "Include /etc/apache/mod_jk.conf" >> %{_apacheconf}
fi
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	umask 027
	grep -v "^Include.*mod_jk.conf" %{_apacheconf} > \
		%{_apacheconf}.tmp
	mv -f %{_apacheconf}.tmp %{_apacheconf}
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc jk/native/{README,CHANGES.txt} jk/docs/*
%config(noreplace) %{_apacheconfdir}/mod_jk.conf
%attr(755,root,root) %{_pkglibdir}/*
%attr(750,http,http) /var/lock/mod_jk
