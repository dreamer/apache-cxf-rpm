Name:             cxf-xjc-utils
Version:          2.6.0
Release:          1%{?dist}
Summary:          Apache CXF XJC-Utils
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://cxf.apache.org/xjc-utils.html

# svn export http://svn.apache.org/repos/asf/cxf/xjc-utils/tags/xjc-utils-2.6.0/ cxf-xjc-utils-2.6.0
# tar cafJ cxf-xjc-utils-2.6.0.tar.xz cxf-xjc-utils-2.6.0

Source0:          %{name}-%{version}.tar.xz

Patch0:           %{name}-%{version}-pom.patch

BuildArch:        noarch

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    maven
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-shade-plugin
BuildRequires:    apache-commons-lang
BuildRequires:    glassfish-jaxb
BuildRequires:    glassfish-jaxb-api
BuildRequires:    junit
BuildRequires:    jvnet-parent
BuildRequires:    maven-project
BuildRequires:    maven-shared-downloader
BuildRequires:    maven-surefire-provider-junit4
BuildRequires:    ws-jaxme
BuildRequires:    wsdl4j

Requires:         jpackage-utils
Requires:         java
Requires:         apache-commons-lang
Requires:         glassfish-jaxb
Requires:         junit
Requires:         maven-project
Requires:         maven-shared-downloader
Requires:         maven-surefire-provider-junit4
Requires:         ws-jaxme
Requires:         wsdl4j

%description
The Apache CXF XJC-Utils provides a bunch of utilities for working
with JAXB to generate better or more usable code.

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}

%patch0 -p1

%build
# test fail because of missing dependencies
mvn-rpmbuild \
	-Dmaven.test.skip=true \
	-Dproject.build.sourceEncoding=UTF-8 \
	package javadoc:aggregate


%install
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_javadir}/%{name}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}

for module in boolean bug671 cxf-xjc-plugin dv \
              property-listener runtime ts wsdlextension;
do
	pushd $module

	case $module in
	cxf-xjc-plugin)    module=plugin ;;
	property-listener) module=pl ;;
	esac

	install -pm 644 target/cxf-xjc-$module-%{version}.jar %{buildroot}%{_javadir}/%{name}/cxf-xjc-$module.jar
	install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-cxf-xjc-$module.pom
	%add_maven_depmap JPP.%{name}-cxf-xjc-$module.pom %{name}/cxf-xjc-$module.jar
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
* Thu May 10 2012 Patryk Obara <pobara@redhat.com> 2.4.1-1
- Initial packaging

