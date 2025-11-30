#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Low-level, pure Python DBus protocol wrapper
Summary(pl.UTF-8):	Niskopoziomowe obudowanie protokołu DBus w czystym Pythonie
Name:		python3-jeepney
Version:	0.9.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jeepney/
Source0:	https://files.pythonhosted.org/packages/source/j/jeepney/jeepney-%{version}.tar.gz
# Source0-md5:	d0c0d388ee003d6475750aebe56fc699
URL:		https://pypi.org/project/jeepney/
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.11
BuildRequires:	python3-flit_core < 4
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.7
%if %{with tests}
%if "%{_ver_lt %{py3_ver} 3.11}" == "1"
BuildRequires:	python3-async_timeout
%endif
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio >= 0.17
BuildRequires:	python3-pytest-trio
BuildRequires:	python3-testpath
BuildRequires:	python3-trio
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-outcome
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	python3-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
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
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_asyncio.plugin,pytest_trio.plugin" \
%{__python3} -m pytest jeepney
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{py3_sitescriptdir}/jeepney
%{py3_sitescriptdir}/jeepney-%{version}.dist-info
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,api,*.html,*.js}
%endif
