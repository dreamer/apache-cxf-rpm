Name:          aries-quiesce
Version:       0.3
Release:       1%{?dist}
Summary:       Apache Aries Quiesce
License:       ASL 2.0
Group:         Development/Libraries
URL:           http://aries.apache.org/

# svn export http://svn.apache.org/repos/asf/aries/tags/quiesce-0.3/ aries-quiesce-0.3
# tar cafJ aries-quiesce-0.3.tar.xz aries-quiesce-0.3

Source0:       %{name}-%{version}.tar.xz
Patch0:        %{name}-%{version}-xml.patch

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
Quiesce support for Aries

%package javadoc
Summary:       Javadocs for %{name}
Group:         Documentation
Requires:      jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

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
for module in api manager;
do
	pushd quiesce-$module
	jarname=org.apache.aries.quiesce.$module
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
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon May 14 2012 Patryk Obara <pobara@redhat.com> 0.3-1
- Initial packaging
