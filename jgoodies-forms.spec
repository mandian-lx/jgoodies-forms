%define gcj_support 1
%define short_name forms

Name: jgoodies-forms
Summary: Framework to lay out and implement elegant Swing panels in Java
URL: http://www.jgoodies.com/freeware/forms/
Group: Development/Java
Version: 1.0.7
Epoch: 0
Release: %mkrel 1
License: BSD
#Vendor:         JPackage Project
#Distribution:   JPackage

BuildRequires: jpackage-utils >= 0:1.6
BuildRequires: ant
Requires: java >= 0:1.4
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires: java-devel >= 0:1.4.2
BuildArch:      noarch
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0: http://www.jgoodies.com/download/libraries/%{short_name}-%{version}.tar.bz2
Source1: %{name}.README

%description
The JGoodies Forms framework helps you lay out and implement elegant Swing
panels quickly and consistently. It makes simple things easy and the hard
stuff possible, the good design easy and the bad difficult.

Main Benefits:

* Powerful, flexible and precise layout
* Easy to work with and quite easy to learn
* Faster UI production
* Better UI code readability
* Leads to better style guide compliance

%package javadoc
Summary: Javadoc documentation for JGoodies Forms
Group: Development/Java

%description javadoc
The JGoodies Forms framework helps you lay out and implement elegant Swing
panels quickly and consistently. It makes simple things easy and the hard
stuff possible, the good design easy and the bad difficult.

This package contains the Javadoc documentation for JGoodies Forms.

%prep
%setup -q -n %{short_name}-%{version}
find . -type f -name "*.html" -o -name "*.css" -o -name "*.txt" -o -name "*.java" | \
  xargs %{__perl} -pi -e 's/\r$//g'

%build
export CLASSPATH=%{java_home}/jre/lib/rt.jar
export OPT_JAR_LIST=
%ant -Djavadoc.link=%{_javadocdir}/java compile jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir} \
	$RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -m 644 build/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{short_name}-%{version}.jar
ln -s %{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{short_name}.jar
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -m 644 %SOURCE1 README_RPM.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
ln -s %{_javadocdir}/%{name}-%{version} %{_docdir}/%{name}-javadoc/docs/api

%preun javadoc
rm -f %{_docdir}/%{name}-javadoc/docs/api

%files
%defattr(-,root,root)
%{_javadir}/%{short_name}*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif
%doc RELEASE-NOTES.txt

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}
%doc RELEASE-NOTES.txt README_RPM.txt README.html docs/ src/tutorial/ build/classes/tutorial/
