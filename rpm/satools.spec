Name:		satools
Version:	0.4
Release:	1%{?dist}
Summary:	Red Hat UK&I SA tools
License:	GPL
URL:		https://github.com/RedHatUKI/satools
Source:		satools.tar.gz
BuildArch:	noarch
Requires:	mimehandler(application/x-java-jnlp-file), python-BeautifulSoup, python-lxml
BuildRequires:	redhat-rpm-config

%define _srcdefattr (-,root,root)

%description
Red Hat UK&I SA tools

%prep
%setup -qc

%install
mkdir -p %{buildroot}/%{python_sitelib}
cp -a satools %{buildroot}/%{python_sitelib}

%clean
rm -rf %{buildroot}

%post
for i in elluminate lgrep mailindex sync-clearspace sync-lists sync-product-docs
do
  ln -sf %{python_sitelib}/satools/$i.py %{_bindir}/$i
done

%postun
for i in elluminate lgrep mailindex sync-clearspace sync-lists sync-product-docs
do
  rm -f %{_bindir}/$i
done

%files
%defattr(-,root,root,-)
%{python_sitelib}
%doc README.rst

%changelog

* Fri Mar 23 2012 Jim Minter <jminter@redhat.com> 0.4

* Mon Mar 19 2012 Jim Minter <jminter@redhat.com> 0.3

* Fri Nov 18 2011 Jim Minter <jminter@redhat.com> 0.2

* Mon Nov 14 2011 Jim Minter <jminter@redhat.com> 0.1
- First release
