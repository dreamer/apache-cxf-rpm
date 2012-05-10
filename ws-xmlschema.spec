Name:             ws-xmlschema
Version:          2.0.2
Release:          1%{?dist}
Summary:          XMLSchema FIXME
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://ws.apache.org/commons/xmlschema20/

# svn checkout http://svn.apache.org/repos/asf/webservices/xmlschema/tags/xmlschema-2.0.2/ ws-xmlschema-2.0.2
# tar cafJ ws-xmlschema-2.0.2.tar.xz ws-xmlschema-2.0.2
Source0:          %{name}-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    apache-resource-bundles
BuildRequires:    maven
BuildRequires:    maven-assembly-plugin
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-remote-resources-plugin
BuildRequires:    maven-shade-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    xmlunit

Requires:         jpackage-utils
Requires:         java

%description
XMLSchema is a lightweight schema object model that can be used to
manipulate and generate XML schema representations. It has very few external
dependencies and can be easily integrated into an existing project.

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

%build
# fastinstall profile avoids some build dependencies
# tests require unavailable dependencies
mvn-rpmbuild \
	-Pfastinstall \
	-Dmaven.test.skip=true \
	-Dproject.build.sourceEncoding=UTF-8 \
	install javadoc:aggregate

%install
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

module=xmlschema-core
pushd $module
install -pm 644 target/$module-%{version}.jar %{buildroot}%{_javadir}/%{name}/$module.jar
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-$module.pom
%add_maven_depmap JPP.%{name}-$module.pom %{name}/$module.jar
popd

install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}.pom
%add_maven_depmap JPP.%{name}.pom

# javadoc
cp -rp target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%doc README.txt RELEASE-NOTE.txt
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Wed May 2 2012 Patryk Obara <pobara@redhat.com> 1.0.0-1
- Initial packaging

