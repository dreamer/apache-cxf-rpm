Name:             cxf-build-utils
Version:          2.4.1
Release:          1%{?dist}
Summary:          Apache CXF build utils
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://cxf.apache.org/build-utils.html

# svn export http://svn.apache.org/repos/asf/cxf/build-utils/tags/cxf-build-utils-2.4.1/ apache-cxf-build-utils-2.4.1
# tar cafJ apache-cxf-build-utils-2.4.1.tar.xz apache-cxf-build-utils-2.4.1
Source0:          apache-%{name}-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    maven
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-shade-plugin

Requires:         jpackage-utils
Requires:         java

%description
Apache something something FIXME.

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n apache-%{name}-%{version}

%build
mvn-rpmbuild \
  -Dmaven.test.skip=true \
  -Dproject.build.sourceEncoding=UTF-8 \
  install javadoc:aggregate

%install
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

for module in buildtools xml2fastinfoset-plugin; do
	pushd $module
	install -pm 644 target/cxf-$module-%{version}.jar %{buildroot}%{_javadir}/%{name}/cxf-$module.jar
	install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-cxf-$module.pom
	%add_maven_depmap JPP.%{name}-cxf-$module.pom %{name}/cxf-$module.jar
	popd
done

install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}.pom
%add_maven_depmap JPP.%{name}.pom

# javadoc
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Wed May 9 2012 Patryk Obara <pobara@redhat.com> 2.4.1-1
- Initial packaging

