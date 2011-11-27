%define shortname forms

Name: jgoodies-forms
Summary: Framework to lay out and implement elegant Swing panels in Java
URL: http://www.jgoodies.com/freeware/forms/
Group: Development/Java
Version: 1.2.0
Release: 6
License: BSD

BuildRequires: jpackage-utils >= 0:1.6
BuildRequires: java-devel >= 0:1.4
BuildRequires: ant
Requires: java >= 0:1.4
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

# Unfortunately, the filename has the version in an annoying way
Source0: http://www.jgoodies.com/download/libraries/%{shortname}/%{shortname}-1_2_0.zip
Patch0: %{name}-build.patch

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
%setup -q -n %{shortname}-%{version}
%patch0 -p1
rm %{shortname}-%{version}.jar
rm -r docs/api

%build
export CLASSPATH=""
%ant compile jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -p -d $RPM_BUILD_ROOT%{_javadir} \
        $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -p -m 644 build/%{shortname}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
# Fix the line endings and the encodings
for file in *.txt *.html docs/*.* docs/reference/* docs/tutorial/* \
        src/tutorial/com/jgoodies/forms/tutorial/*.java \
        src/tutorial/com/jgoodies/forms/tutorial/*/*.java
do
    sed -i 's/\r//' $file
done
for file in docs/reference/*.html docs/tutorial/*.html
do
    iconv --from=ISO-8859-1 --to=UTF-8 $file > $file.new
    sed -i 's/iso-8859-1/utf-8/' $file.new
    mv $file.new $file
done
cd $RPM_BUILD_ROOT%{_javadocdir}
ln -s %{name}-%{version} %{name}

%clean
# rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%doc RELEASE-NOTES.txt LICENSE.txt README.html docs/ src/tutorial/

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

