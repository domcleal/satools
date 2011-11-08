Name:		satools-search
Version:	0.1
Release:	1%{?dist}
Summary:	Red Hat UK&I SA tools list search engine
License:	GPL
URL:		https://github.com/RedHatUKI/satools
Source:		satools.tar.gz
BuildArch:	noarch
Requires:	satools, python-webpy, httpd, mod_wsgi

%define _srcdefattr (-,root,root)

%description
Red Hat UK&I SA tools list search engine

%prep
%setup -qc

%build
%__make search

%install
mkdir -p %{buildroot}/opt/satools/search/static/extjs
cp -a search/app/{*.py,templates} %{buildroot}/opt/satools/search
cp -a search/app/static/{app-all.js,app.css,controller,store,view} %{buildroot}/opt/satools/search/static
cp search/app/static/index-prod.html %{buildroot}/opt/satools/search/static/index.html
cp search/app/static/extjs/ext.js %{buildroot}/opt/satools/search/static/extjs
cp -a search/app/static/extjs/resources %{buildroot}/opt/satools/search/static/extjs

mkdir -p %{buildroot}/etc/httpd/conf.d
cp search/httpd-conf/* %{buildroot}/etc/httpd/conf.d

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-,root,root,-)
/
%doc README

%changelog

* Tue Nov 08 2011 Jim Minter <jminter@redhat.com> 0.1
- First release