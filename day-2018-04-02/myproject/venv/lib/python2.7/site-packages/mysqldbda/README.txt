This files helps you installing the MySQL Database adapter in Zope 3
In this document I'm assuming your Zope3 lives in ~/Zope3.

Installing mysqldbda

  1. Check out the mysqldbda product into ~/Zope3/src

       cd ~/Zope3/src
       cvs -d :pserver:anonymous@cvs.zope.org:/cvs-repository login
       cvs -d :pserver:anonymous@cvs.zope.org:/cvs-repository checkout \
                                                mysqldbda

  2. Create a file named 'mysqldbda-configure.zcml' inside
     ~/Zope3/package-includes with the following contents:

       <include package='mysqldbda' />

Creating Database Connections

  It is time to add some connections. A connection in Zope 3 is
  registered as a utility.

  3. Open a web browser on your Zope root folder (http://localhost:8080/ if
     you use the default settings in zope.conf.in).

  4. Click on the 'Manage Site' action on the right side of the
     screen. You should see a screen which reads 'Common Site
     Management Tasks'

  5. Around the middle of that page, you should see a link named 'Add
     Utility'. Click on it.

  6. Select 'MySQL DA' and type in a name at the bottom of the page.

  7. Enter the database connection string.  It looks like this:

        dbi://username:password@host:port/databasename

  8. Click on the 'Add' button.

  9. You should be on a page which reads 'Add Database Connection
     Registration'. There you can configure the permission needed to
     use the database connection, the name of the registration and the
     registration status. You can use any name for 'Register As'
     field, as long as it doesn't clash with an existing one. Choose a
     permission. Choose between 'Registered' and 'Active' for  the
     'Registration Status'. Only one component of a kind can be
     'Active' at a time, so be careful.

  10. You should be redirected to the 'Edit' screen of the connection
      utility.

  11. If you want to, you can go to the Test page and execute arbitrary SQL
      queries to see whether the connection is working as expected.

Using SQL Scripts

  You can create SQL Scripts in the content space.  For example:

  12. Go to Zope root.

  13. Add an SQL script (you can use the Common Tasks box on the left, or
      the Add action on the right).

  14. Click on the name of your new SQL script.

  15. Choose a connection name (the one you entered in step 29) from the
      drop-down.

  16. Enter your query and click on the 'Save Changes' button.

  17. You can test the script in the -- surprise! -- Test page.