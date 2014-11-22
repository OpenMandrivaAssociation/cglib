%{?_javapackages_macros:%_javapackages_macros}
Name:           cglib
Version:        3.1
Release:        5%{?dist}
Summary:        Code Generation Library for Java
License:        ASL 2.0 and BSD
Group:          Development/Tools
Url:            http://cglib.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-src-%{version}.jar
Source1:        http://mirrors.ibiblio.org/pub/mirrors/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
Source2:        bnd.properties

Requires: java-headless >= 0:1.6.0
Requires: objectweb-asm

BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  objectweb-asm
BuildRequires:  unzip
BuildRequires:  aqute-bnd
BuildArch:      noarch

%description
cglib is a powerful, high performance and quality code generation library 
for Java. It is used to extend Java classes and implements interfaces 
at runtime.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation
%description javadoc
Documentation for the cglib code generation library.

%prep
%setup -q -c %{name}-%{version}
cp -p %{SOURCE1} pom.xml
rm lib/*.jar
# Remove the repackaging step that includes other jars into the final thing
sed -i "/<taskdef name=.jarjar/,/<.jarjar>/d" build.xml

%pom_xpath_remove "pom:dependency[pom:artifactId = 'asm-util']/pom:optional"

%build
export OPT_JAR_LIST=objectweb-asm
ant jar javadoc
# Convert to OSGi bundle
pushd dist
java -Dcglib.bundle.version="%{version}" \
  -jar $(build-classpath aqute-bnd) wrap -output %{name}-%{version}.bar -properties %{SOURCE2} %{name}-%{version}.jar
popd

%install
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
mkdir -p %{buildroot}%{_mavenpomdir}
# yes, this is really *.bar - aqute bnd created it
install -p -m 644 dist/%{name}-%{version}.bar %{buildroot}%{_javadir}/%{name}.jar
install -p -m 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap -a net.sf.cglib:cglib,cglib:cglib-full,cglib:cglib-nodep,org.sonatype.sisu.inject:cglib

cp -rp docs/* %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%doc LICENSE NOTICE

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Mon Oct 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-5
- Add alias for cglib:cglib-nodep

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-3
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.1-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Jan 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-1
- Update to upstream version 3.1
- Remove patch for upstream bug 44 (fixed upstream)

* Mon Nov 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0-1
- Update to upstream version 3.0
- Add alias for org.sonatype.sisu.inject:cglib

* Mon Aug 05 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.2-17
- Remove old call to %add_to_maven_depmap macro.
- Fixes RHBZ#992051.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-14
- Add additional maven depmap

* Mon Sep 17 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.2-13
- Use aqute bnd in order to generate OSGi metadata.

* Fri Aug 17 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-12
- Add additional depmap

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2-11
- Fix license tag
- Install LICENSE and NOTICE with javadoc package
- Convert versioned JARs to unversioned
- Preserve timestamp of POM file
- Update to current packaging guidelines

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2-7
- Add missing pom file (Resolves rhbz#655793)

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 2.2-6
- BR unzip to fix openSUSE build

* Tue Dec  9 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-5
- Add dist to version
- Fix BuildRoot to follow the latest guidelines

* Mon Nov 24 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-4
- Add a comment explaining the patch

* Thu Nov  6 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-3
- Flag Maven depmap as "config"

* Wed Nov  5 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-2
- Explicitly require Java > 1.6 because it won't compile with gcj
- Fix cosmetic issues in spec file

* Tue Nov  4 2008 Mary Ellen Foster <mefoster at gmail.com> - 2.2-1
- Initial package (based on previous JPP version)

