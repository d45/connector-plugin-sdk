---
title: How to Package and Sign Your Connector for Distribution 
---

Packaging provides a convenient way to distribute your connector as a single .taco (Tableau Connector) file.  Signing ensures that Tableau will load only .taco files that have been signed, ensuring that they haven't been tampered with. Signing is done using the JDK and a certificate trusted by a root certificate authority (CA) that has been installed in your Java environment. Tableau Desktop verifies and loads signed connectors from a standard location (My Tableau Repository\\Connectors) or from a user supplied directory. 

This document explains how to package and sign your connector using the Connector SDK. 

## Before you begin 

Make sure you have the following:

-   Python version 3.7.3 or later 

-   Java JDK is installed, JAVA\_HOME is set, and the JDK is in your PATH environment variable 

-   Tableau Desktop 2019.4 or later   

-   A connector developed with the SDK that you would like to package or sign 

-   [Git](https://git-scm.com/downloads)

 

### Set up the virtual environment for packaging and signing

Follow these steps to get the packaging and signing tool and set up the virtual environment. 

1.  Get the [Connector SDK repository](https://github.com/tableau/connector-plugin-sdk) on GitHub.

    For example, open a terminal in the directory where you want to copy the Tableau Connector SDK. Then run the following command to clone the Tableau Connector SDK git repository:

    ```
    git clone https://github.com/tableau/connector-plugin-sdk.git
    ```

1.  Set up the virtual environment by going to the connector-packager folder and running python –m venv .venv  

    For example: 
    
    ```
    C:\\connector-plugin-sdk\\connector-packager> python -m venv .venv
    ```
    
    For more information about venv, see [venv – Creation of virtual environments](https://docs.python.org/3/library/venv.html) on the Python website.

1.  Activate the virtual environment using the activate command.  

    For example:  

    ```
    C:\\connector-plugin-sdk\\connector-packager>.\\.venv\\Scripts\\activate  
    ```

1.  Install the packaging module in the virtual environment: 

    ```
    (.venv) C:\\connector-plugin-sdk\\connector-packager>python setup.py install  
    ```

## Use keytool to get a certificate

Getting a certificate is a multi-step process.

### Step 1: Use keytool to generate a key pair 

To generate a key pair, run this command:

```
keytool -genkeypair -alias alias -keystore keystore 
```

For example: 

```
(.venv) D:\\connector-plugin-sdk\\connector-packager>keytool -genkey -alias test1year -keystore test1yearkeystore.jks -validity 365 
```

For more information about keytool arguments, see the Java Documentation about [keytool](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/keytool.html) on the Oracle website. 

 

### Step 2: Export key to certificate file

Run this command to export the key to a certificate file: 

```
keytool -export -alias alias -file cert\_file -keystore keystore 
```

For example: 

```
(.venv) D:\\connector-plugin-sdk\\connector-packager>keytool -export -alias test1year -file test1year.crt -keystore test1yearkeystore.jks 
```
 

### Step 3: Generate a Certificate Signing Request 

A certificate signing request (CSR) is a request for a certificate authority (CA) to create a public certificate for your organization. To generate a CSR, run the following command:

```
keytool -certreq -alias alias -keystore keystore -file certreq\_file  
```

For example: 

```
(.venv) D:\\connector-plugin-sdk\\connector-packager>keytool -certreq -alias test1year -keystore test1yearkeystore.jks -file test1year.csr 
```
 

### Step 4: Get the CSR signed by the certificate authority 

Send the certificate signing request to the CA you want to create a certificate for you (for example, Verisign, Thawte, or some other CA). The CA will sign the CSR file with their own signature and send that certificate back to you. You can then use this signed certificate to sign the .taco file.

After you receive/fetch the new certificate from the CA, along with any applicable 'chain' or 'intermediate' certificates, run the following command to install the new cert and chain into the keystore:

```
keytool -importcert 
```

### (Optional) Step 5: Import certificate to JRE keystore 

You can import the certificate to the JRE keystore to simulate Step 4 before you get the signed certificate back from the CA. You might want to do this so you can test packaging and signing your connector. To import the certificate, run the following command:

```
keytool -import -trustcacerts -alias alias -file crt -file -keystore "C:\\Program Files\\Java\\jdk1.8.0\_131\\jre\\lib\\security\\cacerts" -storepass changeit 
```

**Note:** The path to cacerts is under java\\jdk1.8.0.131\\jre\\lib\\security, not java\\jre1.8.0\_xxx.  For JDK 9 or later, cacerts is under java\\jdk1.xxx\\lib\\security\\. 

For example: 

```
(.venv) D:\\connector-plugin-sdk\\connector-packager>keytool -import -trustcacerts -alias test1year -file test1year.crt -keystore "C:\\Program Files\\Java\\jdk1.8.0\_131\\jre\\lib\\security\\cacerts" -storepass changeit 
```

When prompted to "trust this certificate," answer ‘yes’. 

## Package and sign the connector


### Run the package module 

The connector-packager tool must be run from the connector-plugin-sdk/connector-packager/ directory.  There are several ways to run the tool:

-   To package the connector and sign it, run this command: 
 
    ```
    python -m connector\_packager.package \[path\_to\_plugin\_folder\] -a \[alias\_name\] -ks \[keystore\_file\_path\]
    ```

    For example:  
    
    ```
    python -m connector\_packager.package .\\tests\\test\_resources\\valid\_connector -a key\_same\_pwd -ks tests\\test\_resources\\test\_keystore\\test\_ks.jks --dest d:/pp 
    ```
 

-   To package the connector without signing, run this command:  

    ```
    python -m connector\_packager.package \[path\_to\_plugin\_folder\] --package-only  
    ```
    
    For example:
    
    ```
    python -m connector\_packager.package d:/plugins-samples/postgres\_odbc --package-only
    ```


-   To validate that the .xml files are valid, run this command:

    ```
    python -m connector\_packager.package --validate-only \[path\_to\_plugin\_folder\] 
    ```

    For example:

    ```
    python -m connector\_packager.package --validate-only d:/plugins 
    ```

Review the following examples:

#### Example 1: .taco file is generated into connector-plugin-sdk\\connector-packager\\packaged-connector 

```
(.venv) E:\\connector-plugin-sdk\\connector-packager>python -m connector\_packager.package ..\\samples\\plugins\\mysql\_odbc -a test1year -ks test1yearkeystore.jks

Validation succeeded.

mysql\_odbc\_sample.taco was created in E:\\connector-plugin-sdk\\connector-packager\\packaged-connector

Enter keystore password:

Enter password for alias test1year:(RETURN if same as keystore password)

jar signed.

Warning:

No -tsa or -tsacert is provided and this jar is not timestamped. Without a timestamp, users may not be able to validate this jar after the signer certificate's expiration date (2020-10-06) or after any future revocation date.

taco was signed as mysql\_odbc\_sample.taco at E:\\connector-plugin-sdk\\connector-packager\\packaged-connector

```

#### Example 2: .taco file is generated into user supplied location and log file is generated into user supplied location 

```
(.venv) E:\\connector-plugin-sdk\\connector-packager>python -m connector\_packager.package ..\\samples\\plugins\\mysql\_odbc -a test1year -ks test1yearkeystore.jks --dest e:\\temp -l e:\\temp

Validation succeeded.

mysql\_odbc\_sample.taco was created in e:\\temp

Enter keystore password:

Enter password for alias test1year:(RETURN if same as keystore password)

jar signed.

Warning:

No -tsa or -tsacert is provided and this jar is not timestamped. Without a timestamp, users may not be able to validate this jar after the signer certificate's expiration date (2020-10-06) or after any future revocation date.

```


### Verify the connector with signature

**Note:** You can use the package tool to package and sign the connector, and use the connector in Tableau Desktop 2019.x. Signature verification is supported starting in Tableau Desktop 2019.4 on Windows.  

You can install and test your connector one of two ways:

-   Put your .taco file in the standard location, My Tableau Repository/Connectors, then launch Tableau Desktop. 

-   Put your .taco file anywhere you want. Launch Tableau Desktop with the packaged and signed connector with the option -DConnectPluginsPath . For example:

    ```
    "C:\\Program Files\\Tableau\\Tableau 2019.4\\bin\\tableau.exe" -DConnectPluginsPath="d:\\connector-plugin-sdk\\connector-packager\\packaged-connector" 
    ```

In both cases, when you launch Tableau Desktop, your connector is listed on the **Connect** pane, under **To a Server** > **More**.

![]({{ site.baseurl }}/assets/connect-pane.png) 
 

To connect, select the name of your connector, enter the information in the Connection dialog, and then click **Sign In**.

![]({{ site.baseurl }}/assets/data-source-page.png)

### (Optional) Verify the connector without a signature

You can verify a packaged connector without a signature. If everything is correct, other than the signature, the process should only skip the signature verification part and perform all the other steps correctly. This includes connecting to the data. To verify the connector without a signature, follow these steps:

1.  Package the connector with –package-only. For example:

    ```
    (.venv) E:\\connector-plugin-sdk\\connector-packager>python -m connector\_packager.package ..\\samples\\plugins\\postgres\_odbc --package-only
    ```

1.  Launch Tableau Desktop by skipping signature verification with -DDisableVerifyConnectorPluginSignature=true. For example:

    ```
    (.venv) E:\\connector-plugin-sdk\\connector-packager>"c:\\Program Files\\Tableau\\Tableau 2019.4\\bin\\tableau.exe" -DDisableVerifyConnectorPluginSignature=true -DConnectPluginsPath="E:\\connector-plugin-sdk\\connector-packager\\packaged-connector"
    ```
    When you launch Tableau Desktop, your connector is listed on the **Connect** pane, under **To a Server** > **More**.

1.  Select the connector, enter the information you're prompted for, and click **Sign In** to connect. 

## Troubleshoot connector packaging and signing


### Where to find log files 

By default, a log file packaging\_log.txt will be generated at connector-plugin-sdk/connector-packager/ directory 

### XML Validation failed for manifest.xml  

Packaging failed. Check your\_path\\connector-plugin-sdk\\connector-packager\\packaging\_log.txt for more information. 

Check your manifest.xml file. You can do validate only with –v to get more details and make sure your package is valid. For example: 

```
(.venv) E:\\packagetest\\connector-plugin-sdk\\connector-packager>python -m connector\_packager.package --validate-only e:\\badplugins\\mysql\_odbc –v 
```

### keytool error: java.io.FileNotFoundException: C:\\Program Files\\Java\\jdk1.8.0\_131\\jre\\lib\\security\\cacerts 

Check your path to see if the JRE does exist under jdk1.8.0\_131. If not, you might need to reinstall Java JDK.

For JDK9 and later, the path is Java\\jdk\_version\\lib\\security\\cacerts

 

### Java Error: jdk\_create\_jar: no jdk set up in PATH environment variable, please download JAVA JDK and add it to PATH 

Check your PATH environment variable and make sure that JAVA\_HOME is in PATH.

### keytool error: java.io.FileNotFoundException: C:\\Program Files\\Java\\jdk-12.0.2\\lib\\security" -storepass changeit  (The filename, directory name, or volume label syntax is incorrect) 

Make sure that the path includes "cacerts" as in the following example:

```
C:\\Program Files\\Java\\jdk1.8.0\_131\\jre\\lib\\security\\cacerts 
```