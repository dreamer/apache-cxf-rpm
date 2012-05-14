Name:          aries-util
Version:       0.4
Release:       1%{?dist}
Summary:       Apache Aries Util
License:       ASL 2.0
Group:         Development/Libraries
URL:           http://aries.apache.org/

# svn export http://svn.apache.org/repos/asf/aries/tags/org.apache.aries.util-0.4/ aries-util-0.4
# tar cafJ aries-util-0.4.tar.xz aries-util-0.4

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
This bundle contains the OSGi common util for Apache Aries

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
  install javadoc:aggregate

%install

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# jar
install -pm 644 target/org.apache.aries.util-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# pom
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# depmap
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# javadoc
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%doc LICENSE NOTICE
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Mon May 14 2012 Patryk Obara <pobara@redhat.com> 0.4-1
- Initial packaging
