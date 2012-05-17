Name:          aries-blueprint
Version:       0.3.1
Release:       1%{?dist}
Summary:       Apache Aries Blueprint
License:       ASL 2.0
Group:         Development/Libraries
URL:           http://aries.apache.org/

# svn export http://svn.apache.org/repos/asf/aries/tags/blueprint-0.3.1/ aries-blueprint-0.3.1
# tar cafJ aries-blueprint-0.3.1.tar.xz aries-blueprint-0.3.1

Source0:       %{name}-%{version}.tar.xz
Patch0:        %{name}-%{version}-xml.patch
Patch1:        %{name}-%{version}-java.patch

BuildArch:     noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: maven
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-release-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-plugin

Requires:      java
Requires:      jpackage-utils

%description
Implementation of the Blueprint Container Specification

%package javadoc
Summary:       Javadocs for %{name}
Group:         Documentation
Requires:      jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%build
# FIXME try enabling tests
mvn-rpmbuild \
  -Dmaven.test.skip=true \
  -Dproject.build.sourceEncoding=UTF-8 \
  package javadoc:aggregate

%install

install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

# modules
for module in blueprint-annotation-api blueprint-api blueprint-cm \
              blueprint-core blueprint-sample;
do
	pushd $module
	jarname=`echo org.apache.aries.$module | tr - .`
	install -pm 644 target/$jarname-%{version}.jar %{buildroot}%{_javadir}/%{name}/$jarname.jar
	install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-$jarname.pom
	%add_maven_depmap JPP.%{name}-$jarname.pom %{name}/$jarname.jar
	popd
done

# pom
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}.pom

# depmap
%add_maven_depmap JPP.%{name}.pom

# javadoc
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}


%files
%doc README LICENSE NOTICE
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*

%files javadoc
%doc README LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Thu May 17 2012 Patryk Obara <pobara@redhat.com> 0.3.1-1
- Initial packaging
