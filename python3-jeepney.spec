#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Low-level, pure Python DBus protocol wrapper
Summary(pl.UTF-8):	Niskopoziomowe obudowanie protokołu DBus w czystym Pythonie
Name:		python3-jeepney
Version:	0.4.3
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jeepney/
Source0:	https://files.pythonhosted.org/packages/source/j/jeepney/jeepney-%{version}.tar.gz
# Source0-md5:	18afe08d79ad87f626186dd68939ab47
URL:		https://pypi.org/project/jeepney/
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-testpath
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	python3-modules >= 1:3.5
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a low-level, pure Python DBus protocol client. It has an
I/O-free core, and integration modules for different event loops.

DBus is an inter-process communication system, mainly used in Linux.

%description -l pl.UTF-8
Jeepney to niskopoziomowy, napisany w czystym Pythonie klient
protokołu DBus. Wewnętrznie jest oparty na podejściu I/O-free, ma
moduły integrujące dla różnych pętli zdarzeń.

DBus to system komunikacji międzyprocesowej, używany głównie na
Linuksie.

%package apidocs
Summary:	jeepney API documentation
Summary(pl.UTF-8):	Dokumentacja API jeepney
Group:		Documentation

%description apidocs
API documentation for jeepney.

%description apidocs -l pl.UTF-8
Dokumentacja API jeepney.

%prep
%setup -q -n jeepney-%{version}

%build
%py3_build

%if %{with tests}
%{__python3} -m pytest jeepney/tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/jeepney/tests

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/jeepney
%{py3_sitescriptdir}/jeepney-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
