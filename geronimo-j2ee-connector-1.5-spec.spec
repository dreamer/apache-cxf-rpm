%global api_version 1.5
Name:          geronimo-j2ee-connector-%{api_version}-spec
Version:       2.0.0
Release:       1%{?dist}
Summary:       Java Authentication SPI for Containers FIXME
License:       ASL 2.0
Group:         Development/Libraries
URL:           http://geronimo.apache.org/

# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/geronimo-j2ee-connector_1.5_spec-2.0.0/ geronimo-j2ee-connector-1.5-spec-2.0.0
# tar cafJ geronimo-j2ee-connector-1.5-spec-2.0.0.tar.xz geronimo-j2ee-connector-1.5-spec-2.0.0

Source0:       %{name}-%{version}.tar.xz
#Patch0:        geronimo-jaspic-spec-use-parent-pom.patch

BuildArch:     noarch

BuildRequires: java-devel
BuildRequires: maven
BuildRequires: maven-plugin-bundle
BuildRequires: geronimo-parent-poms
BuildRequires: jpackage-utils

Requires:      java
Requires:      jpackage-utils

%description
FIXME update description
Java Authentication Service Provider Interface for Containers (JSR-196) api.

%package javadoc
Group:          Documentation
Summary:        API documentation for %{name}
Requires:       jpackage-utils

%description javadoc
%{summary}.


%prep
%setup -q -n %{name}-%{version}

%build
# tests don't compile
mvn-rpmbuild \
	-Dmaven.test.skip=true \
	-Dproject.build.sourceEncoding=UTF-8 \
	install javadoc:aggregate

%install
mkdir -p %{buildroot}%{_javadir}
install -m 644 target/geronimo-j2ee-connector_%{api_version}_spec-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}


%files
%doc LICENSE.txt NOTICE.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Fri May 10 2012 Patryk Obara <pobara@redhat.com> - 1.0-1
- Initial package
