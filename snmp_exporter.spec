%global debug_package %{nil}

Name:           snmp_exporter
Version:        0.24.1
Release:        1%{?dist}
Summary:        A simple hierarchical database supporting plugin data sources

License:        Apache-2.0
URL:            https://github.com/prometheus/%{name}

Source0:        https://github.com/prometheus/%{name}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}.service
Source2:        snmp.yml

BuildRequires:  git
BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

Provides:       %{name} = %{version}

%description
Prometheus exporter for SNMP metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%autosetup

%build
make build

%pre
useradd \
       --system --user-group --shell /sbin/nologin \
       --home-dir /var/lib/%{name} \
       --comment "Prometheus SNMP Exporter" %{name}
exit 0

%install
install -Dpm 0755 %{name}-%{version} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 snmp.yml %{buildroot}%{_sysconfdir}/%{name}/snmp.yml
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
go test -v ./...

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/usr/sbin/userdel %{name}

%files
# Binary
%{_bindir}/%{name}

# Configuration
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/snmp.yml

# systemD
%{_unitdir}/%{name}.service

%license LICENSE


%changelog
* Tue Nov 07 2023 Cody Robertson <cody@nerdymuffin.com> - 0.24.1-1
- Initial build
